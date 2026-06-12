# engines.py - Motores de Simulación Numérica y Control de Desviación Predictiva
import numpy as np
import scipy.stats as stats

def engine_klement(datos, rival_confed, es_local):
    """Modelo 1: Joachim Klement (Econometría Aplicada)"""
    f_deportiva = (100 - datos["ranking"]) * 0.40
    pib_k = datos["pib"] / 1000
    f_economica = (pib_k * 0.15) - (0.0015 * (pib_k ** 2))
    f_demografica = np.log(datos["poblacion"]) * 0.20
    f_clima = -0.08 * abs(datos["temp"] - 14.0)
    fuerza = f_deportiva + f_economica + f_demografica + f_clima + (-0.6 if datos["campeon"] else 0.0)
    if es_local:
        fuerza *= (1.0 + datos["k_noise"])
    return max(0.5, fuerza / 13.0)

def engine_model_two(datos, rival_confed, es_local):
    """Modelo 2: Ajuste Alternativo No Lineal"""
    f_deportiva = (100 - datos["ranking"]) * 0.50
    pib_k = datos["pib"] / 1000
    f_economica = (pib_k * 0.18) - (0.0018 * (pib_k ** 2))
    f_demografica = np.log(datos["poblacion"]) * 0.25
    f_clima = -0.05 * abs(datos["temp"] - 14.0)
    fuerza = f_deportiva + f_economica + f_demografica + f_clima
    if es_local:
        resistencia = 1.0 if rival_confed == "CONMEBOL" else (0.75 if rival_confed == "UEFA" else 0.55)
        fuerza *= (1.0 + (datos["m2_noise"] * (1.0 - resistencia)))
    return max(0.5, fuerza / 12.5)

def ejecutar_montecarlo(lk_a, lk_b, lg_a, lg_b, n_simulaciones=10000):
    """Ejecuta las 10,000 iteraciones estocásticas distribuidas por Poisson"""
    sim_k_a = stats.poisson.rvs(mu=lk_a, size=n_simulaciones)
    sim_k_b = stats.poisson.rvs(mu=lk_b, size=n_simulaciones)
    sim_g_a = stats.poisson.rvs(mu=lg_a, size=n_simulaciones)
    sim_g_b = stats.poisson.rvs(mu=lg_b, size=n_simulaciones)

    res = {
        "pk_a": float(np.sum(sim_k_a > sim_k_b) / (n_simulaciones / 100)),
        "pk_emp": float(np.sum(sim_k_a == sim_k_b) / (n_simulaciones / 100)),
        "pk_b": float(np.sum(sim_k_b > sim_k_a) / (n_simulaciones / 100)),
        "pg_a": float(np.sum(sim_g_a > sim_g_b) / (n_simulaciones / 100)),
        "pg_emp": float(np.sum(sim_g_a == sim_g_b) / (n_simulaciones / 100)),
        "pg_b": float(np.sum(sim_g_b > sim_g_a) / (n_simulaciones / 100))
    }
    return res