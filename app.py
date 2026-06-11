import streamlit as st
import numpy as np
import scipy.stats as stats

# 1. Configuración de la interfaz
st.set_page_config(
    page_title="Klement Open Source Predictor", 
    page_icon="📊", 
    layout="centered"
)

st.title("📊 Klement Open Source Predictor")
st.markdown("""
### ¡Democratizando la Econometría Deportiva!
Esta es una réplica de código abierto inspirada en el modelo estadístico de **Joachim Klement**. 
Cruza variables macroeconómicas, demográficas, climáticas y deportivas para calcular probabilidades reales.
""")

# 2. Base de datos con las variables estructurales reales
teams_data = {
    "Países Bajos": {"ranking": 7, "pib": 62000, "temp": 10.0, "poblacion": 18.0, "confed": "UEFA", "campeon_defensor": False, "bullicio": 0.2},
    "Portugal": {"ranking": 6, "pib": 26000, "temp": 15.5, "poblacion": 10.4, "confed": "UEFA", "campeon_defensor": False, "bullicio": 0.25},
    "Argentina": {"ranking": 1, "pib": 13000, "temp": 14.0, "poblacion": 46.2, "confed": "CONMEBOL", "campeon_defensor": True, "bullicio": 0.5},
    "Francia": {"ranking": 2, "pib": 45000, "temp": 11.0, "poblacion": 68.0, "confed": "UEFA", "campeon_defensor": False, "bullicio": 0.3},
    "España": {"ranking": 3, "pib": 32000, "temp": 14.5, "poblacion": 48.0, "confed": "UEFA", "campeon_defensor": False, "bullicio": 0.3},
    "Brasil": {"ranking": 5, "pib": 10000, "temp": 25.0, "poblacion": 215.3, "confed": "CONMEBOL", "campeon_defensor": False, "bullicio": 0.45},
    "México": {"ranking": 15, "pib": 11000, "temp": 21.0, "poblacion": 128.5, "confed": "CONACCACAF", "campeon_defensor": False, "bullicio": 0.4},
    "Estados Unidos": {"ranking": 11, "pib": 80000, "temp": 12.0, "poblacion": 334.9, "confed": "CONCACAF", "campeon_defensor": False, "bullicio": 0.2},
    "Japón": {"ranking": 18, "pib": 34000, "temp": 11.5, "poblacion": 125.1, "confed": "AFC", "campeon_defensor": False, "bullicio": 0.15},
    "Marruecos": {"ranking": 13, "pib": 4000, "temp": 17.5, "poblacion": 37.5, "confed": "CAF", "campeon_defensor": False, "bullicio": 0.35},
    "Sudáfrica": {"ranking": 59, "pib": 6000, "temp": 17.5, "poblacion": 60.6, "confed": "CAF", "campeon_defensor": False, "bullicio": 0.2}
}

# 3. Selectores de equipos
st.subheader("⚽ Configurar el Enfrentamiento")
col1, col2 = st.columns(2)

with col1:
    team_a = st.selectbox("Selección A (Local en simulación)", list(teams_data.keys()), index=2) # Argentina por defecto
with col2:
    team_b = st.selectbox("Selección B (Visitante en simulación)", list(teams_data.keys()), index=0) # Países Bajos por defecto

if team_a == team_b:
    st.error("⚠️ Debes seleccionar dos equipos diferentes para la simulación.")
else:
    a = teams_data[team_a]
    b = teams_data[team_b]
    
    # 4. Motor Algorítmico No Lineal
    def calcular_fuerza_efectiva(datos, rival_confed, es_local):
        # Variable Deportiva (Ranking FIFA)
        f_deportiva = (100 - datos["ranking"]) * 0.50
        
        # Curva Parabólica del PIB (La riqueza extrema disminuye el 'hambre de gloria')
        pib_k = datos["pib"] / 1000
        f_economica = (pib_k * 0.18) - (0.0018 * (pib_k ** 2))
        
        # Factor Demográfico (Masa crítica de talento en escala logarítmica)
        f_demografica = np.log(datos["poblacion"]) * 0.25
        
        # Penalización Climática (Desviación absoluta de la temperatura biológica óptima de 14°C)
        desviacion_termica = abs(datos["temp"] - 14.0)
        f_clima = -0.08 * desviacion_termica
        
        # Regresión Histórica del Campeón Defensor (Efecto saturación de éxito)
        f_campeon = -0.6 if datos["campeon_defensor"] else 0.0
        
        # Sumatoria de fuerza base estructural
        fuerza_base = f_deportiva + f_economica + f_demografica + f_clima + f_campeon
        
        # Modificador dinámico de localía y resistencia psicológica (Efecto Libertadores)
        if es_local:
            resistencia_rival = 1.0 if rival_confed == "CONMEBOL" else (0.75 if rival_confed == "UEFA" else 0.55)
            factor_presion_neta = datos["bullicio"] * (1.0 - resistencia_rival)
            fuerza_final = fuerza_base * (1.0 + factor_presion_neta)
        else:
            fuerza_final = fuerza_base
            
        return max(0.5, fuerza_final / 12.5) # Escala para tasa de goles (Lambda)

    # Calcular los parámetros Lambda para la distribución de Poisson
    lambda_a = calcular_fuerza_efectiva(a, b["confed"], es_local=True)
    lambda_b = calcular_fuerza_efectiva(b, a["confed"], es_local=False)
    
    # 5. Botón de ejecución y simulación de Montecarlo
    if st.button("🚀 Ejecutar 10,000 Simulaciones Estadísticas"):
        # Generar muestras aleatorias independientes basadas en la fuerza calculada
        sim_a = stats.poisson.rvs(mu=lambda_a, size=10000)
        sim_b = stats.poisson.rvs(mu=lambda_b, size=10000)
        
        # Calcular los porcentajes de éxito de las 10,000 iteraciones
        p_a = (np.sum(sim_a > sim_b) / 10000) * 100
        p_emp = (np.sum(sim_a == sim_b) / 10000) * 100
        p_b = (np.sum(sim_b > sim_a) / 10000) * 100
        
        # Mostrar métricas en columnas estéticas
        st.success("### 🎯 Resultados del Modelo Predictivo")
        c1, c2, c3 = st.columns(3)
        c1.metric(f"Victoria {team_a}", f"{p_a:.1f}%")
        c2.metric("Empate Técnico", f"{p_emp:.1f}%")
        c3.metric(f"Victoria {team_b}", f"{p_b:.1f}%")
        
        # 6. Bloque de auditoría transparente de datos macroeconómicos
        st.markdown("---")
        st.subheader("🔍 Desglose de Auditoría Econométrica")
        
        # Análisis cualitativo de la localía
        res_b_val = 1.0 if b["confed"] == "CONMEBOL" else (0.75 if b["confed"] == "UEFA" else 0.55)
        presion_ejercida = a["bullicio"] * (1.0 - res_b_val)
        
        st.write(f"* **{team_a} (Local)**: Desviación térmica de **{abs(a['temp']-14):.1f}°C** respecto al óptimo. Su beneficio por localía se ajustó a **+{presion_ejercida*100:.1f}%** debido a que la resistencia de la confederación de su rival ({b['confed']}) es del **{res_b_val*100:.0f}%**.")
        st.write(f"* **{team_b} (Visitante)**: Desviación térmica de **{abs(b['temp']-14):.1f}°C**. Su rendimiento se calcula puramente sobre su infraestructura de PIB (${b['pib']:,} USD) y ranking deportivo.")
        
        if a["campeon_defensor"] or b["campeon_defensor"]:
            st.warning("⚠️ Nota del modelo: El Campeón Defensor acarrea una penalización automática en su fuerza base por regresión histórica de rendimiento.")