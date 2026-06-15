# engines.py - Motor Fusionado de Simulación Numérica v2.0
# Combina Klement + Modelo 2 en un único lambda ponderado por Log Loss histórico,
# añade predicción de marcador probable y vectores de goles por simulación.
import numpy as np
import scipy.stats as stats
from collections import Counter

# ─────────────────────────────────────────────────────────────────────────────
# BLOQUE 1: CÁLCULO DE FUERZA BASE (los dos motores originales, intactos)
# ─────────────────────────────────────────────────────────────────────────────

def engine_klement(datos, rival_confed, es_local):
    """Modelo 1: Joachim Klement (Econometría Aplicada)"""
    f_deportiva  = (100 - datos["ranking"]) * 0.40
    pib_k        = datos["pib"] / 1000
    f_economica  = (pib_k * 0.15) - (0.0015 * (pib_k ** 2))
    f_demografica = np.log(max(1.0, datos["poblacion"])) * 0.20
    f_clima      = -0.08 * abs(datos["temp"] - 14.0)
    fuerza       = f_deportiva + f_economica + f_demografica + f_clima + (-0.6 if datos["campeon"] else 0.0)
    if es_local:
        fuerza *= (1.0 + datos["k_noise"])
    else:
        fuerza *= (1.0 - abs(datos["k_noise"] * 0.5))
    return max(0.2, fuerza / 13.0)


def engine_model_two(datos, rival_confed, es_local):
    """Modelo 2: Ajuste Alternativo No Lineal"""
    f_deportiva  = (100 - datos["ranking"]) * 0.50
    pib_k        = datos["pib"] / 1000
    f_economica  = (pib_k * 0.18) - (0.0018 * (pib_k ** 2))
    f_demografica = np.log(max(1.0, datos["poblacion"])) * 0.25
    f_clima      = -0.05 * abs(datos["temp"] - 14.0)
    fuerza       = f_deportiva + f_economica + f_demografica + f_clima
    if es_local:
        resistencia = 1.0 if rival_confed == "CONMEBOL" else (0.75 if rival_confed == "UEFA" else 0.55)
        fuerza *= (1.0 + (datos["m2_noise"] * (1.0 - resistencia)))
    else:
        fuerza *= 0.90
    return max(0.2, fuerza / 12.5)


# ─────────────────────────────────────────────────────────────────────────────
# BLOQUE 2: FUSIÓN DINÁMICA PONDERADA POR LOG LOSS HISTÓRICO
# ─────────────────────────────────────────────────────────────────────────────

def calcular_pesos_por_logloss(audit_history):
    """
    Deriva los pesos w_k y w_g desde el historial de auditoría.
    El modelo con menor Log Loss acumulado recibe mayor peso.
    Si no hay historial, los pesos son iguales (50/50).
    """
    if not audit_history or len(audit_history) < 2:
        return 0.5, 0.5

    ll_k = np.mean([r["Log Loss Klement"]  for r in audit_history])
    ll_g = np.mean([r["Log Loss Modelo 2"] for r in audit_history])

    # Invertimos: menor Log Loss = mayor peso
    inv_k = 1.0 / max(ll_k, 1e-6)
    inv_g = 1.0 / max(ll_g, 1e-6)
    total  = inv_k + inv_g
    return inv_k / total, inv_g / total


def fusionar_lambdas(lk_a, lk_b, lg_a, lg_b, w_k, w_g):
    """
    Combina los lambdas de Poisson de ambos motores con los pesos derivados.
    Resultado: un único par (mu_a, mu_b) para el motor fusionado.
    """
    mu_a = w_k * lk_a + w_g * lg_a
    mu_b = w_k * lk_b + w_g * lg_b
    return mu_a, mu_b


# ─────────────────────────────────────────────────────────────────────────────
# BLOQUE 3: MONTECARLO UNIFICADO CON MARCADOR PROBABLE
# ─────────────────────────────────────────────────────────────────────────────

def ejecutar_montecarlo(lk_a, lk_b, lg_a, lg_b, n_simulaciones=10000, audit_history=None):
    """
    Motor principal unificado.
    - Fusiona ambos modelos con pesos dinámicos por Log Loss.
    - Genera 10.000 simulaciones Poisson.
    - Devuelve probabilidades G/E/P, marcador más probable, y top 5 marcadores.
    - Mantiene compatibilidad total con el sistema de Log Loss existente
      devolviendo también pk_*/pg_* para la pestaña 2.
    """
    if audit_history is None:
        audit_history = []

    w_k, w_g = calcular_pesos_por_logloss(audit_history)

    # ── Lambda fusionado (motor principal) ──
    mu_a, mu_b = fusionar_lambdas(lk_a, lk_b, lg_a, lg_b, w_k, w_g)

    # ── Simulaciones del motor fusionado ──
    sim_a = stats.poisson.rvs(mu=mu_a, size=n_simulaciones)
    sim_b = stats.poisson.rvs(mu=mu_b, size=n_simulaciones)

    # ── Probabilidades G/E/P fusionadas ──
    pf_a   = float(np.sum(sim_a >  sim_b) / n_simulaciones) * 100
    pf_emp = float(np.sum(sim_a == sim_b) / n_simulaciones) * 100
    pf_b   = float(np.sum(sim_b >  sim_a) / n_simulaciones) * 100

    # ── Normalización estricta ──
    def normalizar(a, e, b):
        a, e, b = max(0.1, a), max(0.1, e), max(0.1, b)
        s = a + e + b
        return (a/s)*100, (e/s)*100, (b/s)*100

    pf_a, pf_emp, pf_b = normalizar(pf_a, pf_emp, pf_b)

    # ── Marcadores más frecuentes (top 5) ──
    marcadores = Counter(zip(sim_a.tolist(), sim_b.tolist()))
    top5 = marcadores.most_common(5)
    marcador_prob   = top5[0][0]           # Marcador más probable
    marcador_prob_p = top5[0][1] / n_simulaciones * 100  # Su frecuencia %

    # ── Lambdas individuales para Log Loss (compatibilidad con pestaña 2) ──
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
        # ── Motor fusionado (principal) ──
        "pf_a":   pf_a,
        "pf_emp": pf_emp,
        "pf_b":   pf_b,
        "w_k":    round(w_k * 100, 1),
        "w_g":    round(w_g * 100, 1),
        "mu_a":   round(mu_a, 3),
        "mu_b":   round(mu_b, 3),
        # ── Marcador probable ──
        "marcador_prob":   marcador_prob,
        "marcador_prob_p": round(marcador_prob_p, 1),
        "top5_marcadores": top5,
        # ── Compatibilidad Log Loss (motores individuales) ──
        "pk_a": pk_a, "pk_emp": pk_emp, "pk_b": pk_b,
        "pg_a": pg_a, "pg_emp": pg_emp, "pg_b": pg_b,
    }
