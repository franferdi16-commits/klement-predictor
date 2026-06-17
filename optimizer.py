# optimizer.py v2.0 - Optimiza divisores, techo, noise scales, bonus_top5/otra
# y genera diaspora_override por equipo desde resultados reales.
import json, os, sys
import numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson

PARAMS_DEFAULT = {
    "divisor_k": 20.0, "divisor_g": 19.0, "techo_lambda": 2.5,
    "k_noise_scale": 1.0, "m2_noise_scale": 1.0,
    "bonus_top5": 0.016, "bonus_otra": 0.007,
    "diaspora_override": {},
}

# ── I/O ───────────────────────────────────────────────────────────────────────
def cargar_historial(path="historial.json"):
    if not os.path.exists(path):
        print(f"⚠️  No se encontró {path}")
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def cargar_params(path="params.json"):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            p = json.load(f)
        for k, v in PARAMS_DEFAULT.items():
            if k not in p:
                p[k] = v
        return p
    return dict(PARAMS_DEFAULT)

def guardar_params(params, path="params.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(params, f, ensure_ascii=False, indent=2)
    print(f"✅ params.json guardado")

# ── Cálculo de lambda con params variables ────────────────────────────────────
def _lambda(datos, nombre, rival_confed, es_local, liga_index, params, motor):
    li   = liga_index.get(nombre, {"top5_eur": 0, "otra_eur": 0})
    bon  = (li["top5_eur"] * params["bonus_top5"] +
            li["otra_eur"] * params["bonus_otra"])
    bon  = min(0.40, max(-0.10, bon))
    ov   = params.get("diaspora_override", {}).get(nombre, 0.0)
    bon  = max(-0.15, min(0.40, bon + ov))

    if motor == "k":
        pk   = datos["pib"] / 1000
        f    = ((100 - datos["ranking"]) * 0.40
                + pk * 0.15 - 0.0015 * pk**2
                + np.log(max(1.0, datos["poblacion"])) * 0.20
                - 0.08 * abs(datos["temp"] - 14.0)
                + (-0.6 if datos["campeon"] else 0.0))
        f   *= (1 + bon)
        kn   = datos["k_noise"] * params["k_noise_scale"]
        f   *= (1 + kn) if es_local else (1 - abs(kn * 0.5))
        div  = params["divisor_k"]
    else:
        pk   = datos["pib"] / 1000
        f    = ((100 - datos["ranking"]) * 0.50
                + pk * 0.18 - 0.0018 * pk**2
                + np.log(max(1.0, datos["poblacion"])) * 0.25
                - 0.05 * abs(datos["temp"] - 14.0))
        f   *= (1 + bon)
        m2n  = datos["m2_noise"] * params["m2_noise_scale"]
        if es_local:
            res = 1.0 if rival_confed == "CONMEBOL" else (0.75 if rival_confed == "UEFA" else 0.55)
            f  *= (1 + m2n * (1 - res))
        else:
            f  *= 0.90
        div  = params["divisor_g"]

    return min(params["techo_lambda"], max(0.2, f / div))

def _mu(local, visitante, teams, liga_index, params):
    da, db = teams[local], teams[visitante]
    lk_a = _lambda(da, local,    db["confed"], True,  liga_index, params, "k")
    lk_b = _lambda(db, visitante, da["confed"], False, liga_index, params, "k")
    lg_a = _lambda(da, local,    db["confed"], True,  liga_index, params, "g")
    lg_b = _lambda(db, visitante, da["confed"], False, liga_index, params, "g")
    return 0.5*lk_a + 0.5*lg_a, 0.5*lk_b + 0.5*lg_b

# ── Función objetivo global ───────────────────────────────────────────────────
def objetivo_global(x, partidos, teams, liga_index, params_base):
    div_k, div_g, techo, kns, m2s, bt5, bot = x
    if any(v <= 0 for v in [div_k, div_g, techo, kns, m2s, bt5, bot]):
        return 1e9
    p = {**params_base,
         "divisor_k": div_k, "divisor_g": div_g, "techo_lambda": techo,
         "k_noise_scale": kns, "m2_noise_scale": m2s,
         "bonus_top5": bt5, "bonus_otra": bot}
    total, n = 0.0, 0
    for res in partidos.values():
        loc, vis = res["local"], res["visitante"]
        if loc not in teams or vis not in teams:
            continue
        mu_a, mu_b = _mu(loc, vis, teams, liga_index, p)
        ll = -np.log(max(poisson.pmf(res["goles_l"], mu_a) *
                         poisson.pmf(res["goles_v"], mu_b), 1e-9))
        total += ll; n += 1
    return total / max(n, 1)

def optimizar_global(partidos, teams, liga_index, params):
    print("\n🔧 Optimizando parámetros globales (7 variables)...")
    x0 = [params["divisor_k"], params["divisor_g"], params["techo_lambda"],
          params["k_noise_scale"], params["m2_noise_scale"],
          params["bonus_top5"], params["bonus_otra"]]
    ll0 = objetivo_global(x0, partidos, teams, liga_index, params)
    print(f"   Log Loss inicial: {ll0:.4f}")

    res = minimize(objetivo_global, x0,
                   args=(partidos, teams, liga_index, params),
                   method="Nelder-Mead",
                   options={"maxiter": 3000, "xatol": 1e-5, "fatol": 1e-5})

    if res.fun < ll0:
        div_k, div_g, techo, kns, m2s, bt5, bot = res.x
        print(f"   Log Loss final:   {res.fun:.4f} ✅")
        print(f"   divisor_k={div_k:.2f}  divisor_g={div_g:.2f}  techo={techo:.2f}")
        print(f"   k_noise_scale={kns:.3f}  m2_noise_scale={m2s:.3f}")
        print(f"   bonus_top5={bt5:.4f}  bonus_otra={bot:.4f}")
        return {
            "divisor_k":      round(max(10, min(35, div_k)), 3),
            "divisor_g":      round(max(10, min(35, div_g)), 3),
            "techo_lambda":   round(max(1.5, min(4.0, techo)), 3),
            "k_noise_scale":  round(max(0.3, min(2.0, kns)),  4),
            "m2_noise_scale": round(max(0.3, min(2.0, m2s)),  4),
            "bonus_top5":     round(max(0.005, min(0.04, bt5)), 5),
            "bonus_otra":     round(max(0.002, min(0.02, bot)), 5),
        }
    else:
        print("   ⚠️  Sin mejora, manteniendo valores actuales.")
        return {k: params[k] for k in ["divisor_k","divisor_g","techo_lambda",
                                        "k_noise_scale","m2_noise_scale",
                                        "bonus_top5","bonus_otra"]}

# ── Override por equipo ───────────────────────────────────────────────────────
def optimizar_overrides(partidos, teams, liga_index, params):
    """Ajusta diaspora_override por equipo según error real vs predicho."""
    print("\n🌍 Ajustando overrides por equipo...")
    errores = {}
    for res in partidos.values():
        loc, vis = res["local"], res["visitante"]
        if loc not in teams or vis not in teams:
            continue
        mu_a, mu_b = _mu(loc, vis, teams, liga_index, params)
        errores.setdefault(loc, []).append(res["goles_l"] - mu_a)
        errores.setdefault(vis, []).append(res["goles_v"] - mu_b)

    LR = 0.07
    overrides = dict(params.get("diaspora_override", {}))
    for eq, errs in errores.items():
        err = np.mean(errs)
        ov_actual = overrides.get(eq, 0.0)
        ov_nuevo  = ov_actual + LR * np.sign(err) * min(abs(err), 1.0)
        ov_nuevo  = round(max(-0.20, min(0.30, ov_nuevo)), 4)
        if abs(ov_nuevo - ov_actual) > 0.003:
            print(f"   {eq:<35} override: {ov_actual:+.4f} → {ov_nuevo:+.4f}  (err={err:+.2f})")
        overrides[eq] = ov_nuevo
    return overrides

# ── Reporte ───────────────────────────────────────────────────────────────────
def reporte(partidos, teams, liga_index, params):
    print(f"\n{'Partido':<38} {'Real':<5} {'λL':>5} {'λV':>5} {'Pred':>6} {'LL':>7}")
    print("-" * 70)
    total, n = 0.0, 0
    for pid, res in sorted(partidos.items(), key=lambda x: int(x[0])):
        loc, vis = res["local"], res["visitante"]
        if loc not in teams or vis not in teams: continue
        mu_a, mu_b = _mu(loc, vis, teams, liga_index, params)
        ll = -np.log(max(poisson.pmf(res["goles_l"], mu_a) *
                         poisson.pmf(res["goles_v"], mu_b), 1e-9))
        total += ll; n += 1
        p_str = f"{loc} vs {vis}"[:37]
        print(f"{p_str:<38} {res['goles_l']}-{res['goles_v']:<3} "
              f"{mu_a:>5.2f} {mu_b:>5.2f} {round(mu_a)}-{round(mu_b):>2} {ll:>7.3f}")
    print(f"\n{'Log Loss promedio:':<38} {total/max(n,1):.4f}  ({n} partidos)")

# ── Main ──────────────────────────────────────────────────────────────────────
def run(historial_path="historial.json", params_path="params.json"):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import data

    hist = cargar_historial(historial_path)
    if not hist: return
    partidos = hist.get("partidos_jugados", {})
    if not partidos:
        print("⚠️  Sin partidos en historial."); return

    print(f"📂 {len(partidos)} partidos cargados")
    params = cargar_params(params_path)

    # 1. Optimizar 7 parámetros globales
    nuevos = optimizar_global(partidos, data.TEAMS, data.LIGA_INDEX, params)
    params.update(nuevos)

    # 2. Override por equipo
    params["diaspora_override"] = optimizar_overrides(
        partidos, data.TEAMS, data.LIGA_INDEX, params)

    # 3. Guardar
    guardar_params(params, params_path)

    # 4. Reporte
    reporte(partidos, data.TEAMS, data.LIGA_INDEX, params)

if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else "historial.json"
    p = sys.argv[2] if len(sys.argv) > 2 else "params.json"
    run(h, p)
