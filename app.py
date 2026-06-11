import streamlit as st
import numpy as np
import scipy.stats as stats
import data

st.set_page_config(page_title="World Cup Pro Predictor 2026", page_icon="⚽", layout="wide")

st.title("⚽ World Cup Pro Predictor 2026")
st.markdown("### Consola Avanzada de Simulación No Lineal y Control Log Loss")
st.markdown("---")

# Verificar persistencia de datos de sesión
if "audit_history" not in st.session_state:
    st.session_state.audit_history = []

tab1, tab2 = st.tabs(["📅 Calendario y Simulación de Montecarlo", "📊 Registro Real y Análisis de Error"])

with tab1:
    st.subheader("🗓️ Selección de Partido desde el Fixture")
    fixture_options = [f"Partido {p['id']} [Grupo {p['grupo']}]: {p['local']} vs. {p['visitante']}" for p in data.FIXTURE]
    selected_match_str = st.selectbox("Elige un enfrentamiento:", fixture_options)
    
    try:
        match_id = int(selected_match_str.split(" ")[1].replace("[", ""))
        match_data = next(p for p in data.FIXTURE if p['id'] == match_id)
        
        team_a = match_data['local']
        team_b = match_data['visitante']
        
        a = data.TEAMS[team_a]
        b = data.TEAMS[team_b]
    except Exception as e:
        st.error("Error al procesar el mapeo del fixture. Verifica el archivo data.py.")
        st.stop()

    # --- MATEMÁTICAS MOTOR 1: KLEMENT ---
    def engine_klement(datos, rival_confed, es_local):
        f_deportiva = (100 - datos["ranking"]) * 0.40
        pib_k = datos["pib"] / 1000
        f_economica = (pib_k * 0.15) - (0.0015 * (pib_k ** 2))
        f_demografica = np.log(datos["poblacion"]) * 0.20
        f_clima = -0.08 * abs(datos["temp"] - 14.0)
        fuerza = f_deportiva + f_economica + f_demografica + f_clima + (-0.6 if datos["campeon"] else 0.0)
        if es_local: fuerza *= (1.0 + datos["k_noise"])
        return max(0.5, fuerza / 13.0)

    # --- MATEMÁTICAS MOTOR 2: MODELO DOS ---
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

    if st.button("🎲 Correr 10,000 Simulaciones"):
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

    if "active_match" in st.session_state and st.session_state.active_match == f"{team_a} vs. {team_b}":
        st.markdown(f"### 📊 Resultados de Simulación: **{team_a} vs. {team_b}**")
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

with tab2:
    st.subheader("📝 Cargar Marcador Oficial de Campo")
    if "active_match" in st.session_state:
        t_split = st.session_state.active_match.split(" vs. ")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            goles_a = st.number_input(f"Goles de {t_split[0]}", min_value=0, step=1, key="g_real_a")
        with col_g2:
            goles_b = st.number_input(f"Goles de {t_split[1]}", min_value=0, step=1, key="g_real_b")
            
        if st.button("💾 Computar Desviaciones y Log Loss"):
            if goles_a > goles_b: y_real = 1.0
            elif goles_a == goles_b: y_real = 0.5
            else: y_real = 0.0

            p_k = st.session_state.pk_a/100 if y_real==1.0 else (st.session_state.pk_emp/100 if y_real==0.5 else st.session_state.pk_b/100)
            p_g = st.session_state.pg_a/100 if y_real==1.0 else (st.session_state.pg_emp/100 if y_real==0.5 else st.session_state.pg_b/100)

            log_loss_k = -np.log(max(0.01, p_k))
            log_loss_g = -np.log(max(0.01, p_g))

            st.session_state.audit_history.append({
                "Partido": st.session_state.active_match,
                "Resultado Real": f"{goles_a} - {goles_b}",
                "Log Loss Klement": round(log_loss_k, 3),
                "Log Loss Modelo 2": round(log_loss_g, 3)
            })
            st.success("¡Cuadro de auditoría actualizado!")

    if st.session_state.audit_history:
        st.markdown("---")
        st.subheader("📈 Historial de Pérdida Logarítmica Acumulada")
        st.dataframe(st.session_state.audit_history, use_container_width=True)
        mean_k = np.mean([x["Log Loss Klement"] for x in st.session_state.audit_history])
        mean_g = np.mean([x["Log Loss Modelo 2"] for x in st.session_state.audit_history])
        st.info(f"💡 **Evaluación:** El error promedio más bajo gana. -> **Klement: {mean_k:.3f}** | **Modelo Dos: {mean_g:.3f}**")
    else:
        st.info("No hay registros guardados en esta sesión. Ejecuta una simulación en la pestaña 1 para habilitar el registro.")
