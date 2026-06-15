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

# ==============================================================================
# INICIALIZACIÓN SEGURA Y PERSISTENTE DEL SESSION STATE
# ==============================================================================
if "audit_history" not in st.session_state:
    st.session_state.audit_history = []
if "partidos_jugados" not in st.session_state:
    st.session_state.partidos_jugados = {}
if "simulaciones_acumuladas" not in st.session_state:
    st.session_state.simulaciones_acumuladas = {}

tab1, tab2, tab3 = st.tabs([
    "📅 Calendario y Simulación de Montecarlo",
    "📊 Registro Real y Análisis de Error",
    "🏆 Tablas de Posiciones en Vivo"
])

# ==============================================================================
# --- PESTAÑA 1: MONTECARLO ---
# ==============================================================================
with tab1:
    st.subheader("🗓️ Selección de Partido desde el Fixture Oficial")
    
    # Lee dinámicamente los 72 partidos del nuevo data.py
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

    # Motores de cálculo paramétrico
    lk_a = engines.engine_klement(a, b["confed"], es_local=True)
    lk_b = engines.engine_klement(b, a["confed"], es_local=False)
    lg_a = engines.engine_model_two(a, b["confed"], es_local=True)
    lg_b = engines.engine_model_two(b, a["confed"], es_local=False)

    if st.button("🎲 Correr 10,000 Simulaciones de Montecarlo"):
        resultados = engines.ejecutar_montecarlo(lk_a, lk_b, lg_a, lg_b)
        
        # Almacenamiento persistente por ID para evitar borrados al cambiar de pestaña
        st.session_state.simulaciones_acumuladas[match_id] = {
            "match_str": f"{team_a} vs. {team_b}",
            "fase": fase_actual,
            "pk_a": resultados["pk_a"],
            "pk_emp": resultados["pk_emp"],
            "pk_b": resultados["pk_b"],
            "pg_a": resultados["pg_a"],
            "pg_emp": resultados["pg_emp"],
            "pg_b": resultados["pg_b"]
        }
        st.session_state.active_id = match_id
        st.success(f"¡Simulación completada para el Partido {match_id}!")

    # Despliegue de métricas
    if match_id in st.session_state.simulaciones_acumuladas:
        sim = st.session_state.simulaciones_acumuladas[match_id]
        st.markdown(f"### 📊 Probabilidades Estocásticas: **{team_a} vs. {team_b}**")
        c1, c2 = st.columns(2)
        with c1:
            st.info("🇪🇺 **Modelo 1: Joachim Klement (Econometría)**")
            st.metric(f"Victoria {team_a}", f"{sim['pk_a']:.1f}%")
            st.metric("Empate", f"{sim['pk_emp']:.1f}%")
            st.metric(f"Victoria {team_b}", f"{sim['pk_b']:.1f}%")
        with c2:
            st.success("📊 **Modelo Dos: Ajuste Alternativo Integrado**")
            st.metric(f"Victoria {team_a}", f"{sim['pg_a']:.1f}%")
            st.metric("Empate", f"{sim['pg_emp']:.1f}%")
            st.metric(f"Victoria {team_b}", f"{sim['pg_b']:.1f}%")
    else:
        st.warning("⚠️ No hay simulaciones en memoria para este partido. Presiona el botón de arriba.")

# ==============================================================================
# --- PESTAÑA 2: REGISTRO REAL Y ANÁLISIS DE ERROR ---
# ==============================================================================
with tab2:
    st.subheader("📝 Cargar Marcador Oficial de Campo")
    
    if "active_id" in st.session_state and st.session_state.active_id in st.session_state.simulaciones_acumuladas:
        id_activo = st.session_state.active_id
        sim_activa = st.session_state.simulaciones_acumuladas[id_activo]
        local_name, visitante_name = sim_activa["match_str"].split(" vs. ")
        
        st.caption(f"Registrando datos para el **Partido {id_activo}** ({sim_activa['fase']})")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            goles_a = st.number_input(f"Goles de {local_name}", min_value=0, step=1, key=f"g_l_{id_activo}")
        with col_g2:
            goles_b = st.number_input(f"Goles de {visitante_name}", min_value=0, step=1, key=f"g_v_{id_activo}")

        if st.button("💾 Computar Desviaciones y Log Loss"):
            y_real = 1.0 if goles_a > goles_b else (0.5 if goles_a == goles_b else 0.0)
            
            p_k = sim_activa["pk_a"]/100 if y_real==1.0 else (sim_activa["pk_emp"]/100 if y_real==0.5 else sim_activa["pk_b"]/100)
            p_g = sim_activa["pg_a"]/100 if y_real==1.0 else (sim_activa["pg_emp"]/100 if y_real==0.5 else sim_activa["pg_b"]/100)
            
            log_loss_k = -np.log(max(0.001, p_k))
            log_loss_g = -np.log(max(0.001, p_g))

            letra_grupo = sim_activa["fase"].replace("Grupo ", "").strip()
            
            # Se guarda el resultado en el estado de la sesión
            st.session_state.partidos_jugados[id_activo] = {
                "local": local_name,
                "visitante": visitante_name,
                "goles_l": goles_a,
                "goles_v": goles_b,
                "grupo": letra_grupo
            }
            
            st.session_state.audit_history.append({
                "ID": id_activo,
                "Partido": sim_activa["match_str"],
                "Resultado": f"{goles_a} - {goles_b}",
                "Log Loss Klement": round(log_loss_k, 4),
                "Log Loss Model 2": round(log_loss_g, 4)
            })
            st.success(f"✅ ¡Marcador Guardado! {local_name} {goles_a} - {goles_b} {visitante_name}.")
    else:
        st.info("💡 Por favor, ve a la pestaña 1 y corre la simulación para el partido que deseas registrar.")

    st.markdown("### 📋 Historial de Auditoría de Modelos (Control Log Loss)")
    if st.session_state.audit_history:
        st.dataframe(pd.DataFrame(st.session_state.audit_history), use_container_width=True, hide_index=True)

# ==============================================================================
# --- PESTAÑA 3: TABLAS DE POSICIONES EN VIVO ---
# ==============================================================================
with tab3:
    st.subheader("🏆 Posiciones Reales Actualizadas de la Fase de Grupos")
    grupos_disponibles = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    
    cols_vista = st.columns(3)
    for index, g in enumerate(grupos_disponibles):
        with cols_vista[index % 3]:
            with st.expander(f"📊 Tabla del Grupo {g}", expanded=True):
                df_grupo = utils.calcular_tabla_grupo(g, st.session_state.partidos_jugados)
                if df_grupo is not None and not df_grupo.empty:
                    st.dataframe(df_grupo, use_container_width=True, hide_index=True)
                else:
                    st.caption("No se han registrado partidos oficiales para este grupo.")
