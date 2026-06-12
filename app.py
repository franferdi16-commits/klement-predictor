# app.py - Interfaz Gráfica de Usuario unificada y optimizada
import streamlit as st
import pandas as pd
import numpy as np
import data
import engines
import utils

st.set_page_config(page_title="World Cup Pro Predictor 2026", page_icon="⚽", layout="wide")
st.title("⚽ World Cup Pro Predictor 2026")
st.markdown("### Consola Avanzada de Simulación No Lineal y Control Log Loss")
st.markdown("---")

# Inicialización segura del Session State
if "audit_history" not in st.session_state:
    st.session_state.audit_history = []
if "partidos_jugados" not in st.session_state:
    st.session_state.partidos_jugados = {}

tab1, tab2, tab3 = st.tabs([
    "📅 Calendario y Simulación de Montecarlo",
    "📊 Registro Real y Análisis de Error",
    "🏆 Tablas de Posiciones en Vivo"
])

# --- PESTAÑA 1: MONTECARLO ---
with tab1:
    st.subheader("🗓️ Selección de Partido desde el Fixture Oficial")
    fixture_options = [f"Partido {p['id']} [{p['fase']}]: {p['local']} vs. {p['visitante']}" for p in data.FIXTURE]
    selected_match_str = st.selectbox("Elige un enfrentamiento:", fixture_options)
    try:
        part_id_texto = selected_match_str.split("Partido ")[1]
        match_id = int(part_id_texto.split(" [")[0])
        match_data = next(p for p in data.FIXTURE if p['id'] == match_id)
        team_a, team_b, fase_actual = match_data['local'], match_data['visitante'], match_data['fase']
        a, b = data.TEAMS[team_a], data.TEAMS[team_b]
    except Exception:
        st.error("Error al procesar el mapeo del fixture. Revisa las claves de data.py.")
        st.stop()

    lk_a = engines.engine_klement(a, b["confed"], es_local=True)
    lk_b = engines.engine_klement(b, a["confed"], es_local=False)
    lg_a = engines.engine_model_two(a, b["confed"], es_local=True)
    lg_b = engines.engine_model_two(b, a["confed"], es_local=False)

    if st.button("🎲 Correr 10,000 Simulaciones de Montecarlo"):
        resultados = engines.ejecutar_montecarlo(lk_a, lk_b, lg_a, lg_b)
        st.session_state.update(resultados)
        st.session_state.active_match = f"{team_a} vs. {team_b}"
        st.session_state.active_id = match_id
        st.session_state.active_fase = fase_actual

    if "active_match" in st.session_state and st.session_state.active_match == f"{team_a} vs. {team_b}":
        st.markdown(f"### 📊 Probabilidades Estocásticas: **{team_a} vs. {team_b}**")
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

# --- PESTAÑA 2: REGISTRO REAL ---
with tab2:
    st.subheader("📝 Cargar Marcador Oficial de Campo")
    if "active_match" in st.session_state:
        local_name, visitante_name = st.session_state.active_match.split(" vs. ")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            goles_a = st.number_input(f"Goles de {local_name}", min_value=0, step=1, key="g_r_a")
        with col_g2:
            goles_b = st.number_input(f"Goles de {visitante_name}", min_value=0, step=1, key="g_r_b")

        if st.button("💾 Computar Desviaciones y Log Loss"):
            y_real = 1.0 if goles_a > goles_b else (0.5 if goles_a == goles_b else 0.0)
            p_k = st.session_state.pk_a/100 if y_real==1.0 else (st.session_state.pk_emp/100 if y_real==0.5 else st.session_state.pk_b/100)
            p_g = st.session_state.pg_a/100 if y_real==1.0 else (st.session_state.pg_emp/100 if y_real==0.5 else st.session_state.pg_b/100)
            log_loss_k = -np.log(max(0.01, p_k))
            log_loss_g = -np.log(max(0.01, p_g))

            letra_grupo = st.session_state.active_fase.replace("Grupo ", "").strip()
            st.session_state.partidos_jugados[st.session_state.active_id] = {
                "local": local_name,
                "visitante": visitante_name,
                "goles_l": goles_a,
                "goles_v": goles_b,
                "grupo": letra_grupo
            }
            st.session_state.audit_history.append({
                "Partido": st.session_state.active_match,
                "Resultado": f"{goles_a} - {goles_b}",
                "Log Loss Klement": round(log_loss_k, 3),
                "Log Loss Model 2": round(log_loss_g, 3)
            })
            st.success(f"¡Marcador Guardado! {local_name} {goles_a} - {goles_b} {visitante_name}.")
    else:
        st.info("Primero corre una simulación en la pestaña 1.")

    st.markdown("### 📋 Historial de Auditoría de Modelos")
    if st.session_state.audit_history:
        st.dataframe(pd.DataFrame(st.session_state.audit_history), use_container_width=True)

# --- PESTAÑA 3: TABLAS DE POSICIONES ---
with tab3:
    st.subheader("🏆 Posiciones Reales Actualizadas de la Fase de Grupos")
    grupos_disponibles = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    for g in grupos_disponibles:
        df_grupo = utils.calcular_tabla_grupo(g, st.session_state.partidos_jugados)
        if df_grupo is not None:
            st.write(f"#### **Grupo {g}**")
            st.table(df_grupo)
