# calibrador.py - Módulo Independiente de Calibración Bayesiana y Ajuste de Empates
import numpy as np
import scipy.stats as stats
import data

def recalcular_con_tendencia_real(match_id, partidos_jugados, lk_a, lk_b, lg_a, lg_b, n_simulaciones=10000):
    """
    Toma los parámetros base de tus motores y los reformula EN TIEMPO REAL 
    analizando si el torneo actual viene plagado de empates o sorpresas.
    """
    # 1. ANALIZAR LA TENDENCIA GLOBAL DEL TORNEO
    total_partidos = len(partidos_jugados)
    empates_reales = sum(1 for p in partidos_jugados.values() if p["goles_l"] == p["goles_v"])
    
    # Factor de ajuste global de empates (Por si el torneo viene muy cerrado)
    tasa_empates_real = (empates_reales / total_partidos) if total_partidos > 0 else 0.25
    # Si hay más de 30% de empates reales, activamos una penalización de dispersión
    ajuste_paridad = 1.15 if tasa_empates_real > 0.30 else 1.0

    # 2. IDENTIFICAR LOS EQUIPOS DEL MATCH ACTUAL
    match_data = next(p for p in data.FIXTURE if p['id'] == match_id)
    team_a, team_b = match_data['local'], match_data['visitante']

    # 3. CALCULAR EL FACTOR DE FORMA RECIENTE INDIVIDUAL
    def obtener_rendimiento(equipo):
        pj, pts = 0, 0
        for r in partidos_jugados.values():
            if r["local"] == equipo or r["visitante"] == equipo:
                pj += 1
                es_local = (r["local"] == equipo)
                if r["goles_l"] == r["goles_v"]:
                    pts += 1
                elif (r["goles_l"] > r["goles_v"] and es_local) or (r["goles_v"] > r["goles_l"] and not es_local):
                    pts += 3
        return pts / (pj * 3) if pj > 0 else 1.0

    rend_a = obtener_rendimiento(team_a)
    rend_b = obtener_rendimiento(team_b)

    # 4. RE-FORMULACIÓN DINÁMICA DE LOS LAMBDAS (MU) DE POISSON
    # Multiplicamos las fuerzas base por su rendimiento real en el torneo
    mu_k_a = lk_a * (0.8 + rend_a * 0.4)
    mu_k_b = lk_b * (0.8 + rend_b * 0.4)
    mu_g_a = lg_a * (0.8 + rend_a * 0.4)
    mu_g_b = lg_b * (0.8 + rend_b * 0.4)

    # 5. MONTECARLO ADAPTATIVO CON AJUSTE DE PARIDAD
    sim_k_a = stats.poisson.rvs(mu=mu_k_a, size=n_simulaciones)
    sim_k_b = stats.poisson.rvs(mu=mu_k_b, size=n_simulaciones)
    sim_g_a = stats.poisson.rvs(mu=mu_g_a, size=n_simulaciones)
    sim_g_b = stats.poisson.rvs(mu=mu_g_b, size=n_simulaciones)

    # Si la tendencia global es al empate, acercamos los vectores artificialmente
    if ajuste_paridad > 1.0:
        # Forzar una sutil convergencia de goles en partidos cerrados
        mascara_ajuste = np.random.rand(n_simulaciones) < 0.15
        sim_k_b[mascara_ajuste] = sim_k_a[mascara_ajuste]
        sim_g_b[mascara_ajuste] = sim_g_a[mascara_ajuste]

    # 6. CÁLCULO DE PROBABILIDADES FINAL NORMALIZADO
    pk_a = float(np.sum(sim_k_a > sim_k_b) / n_simulaciones) * 100
    pk_emp = float(np.sum(sim_k_a == sim_k_b) / n_simulaciones) * 100
    pk_b = float(np.sum(sim_k_b > sim_k_a) / n_simulaciones) * 100

    pg_a = float(np.sum(sim_g_a > sim_g_b) / n_simulaciones) * 100
    pg_emp = float(np.sum(sim_g_a == sim_g_b) / n_simulaciones) * 100
    pg_b = float(np.sum(sim_g_b > sim_g_a) / n_simulaciones) * 100

    res = {
        "pk_a": max(0.1, pk_a), "pk_emp": max(0.1, pk_emp), "pk_b": max(0.1, pk_b),
        "pg_a": max(0.1, pg_a), "pg_emp": max(0.1, pg_emp), "pg_b": max(0.1, pg_b)
    }

    # Re-normalización estricta a 100%
    sum_k = res["pk_a"] + res["pk_emp"] + res["pk_b"]
    res["pk_a"] = (res["pk_a"] / sum_k) * 100
    res["pk_emp"] = (res["pk_emp"] / sum_k) * 100
    res["pk_b"] = (res["pk_b"] / sum_k) * 100

    sum_g = res["pg_a"] + res["pg_emp"] + res["pg_b"]
    res["pg_a"] = (res["pg_a"] / sum_g) * 100
    res["pg_emp"] = (res["pg_emp"] / sum_g) * 100
    res["pg_b"] = (res["pg_b"] / sum_g) * 100

    return res
