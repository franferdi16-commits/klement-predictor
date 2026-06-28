# calibrador.py - Calibrador Bayesiano + Ajuste Dinámico de Fuerzas v2.0
import numpy as np
import scipy.stats as stats
import data

# ── Fuerzas base derivadas de los parámetros de data.py ──────────────────────
def fuerzas_base():
    """
    Genera el diccionario inicial de ataque/defensa para los 48 equipos
    derivado matemáticamente de ranking + k_noise + m2_noise.
    Se usa solo la primera vez (cuando fuerzas={} en el JSON).
    """
    fuerzas = {}
    for nombre, d in data.TEAMS.items():
        fuerza_ranking = (100 - d["ranking"]) / 100  # 0..1
        fuerzas[nombre] = {
            "ataque":  round(0.8 + fuerza_ranking * 1.8 + d["m2_noise"] * 0.5, 4),
            "defensa": round(0.6 + fuerza_ranking * 1.2 - d["k_noise"]  * 0.3, 4),
        }
    return fuerzas

def get_fuerzas(fuerzas_guardadas):
    """Devuelve fuerzas guardadas o genera las base si están vacías."""
    if not fuerzas_guardadas:
        return fuerzas_base()
    # Rellenar equipos que falten (por si se agregaron al data.py)
    base = fuerzas_base()
    for eq in base:
        if eq not in fuerzas_guardadas:
            fuerzas_guardadas[eq] = base[eq]
    return fuerzas_guardadas

# ── Ajuste dinámico post-partido (aprendizaje online) ────────────────────────
FACTOR_AJUSTE = 0.10   # Qué tan rápido aprende el modelo

def actualizar_fuerzas(fuerzas, local, visitante, goles_l, goles_v, lambda_l, lambda_v):
    """
    Ajusta ataque/defensa de ambos equipos basándose en el error real vs predicho.
    Se llama UNA VEZ por partido, justo al guardar el resultado.
    """
    f = fuerzas

    # Equipo local
    f[local]["ataque"]    = max(0.1, f[local]["ataque"]    + FACTOR_AJUSTE * (goles_l - lambda_l))
    f[visitante]["defensa"] = max(0.1, f[visitante]["defensa"] - FACTOR_AJUSTE * (lambda_l - goles_l))

    # Equipo visitante
    f[visitante]["ataque"]  = max(0.1, f[visitante]["ataque"]  + FACTOR_AJUSTE * (goles_v - lambda_v))
    f[local]["defensa"]     = max(0.1, f[local]["defensa"]     - FACTOR_AJUSTE * (lambda_v - goles_v))

    return f

# ── Calibrador bayesiano con fuerzas dinámicas ────────────────────────────────
def recalcular_con_tendencia_real(match_id, partidos_jugados, fuerzas,
                                   lk_a, lk_b, lg_a, lg_b, n_simulaciones=10000):
    """
    Combina:
    1. Tendencia global del torneo (tasa de empates real)
    2. Rendimiento reciente individual de cada equipo
    3. Lambdas ajustados por fuerzas dinámicas ataque/defensa
    """
    match_data = next(p for p in data.FIXTURE if p["id"] == match_id)
    team_a, team_b = match_data["local"], match_data["visitante"]

    # 1. Tendencia global
    total = len(partidos_jugados)
    empates = sum(1 for p in partidos_jugados.values() if p["goles_l"] == p["goles_v"])
    tasa_empates = (empates / total) if total > 0 else 0.25
    ajuste_paridad = 1.15 if tasa_empates > 0.30 else 1.0

    # 2. Rendimiento reciente
    def rendimiento(equipo):
        pj, pts = 0, 0
        for r in partidos_jugados.values():
            if r["local"] == equipo or r["visitante"] == equipo:
                pj += 1
                es_local = (r["local"] == equipo)
                if r["goles_l"] == r["goles_v"]:
                    pts += 1
                elif (r["goles_l"] > r["goles_v"]) == es_local:
                    pts += 3
        return pts / (pj * 3) if pj > 0 else 1.0

    rend_a = rendimiento(team_a)
    rend_b = rendimiento(team_b)

    # 3. Lambda ajustado por fuerzas dinámicas
    fa = fuerzas.get(team_a, {"ataque": 1.5, "defensa": 1.0})
    fb = fuerzas.get(team_b, {"ataque": 1.5, "defensa": 1.0})

    # Lambda fusionado base × fuerza dinámica × rendimiento reciente
    mu_base_a = (0.6 * lk_a + 0.4 * lg_a)
    mu_base_b = (0.6 * lk_b + 0.4 * lg_b)

    mu_a = mu_base_a * (fa["ataque"] / fb["defensa"]) * (0.8 + rend_a * 0.4)
    mu_b = mu_base_b * (fb["ataque"] / fa["defensa"]) * (0.8 + rend_b * 0.4)

    # Protección de rango
    mu_a = max(0.2, min(mu_a, 5.0))
    mu_b = max(0.2, min(mu_b, 5.0))

    # 4. Montecarlo
    sim_a = stats.poisson.rvs(mu=mu_a, size=n_simulaciones)
    sim_b = stats.poisson.rvs(mu=mu_b, size=n_simulaciones)

    if ajuste_paridad > 1.0:
        mascara = np.random.rand(n_simulaciones) < 0.15
        sim_b[mascara] = sim_a[mascara]

    def prob(sa, sb):
        a   = max(0.1, float(np.sum(sa >  sb) / n_simulaciones) * 100)
        emp = max(0.1, float(np.sum(sa == sb) / n_simulaciones) * 100)
        b   = max(0.1, float(np.sum(sb >  sa) / n_simulaciones) * 100)
        s   = a + emp + b
        return (a/s)*100, (emp/s)*100, (b/s)*100

    pf_a, pf_emp, pf_b = prob(sim_a, sim_b)

    # Mantener compatibilidad pk_*/pg_* para Log Loss
    sim_k_a = stats.poisson.rvs(mu=lk_a, size=n_simulaciones)
    sim_k_b = stats.poisson.rvs(mu=lk_b, size=n_simulaciones)
    sim_g_a = stats.poisson.rvs(mu=lg_a, size=n_simulaciones)
    sim_g_b = stats.poisson.rvs(mu=lg_b, size=n_simulaciones)
    pk_a, pk_emp, pk_b = prob(sim_k_a, sim_k_b)
    pg_a, pg_emp, pg_b = prob(sim_g_a, sim_g_b)

    return {
        "pk_a": pk_a, "pk_emp": pk_emp, "pk_b": pk_b,
        "pg_a": pg_a, "pg_emp": pg_emp, "pg_b": pg_b,
        "pf_a": pf_a, "pf_emp": pf_emp, "pf_b": pf_b,
        "mu_a": round(mu_a, 3), "mu_b": round(mu_b, 3),
    }

# ── Modo Eliminatoria: sin empate, con penales ────────────────────────────────
def simular_eliminatoria(mu_a, mu_b, n_simulaciones=10000):
    """
    En eliminatorias no hay empate final.
    Si 90min empatan → prórroga (lambdas reducidos 40%) → si siguen empatados → penales (50/50 + sesgo fuerzas).
    Devuelve prob_a, prob_b y si_penales (% que van a penales).
    """
    import numpy as np
    import scipy.stats as stats

    sim_a = stats.poisson.rvs(mu=mu_a, size=n_simulaciones)
    sim_b = stats.poisson.rvs(mu=mu_b, size=n_simulaciones)

    gana_a   = sim_a > sim_b
    gana_b   = sim_b > sim_a
    empate90 = sim_a == sim_b

    # Prórroga: lambda reducido 40%
    mu_et_a = mu_a * 0.60
    mu_et_b = mu_b * 0.60
    et_a = stats.poisson.rvs(mu=mu_et_a, size=n_simulaciones)
    et_b = stats.poisson.rvs(mu=mu_et_b, size=n_simulaciones)

    gana_a_et   = empate90 & (et_a > et_b)
    gana_b_et   = empate90 & (et_b > et_a)
    empate_et   = empate90 & (et_a == et_b)   # → penales

    # Penales: base 50/50 con pequeño sesgo por fuerzas
    sesgo = min(0.08, abs(mu_a - mu_b) / (mu_a + mu_b + 1e-6))
    prob_pen_a = 0.50 + (sesgo if mu_a > mu_b else -sesgo)

    pen_wins_a = np.random.rand(n_simulaciones) < prob_pen_a
    gana_a_pen = empate_et &  pen_wins_a
    gana_b_pen = empate_et & ~pen_wins_a

    total_a = np.sum(gana_a | gana_a_et | gana_a_pen)
    total_b = np.sum(gana_b | gana_b_et | gana_b_pen)
    van_penales = int(np.sum(empate_et))

    prob_a = round(float(total_a / n_simulaciones) * 100, 1)
    prob_b = round(float(total_b / n_simulaciones) * 100, 1)
    pct_penales = round(float(van_penales / n_simulaciones) * 100, 1)

    return prob_a, prob_b, pct_penales
