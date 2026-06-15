# app.py - Interfaz Gráfica de Usuario unificada y optimizada
import streamlit as st
import pandas as pd
import numpy as np
import data
import engines
import utils
import calibrador

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

# ──────────────────────────────────────────────
# PESTAÑA 1: MONTECARLO
# ──────────────────────────────────────────────
with tab1:
    st.subheader("🗓️ Selección de Partido desde el Fixture Oficial")

    fixture_options = [
        f"Partido {p['id']} [{p['fase']}]: {p['local']} vs. {p['visitante']}"
        for p in data.FIXTURE
    ]
    selected_match_str = st.selectbox("Elige un enfrentamiento:", fixture_options)

    try:
        match_id = int(selected_match_str.split("Partido ")[1].split(" [")[0])
        match_data = next(p for p in data.FIXTURE if p["id"] == match_id)
        team_a = match_data["local"]
        team_b = match_data["visitante"]
        fase_actual = match_data["fase"]
        a = data.TEAMS[team_a]
        b = data.TEAMS[team_b]
    except Exception as e:
        st.error(f"Error al procesar el fixture: {e}")
        st.stop()

    lk_a = engines.engine_klement(a, b["confed"], es_local=True)
    lk_b = engines.engine_klement(b, a["confed"], es_local=False)
    lg_a = engines.engine_model_two(a, b["confed"], es_local=True)
    lg_b = engines.engine_model_two(b, a["confed"], es_local=False)

    usar_calibrador = st.checkbox(
        "🔬 Activar Calibrador Bayesiano (ajusta con tendencia real del torneo)",
        value=len(st.session_state.partidos_jugados) >= 3
    )

    if st.button("🎲 Correr 10,000 Simulaciones de Montecarlo"):
        if usar_calibrador and len(st.session_state.partidos_jugados) >= 1:
            resultados = calibrador.recalcular_con_tendencia_real(
                match_id, st.session_state.partidos_jugados,
                lk_a, lk_b, lg_a, lg_b
            )
        else:
            resultados = engines.ejecutar_montecarlo(lk_a, lk_b, lg_a, lg_b)

        st.session_state.update(resultados)
        st.session_state.active_match = f"{team_a} vs. {team_b}"
        st.session_state.active_id = match_id
        st.session_state.active_fase = fase_actual

    if st.session_state.get("active_match") == f"{team_a} vs. {team_b}":
        st.markdown(f"### 📊 Probabilidades Estocásticas: *{team_a} vs. {team_b}*")
        c1, c2 = st.columns(2)
        with c1:
            st.info("📐 *Modelo 1: Joachim Klement (Econometría)*")
            st.metric(f"🏆 Victoria {team_a}", f"{st.session_state.pk_a:.1f}%")
            st.metric("🤝 Empate",              f"{st.session_state.pk_emp:.1f}%")
            st.metric(f"🏆 Victoria {team_b}", f"{st.session_state.pk_b:.1f}%")
        with c2:
            st.success("📊 *Modelo 2: Ajuste Alternativo Integrado*")
            st.metric(f"🏆 Victoria {team_a}", f"{st.session_state.pg_a:.1f}%")
            st.metric("🤝 Empate",              f"{st.session_state.pg_emp:.1f}%")
            st.metric(f"🏆 Victoria {team_b}", f"{st.session_state.pg_b:.1f}%")

        # Barra visual de probabilidades
        st.markdown("#### Distribución visual de probabilidades")
        prob_df = pd.DataFrame({
            "Resultado": [f"Victoria {team_a}", "Empate", f"Victoria {team_b}"],
            "Klement (%)": [
                round(st.session_state.pk_a, 1),
                round(st.session_state.pk_emp, 1),
                round(st.session_state.pk_b, 1)
            ],
            "Modelo 2 (%)": [
                round(st.session_state.pg_a, 1),
                round(st.session_state.pg_emp, 1),
                round(st.session_state.pg_b, 1)
            ]
        }).set_index("Resultado")
        st.bar_chart(prob_df)

# ──────────────────────────────────────────────
# PESTAÑA 2: REGISTRO REAL Y LOG LOSS
# ──────────────────────────────────────────────
with tab2:
    st.subheader("📝 Cargar Marcador Oficial de Campo")

    if "active_match" in st.session_state:
        local_name, visitante_name = st.session_state.active_match.split(" vs. ")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            goles_a = st.number_input(f"⚽ Goles de {local_name}",    min_value=0, step=1, key="g_r_a")
        with col_g2:
            goles_b = st.number_input(f"⚽ Goles de {visitante_name}", min_value=0, step=1, key="g_r_b")

        if st.button("💾 Computar Desviaciones y Log Loss"):
            y_real = 1.0 if goles_a > goles_b else (0.5 if goles_a == goles_b else 0.0)

            p_k = (
                st.session_state.pk_a  / 100 if y_real == 1.0 else
                st.session_state.pk_emp / 100 if y_real == 0.5 else
                st.session_state.pk_b  / 100
            )
            p_g = (
                st.session_state.pg_a  / 100 if y_real == 1.0 else
                st.session_state.pg_emp / 100 if y_real == 0.5 else
                st.session_state.pg_b  / 100
            )

            log_loss_k = -np.log(max(0.01, p_k))
            log_loss_g = -np.log(max(0.01, p_g))
            letra_grupo = st.session_state.active_fase.replace("Grupo ", "").strip()

            st.session_state.partidos_jugados[st.session_state.active_id] = {
                "local":    local_name,
                "visitante": visitante_name,
                "goles_l":  int(goles_a),
                "goles_v":  int(goles_b),
                "grupo":    letra_grupo,
            }
            st.session_state.audit_history.append({
                "Partido":          st.session_state.active_match,
                "Resultado":        f"{goles_a} - {goles_b}",
                "Log Loss Klement": round(log_loss_k, 3),
                "Log Loss Modelo 2": round(log_loss_g, 3),
            })

            resultado_txt = (
                f"🏆 {local_name} gana" if goles_a > goles_b else
                f"🏆 {visitante_name} gana" if goles_b > goles_a else
                "🤝 Empate"
            )
            st.success(f"¡Guardado! {local_name} {goles_a} – {goles_b} {visitante_name}  →  {resultado_txt}")
            st.info(f"Log Loss Klement: **{log_loss_k:.3f}** | Log Loss Modelo 2: **{log_loss_g:.3f}**")

    else:
        st.info("ℹ️ Primero corre una simulación en la pestaña 1.")

    st.markdown("### 📋 Historial de Auditoría de Modelos")
    if st.session_state.audit_history:
        df_audit = pd.DataFrame(st.session_state.audit_history)
        st.dataframe(df_audit, use_container_width=True)

        # Promedio global de Log Loss
        avg_k = df_audit["Log Loss Klement"].mean()
        avg_g = df_audit["Log Loss Modelo 2"].mean()
        col_a, col_b = st.columns(2)
        col_a.metric("📉 Log Loss promedio Klement", f"{avg_k:.3f}")
        col_b.metric("📉 Log Loss promedio Modelo 2", f"{avg_g:.3f}")

        mejor = "Klement" if avg_k < avg_g else "Modelo 2"
        st.success(f"✅ Modelo con menor error acumulado: **{mejor}**")
    else:
        st.info("ℹ️ Aún no hay partidos registrados.")

# ──────────────────────────────────────────────
# PESTAÑA 3: TABLAS DE POSICIONES
# ──────────────────────────────────────────────
with tab3:
    st.subheader("🏆 Posiciones Reales Actualizadas de la Fase de Grupos")

    grupos_disponibles = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    cols = st.columns(2)

    for i, g in enumerate(grupos_disponibles):
        df_grupo = utils.calcular_tabla_grupo(g, st.session_state.partidos_jugados)
        if df_grupo is not None:
            with cols[i % 2]:
                st.markdown(f"#### 🗂️ Grupo {g}")
                # Resaltar los 2 primeros (clasificados directos)
                st.dataframe(
                    df_grupo.style.apply(
                        lambda row: [
                            "background-color: #d4edda" if row.name <= 2 else
                            "background-color: #fff3cd" if row.name == 3 else ""
                        ] * len(row),
                        axis=1
                    ),
                    use_container_width=True
                )

    if not st.session_state.partidos_jugados:
        st.info("ℹ️ Las tablas se actualizarán automáticamente al registrar resultados en la pestaña 2.")
