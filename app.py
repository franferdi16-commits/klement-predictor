import streamlit as st
import numpy as np
import scipy.stats as stats
import pandas as pd
import data

st.set_page_config(page_title="World Cup Pro Predictor 2026", page_icon="⚽", layout="wide")
st.title("⚽ World Cup Pro Predictor 2026")
st.markdown("### Consola Avanzada de Simulación No Lineal y Control Log Loss")
st.markdown("---")

# Inicialización segura de variables globales de sesión
if "audit_history" not in st.session_state:
    st.session_state.audit_history = []
if "partidos_jugados" not in st.session_state:
    st.session_state.partidos_jugados = {}

# Creación de las tres pestañas de trabajo
tab1, tab2, tab3 = st.tabs([
    "📅 Calendario y Simulación de Montecarlo",
    "📊 Registro Real y Análisis de Error",
    "🏆 Tablas de Posiciones en Vivo"
])

# --- PESTAÑA 1: SIMULACIÓN ---
with tab1:
    st.subheader("🗓️ Selección de Partido desde el Fixture Oficial")
    # Generar opciones legibles para el selectbox
    fixture_options = [f"Partido {p['id']} [{p['fase']}]: {p['local']} vs. {p['visitante']}" for p in data.FIXTURE]
    selected_match_str = st.selectbox("Elige un enfrentamiento:", fixture_options)
    try:
        # Extracción segura del ID numérico del partido
        part_id_texto = selected_match_str.split("Partido ")[1]
        match_id = int(part_id_texto.split(" [")[0])
        # Buscar datos del partido seleccionado en data.py
        match_data = next(p for p in data.FIXTURE if p['id'] == match_id)
        team_a = match_data['local']
        team_b = match_data['visitante']
        fase_actual = match_data['fase']
        a = data.TEAMS[team_a]
        b = data.TEAMS[team_b]
    except Exception as e:
        st.error("Error al procesar el mapeo del fixture. Revisa las claves de data.py.")
        st.stop()

    # --- MATEMÁTICAS MOTOR 1: KLEMENT (Econometría) ---
    def engine_klement(datos, rival_confed, es_local):
        f_deportiva = (100 - datos["ranking"]) * 0.40
        pib_k = datos["pib"] / 1000
        f_economica = (pib_k * 0.15) - (0.0015 * (pib_k ** 2))
        f_demografica = np.log(datos["poblacion"]) * 0.20
        f_clima = -0.08 * abs(datos["temp"] - 14.0)
        fuerza = f_deportiva + f_economica + f_demografica + f_clima + (-0.6 if datos["campeon"] else 0.0)
        if es_local:
            fuerza *= (1.0 + datos["k_noise"])
        return max(0.5, fuerza / 13.0)

    # --- MATEMÁTICAS MOTOR 2: MODELO DOS (Ajuste Alternativo) ---
    def engine_model_two(datos, rival_confed, es_local):
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

    lk_a = engine_klement(a, b["confed"], es_local=True)
    lk_b = engine_klement(b, a["confed"], es_local=False)
    lg_a = engine_model_two(a, b["confed"], es_local=True)
    lg_b = engine_model_two(b, a["confed"], es_local=False)

    if st.button("🎲 Correr 10,000 Simulaciones de Montecarlo"):
        sim_k_a = stats.poisson.rvs(mu=lk_a, size=10000)
        sim_k_b = stats.poisson.rvs(mu=lk_b, size=10000)
        sim_g_a = stats.poisson.rvs(mu=lg_a, size=10000)
        sim_g_b = stats.poisson.rvs(mu=lg_b, size=10000)
        st.session_state.pk_a = float(np.sum(sim_k_a > sim_k_b) / 100)
        st.session_state.pk_emp = float(np.sum(sim_k_a == sim_k_b) / 100)
        st.session_state.pk_b = float(np.sum(sim_k_b > sim_k_a) / 100)
        st.session_state.pg_a = float(np.sum(sim_g_a > sim_g_b) / 100)
        st.session_state.pg_emp = float(np.sum(sim_g_a == sim_g_b) / 100)
        st.session_state.pg_b = float(np.sum(sim_g_b > sim_g_a) / 100)
        st.session_state.active_match = f"{team_a} vs. {team_b}"
        st.session_state.active_id = match_id
        st.session_state.active_fase = fase_actual

    if "active_match" in st.session_state and st.session_state.active_match == f"{team_a} vs. {team_b}":
        st.markdown(f"### 📊 Probabilidades de Distribución Estocástica: **{team_a} vs. {team_b}**")
        c1, c2 = st.columns(2)
        with c1:
            st.info("🇪🇺 **Modelo 1: Joachim Klement (Econometría)**")
            st.metric(f"Victoria {team_a}", f"{st.session_state.pk_a:.1f}%")
            st.metric("Empate", f"{st.session_state.pk_emp:.1f}%")
            st.metric(f"Victoria {team_b}", f"{st.session_state.pk_b:.1f}%")
        with c2:
            st.success("📊 **Modelo Dos: Ajuste Alternativo Integrado**")
            st.metric(f"Victoria {team_a}", f"{st.session_state.pg_a:.1f}%")
            st.metric("Empate", f"{st.session_state.pg_emp:.1f}%")
            st.metric(f"Victoria {team_b}", f"{st.session_state.pg_b:.1f}%")

# --- PESTAÑA 2: REGISTRO REAL Y ANÁLISIS DE ERROR ---
with tab2:
    st.subheader("📝 Cargar Marcador Oficial de Campo")
    if "active_match" in st.session_state:
        t_split = st.session_state.active_match.split(" vs. ")
        local_name = t_split[0]
        visitante_name = t_split[1]
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            goles_a = st.number_input(f"Goles Regulares de {local_name}", min_value=0, step=1, key="g_r_a")
        with col_g2:
            goles_b = st.number_input(f"Goles Regulares de {visitante_name}", min_value=0, step=1, key="g_r_b")

        # Parámetros condicionales para prórroga y penales en llaves eliminatorias
        es_eliminatoria = "Grupo" not in st.session_state.active_fase
        goles_ee_a, goles_ee_b = 0, 0
        pen_a, pen_b = 0, 0
        hubo_prorroga = False

        if es_eliminatoria and (goles_a == goles_b):
            st.warning("⚠️ Empate en Fase Eliminatoria. Se requieren instancias adicionales.")
            hubo_prorroga = st.checkbox("¿Se jugó tiempo extra prórroga?")
            if hubo_prorroga:
                c_ex1, c_ex2 = st.columns(2)
                with c_ex1:
                    goles_ee_a = st.number_input(f"Goles en Prórroga de {local_name}", min_value=0, step=1)
                with c_ex2:
                    goles_ee_b = st.number_input(f"Goles en Prórroga de {visitante_name}", min_value=0, step=1)
                if (goles_a + goles_ee_a) == (goles_b + goles_ee_b):
                    st.error("🥅 Empate persistente. Definición obligatoria por Penales.")
                    c_p1, c_p2 = st.columns(2)
                    with c_p1:
                        pen_a = st.number_input(f"Penales Anotados por {local_name}", min_value=0, step=1)
                    with c_p2: pen_b =
