# app.py - World Cup Pro Predictor 2026 v3.0
# Persistencia GitHub JSON + Fuerzas dinámicas + Motor fusionado
import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import scipy.stats as stats

import data
import engines
import utils
import calibrador
import persistence

st.set_page_config(
    page_title="World Cup Pro Predictor 2026",
    page_icon="⚽", layout="wide"
)

# ══════════════════════════════════════════════════════════════════════════════
# CARGA DE ESTADO PERSISTIDO (una sola vez por sesión)
# ══════════════════════════════════════════════════════════════════════════════
if "_estado_cargado" not in st.session_state:
    estado = persistence.cargar_estado()
    st.session_state.partidos_jugados = estado["partidos_jugados"]
    st.session_state.audit_history    = estado["audit_history"]
    st.session_state.fuerzas          = calibrador.get_fuerzas(estado["fuerzas"])
    st.session_state._estado_cargado  = True

st.title("⚽ World Cup Pro Predictor 2026")
st.caption("Motor Fusionado · Fuerzas Dinámicas · Persistencia GitHub")
st.markdown("---")

# Indicador de partidos cargados
n_jugados = len(st.session_state.partidos_jugados)
if n_jugados > 0:
    st.success(f"✅ {n_jugados} partido(s) cargados desde el historial guardado.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📅 Simulación y Marcador",
    "📊 Registro y Log Loss",
    "🏆 Tablas de Posiciones",
    "⚙️ Fuerzas por Equipo",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SIMULACIÓN
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("🗓️ Fixture Oficial — Selección de Partido")

    # Separar jugados de pendientes
    ids_jugados = set(st.session_state.partidos_jugados.keys())
    fixture_options = []
    for p in data.FIXTURE:
        estado_txt = "✅" if p["id"] in ids_jugados else "🔜"
        fixture_options.append(
            f"{estado_txt} Partido {p['id']} [{p['fase']}]: {p['local']} vs. {p['visitante']}"
        )

    selected = st.selectbox("Elige un enfrentamiento:", fixture_options)

    try:
        match_id   = int(selected.split("Partido ")[1].split(" [")[0])
        match_data = next(p for p in data.FIXTURE if p["id"] == match_id)
        team_a, team_b = match_data["local"], match_data["visitante"]
        fase_actual    = match_data["fase"]
        a, b           = data.TEAMS[team_a], data.TEAMS[team_b]
    except Exception as e:
        st.error(f"Error al leer fixture: {e}")
        st.stop()

    lk_a = engines.engine_klement(a, b["confed"], es_local=True)
    lk_b = engines.engine_klement(b, a["confed"], es_local=False)
    lg_a = engines.engine_model_two(a, b["confed"], es_local=True)
    lg_b = engines.engine_model_two(b, a["confed"], es_local=False)

    usar_calibrador = st.checkbox(
        "🔬 Activar Calibrador con Fuerzas Dinámicas",
        value=n_jugados >= 1,
    )

    if st.button("🎲 Correr 10,000 Simulaciones"):
        if usar_calibrador and n_jugados >= 1:
            res_cal = calibrador.recalcular_con_tendencia_real(
                match_id,
                st.session_state.partidos_jugados,
                st.session_state.fuerzas,
                lk_a, lk_b, lg_a, lg_b,
            )
            mu_a = res_cal["mu_a"]
            mu_b = res_cal["mu_b"]
            pf_a, pf_emp, pf_b   = res_cal["pf_a"], res_cal["pf_emp"], res_cal["pf_b"]
            pk_a, pk_emp, pk_b   = res_cal["pk_a"], res_cal["pk_emp"], res_cal["pk_b"]
            pg_a, pg_emp, pg_b   = res_cal["pg_a"], res_cal["pg_emp"], res_cal["pg_b"]
            w_k, w_g = "Cal.", "Cal."
        else:
            # Motor fusionado base 50/50
            mu_a = 0.5 * lk_a + 0.5 * lg_a
            mu_b = 0.5 * lk_b + 0.5 * lg_b
            pf_a   = float(np.mean(
                [stats.poisson.rvs(mu=mu_a) > stats.poisson.rvs(mu=mu_b) for _ in range(10000)]
            )) * 100
            # Usar engines para los individuales
            res_raw = engines.ejecutar_montecarlo(lk_a, lk_b, lg_a, lg_b)
            pk_a, pk_emp, pk_b = res_raw["pk_a"], res_raw["pk_emp"], res_raw["pk_b"]
            pg_a, pg_emp, pg_b = res_raw["pg_a"], res_raw["pg_emp"], res_raw["pg_b"]
            pf_a, pf_emp, pf_b = res_raw["pk_a"], res_raw["pk_emp"], res_raw["pk_b"]
            w_k, w_g = 50.0, 50.0

        # Marcador top 5 desde simulación directa
        _n = 10000
        _sa = stats.poisson.rvs(mu=mu_a, size=_n)
        _sb = stats.poisson.rvs(mu=mu_b, size=_n)
        top5 = Counter(zip(_sa.tolist(), _sb.tolist())).most_common(5)

        st.session_state.update({
            "pf_a": pf_a, "pf_emp": pf_emp, "pf_b": pf_b,
            "pk_a": pk_a, "pk_emp": pk_emp, "pk_b": pk_b,
            "pg_a": pg_a, "pg_emp": pg_emp, "pg_b": pg_b,
            "mu_a": mu_a, "mu_b": mu_b,
            "w_k": w_k,   "w_g": w_g,
            "top5_marcadores": top5,
            "marcador_prob":   top5[0][0],
            "marcador_prob_p": round(top5[0][1] / _n * 100, 1),
            "active_match": f"{team_a} vs. {team_b}",
            "active_id":    match_id,
            "active_fase":  fase_actual,
            "active_lk_a":  lk_a, "active_lk_b": lk_b,
            "active_lg_a":  lg_a, "active_lg_b": lg_b,
            "active_mu_a":  mu_a, "active_mu_b": mu_b,
        })

    if st.session_state.get("active_match") == f"{team_a} vs. {team_b}":
        s = st.session_state
        st.markdown(
            f"**Motor →** λ {team_a}: `{s.mu_a:.3f}` | λ {team_b}: `{s.mu_b:.3f}` "
            f"&nbsp;·&nbsp; Pesos K: `{s.w_k}%` M2: `{s.w_g}%`"
        )
        st.markdown("---")

        # Probabilidades
        c1, c2, c3 = st.columns(3)
        c1.metric(f"🏆 {team_a}", f"{s.pf_a:.1f}%")
        c2.metric("🤝 Empate",    f"{s.pf_emp:.1f}%")
        c3.metric(f"🏆 {team_b}", f"{s.pf_b:.1f}%")

        pred = (f"🏆 Gana {team_a}" if s.pf_a > s.pf_b and s.pf_a > s.pf_emp
                else f"🏆 Gana {team_b}" if s.pf_b > s.pf_a and s.pf_b > s.pf_emp
                else "🤝 Empate")
        st.success(f"**Resultado predicho: {pred}**")

        # Marcador probable
        st.markdown("### 🎯 Marcador Más Probable")
        mg_a, mg_b = s.marcador_prob
        mc1, mc2, mc3 = st.columns([2, 1, 2])
        mc1.metric(team_a, str(mg_a))
        mc2.markdown("<h2 style='text-align:center;margin-top:18px'>—</h2>", unsafe_allow_html=True)
        mc3.metric(team_b, str(mg_b))
        st.caption(f"Frecuencia: **{s.marcador_prob_p:.1f}%** de 10,000 simulaciones")

        # Top 5
        st.markdown("#### 📋 Top 5 Marcadores")
        top5_rows = []
        for (ga, gb), freq in s.top5_marcadores:
            res_t = f"Gana {team_a}" if ga > gb else (f"Gana {team_b}" if gb > ga else "Empate")
            top5_rows.append({
                "Marcador":      f"{team_a} {ga} – {gb} {team_b}",
                "Resultado":     res_t,
                "Probabilidad":  f"{freq/100:.1f}%",
            })
        st.table(pd.DataFrame(top5_rows))

        # Barra
        bdf = pd.DataFrame({
            "Resultado": [f"Victoria {team_a}", "Empate", f"Victoria {team_b}"],
            "Prob (%)":  [round(s.pf_a,1), round(s.pf_emp,1), round(s.pf_b,1)],
        }).set_index("Resultado")
        st.bar_chart(bdf)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REGISTRO Y LOG LOSS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("📝 Registrar Marcador Real")

    if "active_match" in st.session_state:
        s = st.session_state
        local_name, visitante_name = s.active_match.split(" vs. ")

        # Si ya está jugado, mostrarlo
        if s.active_id in s.partidos_jugados:
            rj = s.partidos_jugados[s.active_id]
            st.info(f"Este partido ya fue registrado: **{rj['goles_l']} – {rj['goles_v']}**")

        cg1, cg2 = st.columns(2)
        with cg1:
            goles_a = st.number_input(f"⚽ Goles {local_name}",    min_value=0, step=1, key="g_r_a")
        with cg2:
            goles_b = st.number_input(f"⚽ Goles {visitante_name}", min_value=0, step=1, key="g_r_b")

        if st.button("💾 Guardar y Actualizar Modelo"):
            y_real = 1.0 if goles_a > goles_b else (0.5 if goles_a == goles_b else 0.0)

            p_k = s.pk_a/100 if y_real==1.0 else (s.pk_emp/100 if y_real==0.5 else s.pk_b/100)
            p_g = s.pg_a/100 if y_real==1.0 else (s.pg_emp/100 if y_real==0.5 else s.pg_b/100)
            p_f = s.pf_a/100 if y_real==1.0 else (s.pf_emp/100 if y_real==0.5 else s.pf_b/100)

            ll_k = -np.log(max(0.01, p_k))
            ll_g = -np.log(max(0.01, p_g))
            ll_f = -np.log(max(0.01, p_f))

            mg_a, mg_b        = s.marcador_prob
            acierto_marcador  = (int(goles_a) == mg_a and int(goles_b) == mg_b)
            letra_grupo       = s.active_fase.replace("Grupo ", "").strip()

            # Guardar resultado
            s.partidos_jugados[s.active_id] = {
                "local": local_name, "visitante": visitante_name,
                "goles_l": int(goles_a), "goles_v": int(goles_b),
                "grupo":   letra_grupo,
            }

            # Actualizar fuerzas dinámicas
            s.fuerzas = calibrador.actualizar_fuerzas(
                s.fuerzas, local_name, visitante_name,
                int(goles_a), int(goles_b),
                s.active_mu_a, s.active_mu_b,
            )

            s.audit_history.append({
                "Partido":           s.active_match,
                "Real":              f"{goles_a}–{goles_b}",
                "Pred. Marcador":    f"{mg_a}–{mg_b}",
                "✅ Marcador":       "✅" if acierto_marcador else "❌",
                "Log Loss Klement":  round(ll_k, 3),
                "Log Loss Modelo 2": round(ll_g, 3),
                "Log Loss Fusión":   round(ll_f, 3),
            })

            # ── PERSISTIR EN GITHUB ──────────────────────────────────────────
            guardado = persistence.guardar_estado({
                "partidos_jugados": {str(k): v for k, v in s.partidos_jugados.items()},
                "audit_history":    s.audit_history,
                "fuerzas":          s.fuerzas,
            })

            res_txt = (f"{local_name} gana" if goles_a > goles_b
                       else f"{visitante_name} gana" if goles_b > goles_a else "Empate")
            st.success(f"✅ {local_name} {goles_a}–{goles_b} {visitante_name} → {res_txt}")
            if guardado:
                st.success("💾 Historial guardado en GitHub.")
            if acierto_marcador:
                st.balloons()
                st.success("🎯 ¡Marcador exacto predicho!")
            st.info(f"Log Loss → K: `{ll_k:.3f}` | M2: `{ll_g:.3f}` | Fusión: `{ll_f:.3f}`")

    else:
        st.info("ℹ️ Primero corre una simulación en la pestaña 1.")

    st.markdown("### 📋 Historial de Auditoría")
    if st.session_state.audit_history:
        df_a = pd.DataFrame(st.session_state.audit_history)
        st.dataframe(df_a, use_container_width=True)
        ca, cb, cc = st.columns(3)
        ca.metric("Log Loss Klement",  f"{df_a['Log Loss Klement'].mean():.3f}")
        cb.metric("Log Loss Modelo 2", f"{df_a['Log Loss Modelo 2'].mean():.3f}")
        cc.metric("Log Loss Fusión",   f"{df_a['Log Loss Fusión'].mean():.3f}")
        aciertos = df_a["✅ Marcador"].value_counts().get("✅", 0)
        st.metric("🎯 Aciertos de marcador exacto",
                  f"{aciertos} / {len(df_a)}  ({aciertos/len(df_a)*100:.0f}%)")
    else:
        st.info("ℹ️ Sin partidos registrados aún.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TABLAS DE POSICIONES
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🏆 Posiciones en Vivo")
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
                        ] * len(row), axis=1,
                    ),
                    use_container_width=True,
                )
    if not st.session_state.partidos_jugados:
        st.info("ℹ️ Las tablas se actualizan al registrar resultados.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — FUERZAS POR EQUIPO
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("⚙️ Fuerzas Dinámicas por Equipo")
    st.caption("Se actualizan automáticamente con cada resultado registrado.")

    grupos_filter = ["Todos"] + ["A","B","C","D","E","F","G","H","I","J","K","L"]
    filtro = st.selectbox("Filtrar por grupo:", grupos_filter)

    rows = []
    for eq, f in st.session_state.fuerzas.items():
        grupo_eq = data.TEAMS[eq]["grupo"]
        if filtro != "Todos" and grupo_eq != filtro:
            continue
        rows.append({
            "Equipo":   eq,
            "Grupo":    grupo_eq,
            "Ataque":   round(f["ataque"], 3),
            "Defensa":  round(f["defensa"], 3),
            "Ranking":  data.TEAMS[eq]["ranking"],
        })

    df_f = pd.DataFrame(rows).sort_values(["Grupo","Ataque"], ascending=[True, False])
    st.dataframe(df_f.set_index("Equipo"), use_container_width=True)

    if st.button("🔄 Recargar historial desde GitHub"):
        del st.session_state["_estado_cargado"]
        st.rerun()
