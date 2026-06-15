# app.py - World Cup Pro Predictor 2026 - Motor Fusionado v2.0
import streamlit as st
import pandas as pd
import numpy as np
import data
import engines
import utils
import calibrador

st.set_page_config(
    page_title="World Cup Pro Predictor 2026",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ World Cup Pro Predictor 2026")
st.markdown("### Motor Fusionado Klement + M2 · Ponderación Dinámica por Log Loss · Marcador Probable")
st.markdown("---")

# ── Session State ──
if "audit_history"    not in st.session_state: st.session_state.audit_history    = []
if "partidos_jugados" not in st.session_state: st.session_state.partidos_jugados = {}

tab1, tab2, tab3 = st.tabs([
    "📅 Simulación y Marcador Probable",
    "📊 Registro Real y Log Loss",
    "🏆 Tablas de Posiciones en Vivo",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SIMULACIÓN FUSIONADA + MARCADOR
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("🗓️ Fixture Oficial — Selección de Partido")

    fixture_options = [
        f"Partido {p['id']} [{p['fase']}]: {p['local']} vs. {p['visitante']}"
        for p in data.FIXTURE
    ]
    selected = st.selectbox("Elige un enfrentamiento:", fixture_options)

    try:
        match_id  = int(selected.split("Partido ")[1].split(" [")[0])
        match_data = next(p for p in data.FIXTURE if p["id"] == match_id)
        team_a, team_b = match_data["local"], match_data["visitante"]
        fase_actual    = match_data["fase"]
        a, b           = data.TEAMS[team_a], data.TEAMS[team_b]
    except Exception as e:
        st.error(f"Error al leer el fixture: {e}")
        st.stop()

    lk_a = engines.engine_klement(a, b["confed"], es_local=True)
    lk_b = engines.engine_klement(b, a["confed"], es_local=False)
    lg_a = engines.engine_model_two(a, b["confed"], es_local=True)
    lg_b = engines.engine_model_two(b, a["confed"], es_local=False)

    usar_calibrador = st.checkbox(
        "🔬 Activar Calibrador Bayesiano (requiere ≥1 partido registrado)",
        value=len(st.session_state.partidos_jugados) >= 1,
    )

    if st.button("🎲 Correr 10,000 Simulaciones — Motor Fusionado"):
        if usar_calibrador and len(st.session_state.partidos_jugados) >= 1:
            base = calibrador.recalcular_con_tendencia_real(
                match_id, st.session_state.partidos_jugados,
                lk_a, lk_b, lg_a, lg_b,
            )
            # Sobreescribir lambdas con los calibrados antes de fusionar
            lk_a2 = base["pk_a"] / 100 * (lk_a + lg_a)
            lk_b2 = base["pk_b"] / 100 * (lk_b + lg_b)
            lg_a2 = base["pg_a"] / 100 * (lk_a + lg_a)
            lg_b2 = base["pg_b"] / 100 * (lk_b + lg_b)
        else:
            lk_a2, lk_b2, lg_a2, lg_b2 = lk_a, lk_b, lg_a, lg_b

        import inspect
        _mc_params = inspect.signature(engines.ejecutar_montecarlo).parameters
        if "audit_history" in _mc_params:
            res = engines.ejecutar_montecarlo(
                lk_a2, lk_b2, lg_a2, lg_b2,
                audit_history=st.session_state.audit_history,
            )
        else:
            # engines.py viejo: fusión manual aquí
            res_raw = engines.ejecutar_montecarlo(lk_a2, lk_b2, lg_a2, lg_b2)
            import scipy.stats as _stats
            from collections import Counter as _Counter
            import numpy as _np
            _n = 10000
            _mu_a = 0.5 * lk_a2 + 0.5 * lg_a2
            _mu_b = 0.5 * lk_b2 + 0.5 * lg_b2
            _sa = _stats.poisson.rvs(mu=_mu_a, size=_n)
            _sb = _stats.poisson.rvs(mu=_mu_b, size=_n)
            _pf_a   = float(_np.sum(_sa > _sb) / _n) * 100
            _pf_emp = float(_np.sum(_sa == _sb) / _n) * 100
            _pf_b   = float(_np.sum(_sb > _sa) / _n) * 100
            _s = _pf_a + _pf_emp + _pf_b
            _top5 = _Counter(zip(_sa.tolist(), _sb.tolist())).most_common(5)
            res = {
                **res_raw,
                "pf_a":   (_pf_a / _s) * 100,
                "pf_emp": (_pf_emp / _s) * 100,
                "pf_b":   (_pf_b / _s) * 100,
                "w_k": 50.0, "w_g": 50.0,
                "mu_a": round(_mu_a, 3), "mu_b": round(_mu_b, 3),
                "marcador_prob":   _top5[0][0],
                "marcador_prob_p": round(_top5[0][1] / _n * 100, 1),
                "top5_marcadores": _top5,
            }
        st.session_state.update(res)
        st.session_state.active_match = f"{team_a} vs. {team_b}"
        st.session_state.active_id    = match_id
        st.session_state.active_fase  = fase_actual

    # ── Resultados ──
    if st.session_state.get("active_match") == f"{team_a} vs. {team_b}":
        s = st.session_state

        # Pesos actuales
        st.markdown(
            f"**Pesos del motor fusionado →** "
            f"Klement: `{s.w_k}%` | Modelo 2: `{s.w_g}%` "
            f"&nbsp;·&nbsp; λ {team_a}: `{s.mu_a}` | λ {team_b}: `{s.mu_b}`"
        )
        st.markdown("---")

        # ── Probabilidades fusionadas ──
        col1, col2, col3 = st.columns(3)
        resultado_pred = (
            f"🏆 Gana {team_a}" if s.pf_a > s.pf_b and s.pf_a > s.pf_emp else
            f"🏆 Gana {team_b}" if s.pf_b > s.pf_a and s.pf_b > s.pf_emp else
            "🤝 Empate"
        )
        col1.metric(f"🏆 Victoria {team_a}", f"{s.pf_a:.1f}%")
        col2.metric("🤝 Empate",              f"{s.pf_emp:.1f}%")
        col3.metric(f"🏆 Victoria {team_b}", f"{s.pf_b:.1f}%")
        st.success(f"**Resultado predicho: {resultado_pred}**")

        # ── Marcador probable ──
        st.markdown("### 🎯 Marcador Más Probable")
        mg_a, mg_b = s.marcador_prob
        mc1, mc2, mc3 = st.columns([2, 1, 2])
        mc1.metric(team_a, str(mg_a))
        mc2.markdown("<h2 style='text-align:center;margin-top:20px'>—</h2>", unsafe_allow_html=True)
        mc3.metric(team_b, str(mg_b))
        st.caption(f"Frecuencia en simulaciones: **{s.marcador_prob_p:.1f}%** de 10,000 iteraciones")

        # ── Top 5 marcadores ──
        st.markdown("#### 📋 Top 5 Marcadores Más Frecuentes")
        top5_data = []
        for (ga, gb), freq in s.top5_marcadores:
            pct = freq / 10000 * 100
            res_txt = f"Gana {team_a}" if ga > gb else (f"Gana {team_b}" if gb > ga else "Empate")
            top5_data.append({
                "Marcador": f"{team_a} {ga} – {gb} {team_b}",
                "Resultado": res_txt,
                "Frecuencia": freq,
                "Probabilidad": f"{pct:.1f}%",
            })
        st.table(pd.DataFrame(top5_data))

        # ── Barra visual G/E/P ──
        st.markdown("#### Distribución G / E / P (Motor Fusionado)")
        bdf = pd.DataFrame({
            "Resultado": [f"Victoria {team_a}", "Empate", f"Victoria {team_b}"],
            "Probabilidad (%)": [round(s.pf_a, 1), round(s.pf_emp, 1), round(s.pf_b, 1)],
        }).set_index("Resultado")
        st.bar_chart(bdf)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REGISTRO REAL Y LOG LOSS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("📝 Cargar Marcador Real del Partido")

    if "active_match" in st.session_state:
        local_name, visitante_name = st.session_state.active_match.split(" vs. ")
        cg1, cg2 = st.columns(2)
        with cg1:
            goles_a = st.number_input(f"⚽ Goles {local_name}",    min_value=0, step=1, key="g_r_a")
        with cg2:
            goles_b = st.number_input(f"⚽ Goles {visitante_name}", min_value=0, step=1, key="g_r_b")

        if st.button("💾 Registrar y Calcular Log Loss"):
            s = st.session_state
            y_real = 1.0 if goles_a > goles_b else (0.5 if goles_a == goles_b else 0.0)

            p_k = s.pk_a/100 if y_real==1.0 else (s.pk_emp/100 if y_real==0.5 else s.pk_b/100)
            p_g = s.pg_a/100 if y_real==1.0 else (s.pg_emp/100 if y_real==0.5 else s.pg_b/100)
            p_f = s.pf_a/100 if y_real==1.0 else (s.pf_emp/100 if y_real==0.5 else s.pf_b/100)

            ll_k = -np.log(max(0.01, p_k))
            ll_g = -np.log(max(0.01, p_g))
            ll_f = -np.log(max(0.01, p_f))

            # ── Acierto de marcador ──
            mg_a, mg_b = s.marcador_prob
            acierto_marcador = (int(goles_a) == mg_a and int(goles_b) == mg_b)

            letra_grupo = s.active_fase.replace("Grupo ", "").strip()
            s.partidos_jugados[s.active_id] = {
                "local":    local_name, "visitante": visitante_name,
                "goles_l":  int(goles_a), "goles_v": int(goles_b),
                "grupo":    letra_grupo,
            }
            s.audit_history.append({
                "Partido":           s.active_match,
                "Real":              f"{goles_a}–{goles_b}",
                "Pred. Marcador":    f"{mg_a}–{mg_b}",
                "✅ Marcador":       "✅" if acierto_marcador else "❌",
                "Log Loss Klement":  round(ll_k, 3),
                "Log Loss Modelo 2": round(ll_g, 3),
                "Log Loss Fusión":   round(ll_f, 3),
            })

            res_txt = f"{local_name} gana" if goles_a > goles_b else (f"{visitante_name} gana" if goles_b > goles_a else "Empate")
            st.success(f"✅ Guardado: {local_name} {goles_a}–{goles_b} {visitante_name} → {res_txt}")
            if acierto_marcador:
                st.balloons()
                st.success("🎯 ¡El marcador predicho fue exacto!")
            st.info(f"Log Loss → Klement: `{ll_k:.3f}` | Modelo 2: `{ll_g:.3f}` | **Fusión: `{ll_f:.3f}`**")
    else:
        st.info("ℹ️ Primero corre una simulación en la pestaña 1.")

    st.markdown("### 📋 Historial Completo de Auditoría")
    if st.session_state.audit_history:
        df_audit = pd.DataFrame(st.session_state.audit_history)
        st.dataframe(df_audit, use_container_width=True)

        # Promedios
        ca, cb, cc = st.columns(3)
        ca.metric("📉 Log Loss Klement",  f"{df_audit['Log Loss Klement'].mean():.3f}")
        cb.metric("📉 Log Loss Modelo 2", f"{df_audit['Log Loss Modelo 2'].mean():.3f}")
        cc.metric("📉 Log Loss Fusión",   f"{df_audit['Log Loss Fusión'].mean():.3f}")

        aciertos = df_audit["✅ Marcador"].value_counts().get("✅", 0)
        total    = len(df_audit)
        st.metric("🎯 Aciertos de marcador exacto", f"{aciertos} / {total}  ({aciertos/total*100:.0f}%)")
    else:
        st.info("ℹ️ Aún no hay partidos registrados.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TABLAS DE POSICIONES
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🏆 Posiciones en Vivo — Fase de Grupos")

    grupos = ["A","B","C","D","E","F","G","H","I","J","K","L"]
    cols   = st.columns(2)

    for i, g in enumerate(grupos):
        df_g = utils.calcular_tabla_grupo(g, st.session_state.partidos_jugados)
        if df_g is not None:
            with cols[i % 2]:
                st.markdown(f"#### 🗂️ Grupo {g}")
                st.dataframe(
                    df_g.style.apply(
                        lambda row: [
                            "background-color:#d4edda" if row.name <= 2 else
                            "background-color:#fff3cd" if row.name == 3 else ""
                        ] * len(row),
                        axis=1,
                    ),
                    use_container_width=True,
                )

    if not st.session_state.partidos_jugados:
        st.info("ℹ️ Las tablas se actualizan automáticamente al registrar resultados en la pestaña 2.")
