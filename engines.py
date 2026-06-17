# engines.py v5.0 - Motor fusionado con LIGA_INDEX + params.json dinámico
import numpy as np
import scipy.stats as stats
from collections import Counter
import json, os

# ── Carga dinámica de params.json ─────────────────────────────────────────────
def _cargar_params():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "params.json")
    defaults = {
        "divisor_k": 20.0, "divisor_g": 19.0, "techo_lambda": 2.5,
        "k_noise_scale": 1.0, "m2_noise_scale": 1.0,
        "bonus_top5": 0.016,   # peso por jugador en top5 liga
        "bonus_otra": 0.007,   # peso por jugador en otra liga europea
        "diaspora_override": {},  # ajustes manuales post-optimizer por equipo
    }
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            p = json.load(f)
        for k, v in defaults.items():
            if k not in p:
                p[k] = v
        return p
    return defaults

_P = _cargar_params()

def recargar_params():
    global _P
    _P = _cargar_params()

# ── Bonus de calidad real desde LIGA_INDEX ────────────────────────────────────
def _bonus_liga(nombre_equipo):
    """
    Calcula el bonus desde LIGA_INDEX usando pesos por tipo de liga.
    Si el optimizer generó un override para este equipo, lo aplica encima.
    """
    try:
        import data as _d
        li = _d.LIGA_INDEX.get(nombre_equipo)
        if not li:
            return 0.0
        bonus = (li["top5_eur"] * _P["bonus_top5"] +
                 li["otra_eur"] * _P["bonus_otra"])
        bonus = min(0.40, max(-0.10, bonus))
    except Exception:
        bonus = 0.0

    # Override del optimizer si existe
    override = _P.get("diaspora_override", {}).get(nombre_equipo, None)
    if override is not None:
        bonus = max(-0.15, min(0.40, bonus + override))

    return bonus

# ── BLOQUE 1: MOTORES BASE ────────────────────────────────────────────────────

def engine_klement(datos, rival_confed, es_local, nombre_equipo=""):
    pib_k = datos["pib"] / 1000
    f = ((100 - datos["ranking"]) * 0.40
         + pib_k * 0.15 - 0.0015 * (pib_k ** 2)
         + np.log(max(1.0, datos["poblacion"])) * 0.20
         - 0.08 * abs(datos["temp"] - 14.0)
         + (-0.6 if datos["campeon"] else 0.0))
    f *= (1.0 + _bonus_liga(nombre_equipo))
    kn = datos["k_noise"] * _P["k_noise_scale"]
    f *= (1.0 + kn) if es_local else (1.0 - abs(kn * 0.5))
    return min(_P["techo_lambda"], max(0.2, f / _P["divisor_k"]))


def engine_model_two(datos, rival_confed, es_local, nombre_equipo=""):
    pib_k = datos["pib"] / 1000
    f = ((100 - datos["ranking"]) * 0.50
         + pib_k * 0.18 - 0.0018 * (pib_k ** 2)
         + np.log(max(1.0, datos["poblacion"])) * 0.25
         - 0.05 * abs(datos["temp"] - 14.0))
    f *= (1.0 + _bonus_liga(nombre_equipo))
    m2n = datos["m2_noise"] * _P["m2_noise_scale"]
    if es_local:
        res = (1.0 if rival_confed == "CONMEBOL"
               else 0.75 if rival_confed == "UEFA" else 0.55)
        f *= (1.0 + m2n * (1.0 - res))
    else:
        f *= 0.90
    return min(_P["techo_lambda"], max(0.2, f / _P["divisor_g"]))


# ── BLOQUE 2: FUSIÓN DINÁMICA POR LOG LOSS ───────────────────────────────────

def calcular_pesos_por_logloss(audit_history):
    if not audit_history or len(audit_history) < 2:
        return 0.5, 0.5
    ll_k = np.mean([r["Log Loss Klement"]  for r in audit_history])
    ll_g = np.mean([r["Log Loss Modelo 2"] for r in audit_history])
    inv_k = 1.0 / max(ll_k, 1e-6)
    inv_g = 1.0 / max(ll_g, 1e-6)
    s = inv_k + inv_g
    return inv_k / s, inv_g / s

def fusionar_lambdas(lk_a, lk_b, lg_a, lg_b, w_k, w_g):
    return w_k * lk_a + w_g * lg_a, w_k * lk_b + w_g * lg_b


# ── BLOQUE 3: MONTECARLO UNIFICADO ───────────────────────────────────────────

def ejecutar_montecarlo(lk_a, lk_b, lg_a, lg_b, n_simulaciones=10000, audit_history=None):
    if audit_history is None:
        audit_history = []

    w_k, w_g = calcular_pesos_por_logloss(audit_history)
    mu_a, mu_b = fusionar_lambdas(lk_a, lk_b, lg_a, lg_b, w_k, w_g)

    sim_a = stats.poisson.rvs(mu=mu_a, size=n_simulaciones)
    sim_b = stats.poisson.rvs(mu=mu_b, size=n_simulaciones)

    def normalizar(a, e, b):
        a, e, b = max(0.1, a), max(0.1, e), max(0.1, b)
        s = a + e + b
        return (a/s)*100, (e/s)*100, (b/s)*100

    pf_a, pf_emp, pf_b = normalizar(
        float(np.sum(sim_a >  sim_b) / n_simulaciones) * 100,
        float(np.sum(sim_a == sim_b) / n_simulaciones) * 100,
        float(np.sum(sim_b >  sim_a) / n_simulaciones) * 100,
    )
    top5 = Counter(zip(sim_a.tolist(), sim_b.tolist())).most_common(5)

    # Motores individuales para Log Loss
    sim_k_a = stats.poisson.rvs(mu=lk_a, size=n_simulaciones)
    sim_k_b = stats.poisson.rvs(mu=lk_b, size=n_simulaciones)
    sim_g_a = stats.poisson.rvs(mu=lg_a, size=n_simulaciones)
    sim_g_b = stats.poisson.rvs(mu=lg_b, size=n_simulaciones)

    pk_a, pk_emp, pk_b = normalizar(
        float(np.sum(sim_k_a >  sim_k_b) / n_simulaciones) * 100,
        float(np.sum(sim_k_a == sim_k_b) / n_simulaciones) * 100,
        float(np.sum(sim_k_b >  sim_k_a) / n_simulaciones) * 100,
    )
    pg_a, pg_emp, pg_b = normalizar(
        float(np.sum(sim_g_a >  sim_g_b) / n_simulaciones) * 100,
        float(np.sum(sim_g_a == sim_g_b) / n_simulaciones) * 100,
        float(np.sum(sim_g_b >  sim_g_a) / n_simulaciones) * 100,
    )

    return {
        "pf_a": pf_a, "pf_emp": pf_emp, "pf_b": pf_b,
        "w_k":  round(w_k * 100, 1), "w_g": round(w_g * 100, 1),
        "mu_a": round(mu_a, 3),       "mu_b": round(mu_b, 3),
        "marcador_prob":   top5[0][0],
        "marcador_prob_p": round(top5[0][1] / n_simulaciones * 100, 1),
        "top5_marcadores": top5,
        "pk_a": pk_a, "pk_emp": pk_emp, "pk_b": pk_b,
        "pg_a": pg_a, "pg_emp": pg_emp, "pg_b": pg_b,
    }
