import streamlit as st
import numpy as np
import scipy.stats as stats

# Configuración de la interfaz
st.set_page_config(
    page_title="Klement vs. Garratón Predictor", 
    page_icon="📊", 
    layout="centered"
)

st.title("📊 Simulador de Doble Motor Estadístico")
st.markdown("""
### ¿Quién lee mejor el fútbol? ¿La banca europea o la garra sudamericana?
Esta aplicación corre **10,000 simulaciones de Montecarlo** en paralelo usando dos lógicas matemáticas distintas.
""")

# Base de datos unificada con variables para ambos modelos
teams_data = {
    "México": {"ranking": 15, "pib": 11000, "temp": 21.0, "poblacion": 128.5, "confed": "CONCACAF", "campeon_defensor": False, "bullicio_klement": -0.15, "bullicio_garraton": 0.4},
    "Corea del Sur": {"ranking": 22, "pib": 32000, "temp": 12.5, "poblacion": 51.7, "confed": "AFC", "campeon_defensor": False, "bullicio_klement": 0.10, "bullicio_garraton": 0.1},
    "Chequia": {"ranking": 36, "pib": 27000, "temp": 8.0, "poblacion": 10.8, "confed": "UEFA", "campeon_defensor": False, "bullicio_klement": 0.15, "bullicio_garraton": 0.15},
    "Sudáfrica": {"ranking": 59, "pib": 6000, "temp": 17.5, "poblacion": 60.6, "confed": "CAF", "campeon_defensor": False, "bullicio_klement": 0.10, "bullicio_garraton": 0.2},
    "Argentina": {"ranking": 1, "pib": 13000, "temp": 14.0, "poblacion": 46.2, "confed": "CONMEBOL", "campeon_defensor": True, "bullicio_klement": 0.40, "bullicio_garraton": 0.5},
    "Países Bajos": {"ranking": 7, "pib": 62000, "temp": 10.0, "poblacion": 18.0, "confed": "UEFA", "campeon_defensor": False, "bullicio_klement": 0.20, "bullicio_garraton": 0.2},
    "Portugal": {"ranking": 6, "pib": 26000, "temp": 15.5, "poblacion": 10.4, "confed": "UEFA", "campeon_defensor": False, "bullicio_klement": 0.25, "bullicio_garraton": 0.25},
    "Francia": {"ranking": 2, "pib": 45000, "temp": 11.0, "poblacion": 68.0, "confed": "UEFA", "campeon_defensor": False, "bullicio_klement": 0.30, "bullicio_garraton": 0.3},
    "España": {"ranking": 3, "pib": 32000, "temp": 14.5, "poblacion": 48.0, "confed": "UEFA", "campeon_defensor": False, "bullicio_klement": 0.30, "bullicio_garraton": 0.3},
    "Brasil": {"ranking": 5, "pib": 10000, "temp": 25.0, "poblacion": 215.3, "confed": "CONMEBOL", "campeon_defensor": False, "bullicio_klement": 0.40, "bullicio_garraton": 0.45},
    "Estados Unidos": {"ranking": 11, "pib": 80000, "temp": 12.0, "poblacion": 334.9, "confed": "CONCACAF", "campeon_defensor": False, "bullicio_klement": 0.20, "bullicio_garraton": 0.2}
}

st.subheader("⚽ Configurar Enfrentamiento de la Jornada")
col1, col2 = st.columns(2)
with col1:
    team_a = st.selectbox("Selección A (Local)", list(teams_data.keys()), index=0)
with col2:
    team_b = st.selectbox("Selección B (Visitante)", list(teams_data.keys()), index=1)

if team_a == team_b:
    st.error("⚠️ Selecciona dos equipos distintos.")
else:
    a = teams_data[team_a]
    b = teams_data[team_b]

    # --- FUNCIÓN MOTOR 1: REPLICACIÓN KLEMENT ---
    def engine_klement(datos, rival_confed, es_local):
        f_deportiva = (100 - datos["ranking"]) * 0.40
        pib_k = datos["pib"] / 1000
        f_economica = (pib_k * 0.15) - (0.0015 * (pib_k ** 2))
        f_demografica = np.log(datos["poblacion"]) * 0.20
        f_clima = -0.08 * abs(datos["temp"] - 14.0)
        f_campeon = -0.6 if datos["campeon_defensor"] else 0.0
        
        fuerza_base = f_deportiva + f_economica + f_demografica + f_clima + f_campeon
        if es_local:
            # Klement puro: El bullicio puede ser negativo si el anfitrión se congela
            fuerza_base *= (1.0 + datos["bullicio_klement"])
        return max(0.5, fuerza_base / 13.0)

    # --- FUNCIÓN MOTOR 2: AJUSTE GARRATÓN (NUESTRO) ---
    def engine_garraton(datos, rival_confed, es_local):
        f_deportiva = (100 - datos["ranking"]) * 0.50
        pib_k = datos["pib"] / 1000
        f_economica = (pib_k * 0.18) - (0.0018 * (pib_k ** 2))
        f_demografica = np.log(datos["poblacion"]) * 0.25
        f_clima = -0.05 * abs(datos["temp"] - 14.0)
        
        fuerza_base = f_deportiva + f_economica + f_demografica + f_clima
        if es_local:
            resistencia_rival = 1.0 if rival_confed == "CONMEBOL" else (0.75 if rival_confed == "UEFA" else 0.55)
            factor_presion = datos["bullicio_garraton"] * (1.0 - resistencia_rival)
            fuerza_base *= (1.0 + factor_presion)
        return max(0.5, fuerza_base / 12.5)

    if st.button("🚀 Ejecutar Comparación de Modelos"):
        # Ejecución simultánea de simulaciones de Poisson
        # Motor Klement
        lk_a = engine_klement(a, b["confed"], es_local=True)
        lk_b = engine_klement(b, a["confed"], es_local=False)
        sim_k_a = stats.poisson.rvs(mu=lk_a, size=10000)
        sim_k_b = stats.poisson.rvs(mu=lk_b, size=10000)
        
        # Motor Nuestro (Garratón)
        lg_a = engine_garraton(a, b["confed"], es_local=True)
        lg_b = engine_garraton(b, a["confed"], es_local=False)
        sim_g_a = stats.poisson.rvs(mu=lg_a, size=10000)
        sim_g_b = stats.poisson.rvs(mu=lg_b, size=10000)

        # Cálculos de porcentajes
        pk_a = (np.sum(sim_k_a > sim_k_b) / 10000) * 100
        pk_emp = (np.sum(sim_k_a == sim_k_b) / 10000) * 100
        pk_b = (np.sum(sim_k_b > sim_k_a) / 10000) * 100

        pg_a = (np.sum(sim_g_a > sim_g_b) / 10000) * 100
        pg_emp = (np.sum(sim_g_a == sim_g_b) / 10000) * 100
        pg_b = (np.sum(sim_g_b > sim_g_a) / 10000) * 100

        # Bloque Visual 1: Klement Puro
        st.subheader("🇪🇺 Modelo 1: Predicción Joachim Klement (Econometría)")
        c1, c2, c3 = st.columns(3)
        c1.metric(f"Gana {team_a}", f"{pk_a:.1f}%")
        c2.metric("Empate", f"{pk_emp:.1f}%")
        c3.metric(f"Gana {team_b}", f"{pk_b:.1f}%")

        # Bloque Visual 2: Nuestro Algoritmo
        st.subheader(" Latinoamericano: Modelo Garratón (Ajuste Cultural)")
        c4, c5, c6 = st.columns(3)
        c4.metric(f"Gana {team_a}", f"{pg_a:.1f}%")
        c5.metric("Empate", f"{pg_emp:.1f}%")
        c6.metric(f"Gana {team_b}", f"{pg_b:.1f}%")
