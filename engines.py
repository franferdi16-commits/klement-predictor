# engines.py - Motores de Simulación Numérica y Control de Desviación Predictiva
import numpy as np
import scipy.stats as stats

def engine_klement(datos, rival_confed, es_local):
    """Modelo 1: Joachim Klement (Econometría Aplicada)"""
    f_deportiva = (100 - datos["ranking"]) * 0.40
    pib_k = datos["pib"] / 1000
    
    # Ecuación cuadrática econométrica
    f_economica = (pib_k * 0.15) - (0.0015 * (pib_k ** 2))
    f_demografica = np.log(max(1.0, datos["poblacion"])) * 0.20
    f_clima = -0.08 * abs(datos["temp"] - 14.0)
    
    fuerza = f_deportiva + f_economica + f_demografica + f_clima + (-0.6 if datos["campeon"] else 0.0)
    
    # Modificador de ajuste por localía / entorno confederativo
    if es_local:
        fuerza *= (1.0 + datos["k_noise"])
    else:
        # Penalización sutil estándar por jugar fuera de casa según Klement
        fuerza *= (1.0 - abs(datos["k_noise"] * 0.5))
        
    return max(0.2, fuerza / 13.0) # Protegemos que mu no sea 0 para evadir colapsos en Poisson

def engine_model_two(datos, rival_confed, es_local):
    """Modelo 2: Ajuste Alternativo No Lineal"""
    f_deportiva = (100 - datos["ranking"]) * 0.50
    pib_k = datos["pib"] / 1000
    f_economica = (pib_k * 0.18) - (0.0018 * (pib_k ** 2))
    f_demografica = np.log(max(1.0, datos["poblacion"])) * 0.25
    f_clima = -0.05 * abs(datos["temp"] - 14.0)
    
    fuerza = f_deportiva + f_economica + f_demografica + f_clima
    
    if es_local:
        # Factor adaptativo de resistencia según el continente del rival
        resistencia = 1.0 if rival_confed == "CONMEBOL" else (0.75 if rival_confed == "UEFA" else 0.55)
        fuerza *= (1.0 + (datos["m2_noise"] * (1.0 - resistencia)))
    else:
        # Mitigación del rendimiento para el plantel visitante
        fuerza *= 0.90
        
    return max(0.2, fuerza / 12.5)

def ejecutar_montecarlo(lk_a, lk_b, lg_a, lg_b, n_simulaciones=10000):
    """Ejecuta las 10,000 iteraciones estocásticas distribuidas por Poisson"""
    # Generación de vectores aleatorios usando la distribución de Poisson
    sim_k_a = stats.poisson.rvs(mu=lk_a, size=n_simulaciones)
    sim_k_b = stats.poisson.rvs(mu=lk_b, size=n_simulaciones)
    sim_g_a = stats.poisson.rvs(mu=lg_a, size=n_simulaciones)
    sim_g_b = stats.poisson.rvs(mu=lg_b, size=n_simulaciones)

    # Cálculo exacto de frecuencias relativas vectorizadas
    pk_a = float(np.sum(sim_k_a > sim_k_b) / n_simulaciones) * 100
    pk_emp = float(np.sum(sim_k_a == sim_k_b) / n_simulaciones) * 100
    pk_b = float(np.sum(sim_k_b > sim_k_a) / n_simulaciones) * 100

    pg_a = float(np.sum(sim_g_a > sim_g_b) / n_simulaciones) * 100
    pg_emp = float(np.sum(sim_g_a == sim_g_b) / n_simulaciones) * 100
    pg_b = float(np.sum(sim_g_b > sim_g_a) / n_simulaciones) * 100

    # Bucle de protección contra ceros absolutos para salvaguardar la entropía cruzada (Log Loss)
    res = {
        "pk_a": max(0.1, pk_a),
        "pk_emp": max(0.1, pk_emp),
        "pk_b": max(0.1, pk_b),
        "pg_a": max(0.1, pg_a),
        "pg_emp": max(0.1, pg_emp),
        "pg_b": max(0.1, pg_b)
    }
    
    # Normalización matemática estricta para asegurar que la suma de probabilidades sume exactamente 100%
    sum_k = res["pk_a"] + res["pk_emp"] + res["pk_b"]
    res["pk_a"] = (res["pk_a"] / sum_k) * 100
    res["pk_emp"] = (res["pk_emp"] / sum_k) * 100
    res["pk_b"] = (res["pk_b"] / sum_k) * 100

    sum_g = res["pg_a"] + res["pg_emp"] + res["pg_b"]
    res["pg_a"] = (res["pg_a"] / sum_g) * 100
    res["pg_emp"] = (res["pg_emp"] / sum_g) * 100
    res["pg_b"] = (res["pg_b"] / sum_g) * 100

    return res
