# app.py - World Cup Pro Predictor 2026 v4.0
# Grupos + Eliminatorias completas (Ronda 32 → Final) + Modo Penales
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
# CARGA DE ESTADO
# ══════════════════════════════════════════════════════════════════════════════
if "_estado_cargado" not in st.session_state:
    estado = persistence.cargar_estado()
    st.session_state.partidos_jugados          = estado["partidos_jugados"]
    st.session_state.audit_history             = estado["audit_history"]
    st.session_state.fuerzas                   = calibrador.get_fuerzas(estado["fuerzas"])
    st.session_state.partidos_eliminatorias    = estado.get("partidos_eliminatorias", {})
    st.session_state._estado_cargado           = True

st.title("⚽ World Cup Pro Predictor 2026")
st.caption("Motor Fusionado · Fuerzas Dinámicas · Eliminatorias con Penales · Persistencia GitHub")
st.markdown("---")

n_grupos = len(st.session_state.partidos_jugados)
n_elim   = len(st.session_state.partidos_eliminatorias)
if n_grupos > 0:
    st.success(f"✅ {n_grupos} partido(s) de grupos · {n_elim} de eliminatorias cargados.")

# ── Resolver bracket dinámico ─────────────────────────────────────────────────
mapa_bracket = utils.resolver_bracket(st.session_state.partidos_eliminatorias)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📅 Grupos — Simulación",
    "🥊 Eliminatorias",
    "📊 Registro y Log Loss",
    "🏆 Tablas de Posiciones",
    "⚙️ Fuerzas por Equipo",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GRUPOS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("🗓️ Fase de Grupos — Selección de Partido")

    ids_jugados = set(st.session_state.partidos_jugados.keys())
    fixture_options = []
    for p in data.FIXTURE:
        estado_txt = "✅" if p["id"] in ids_jugados else "🔜"
        fixture_options.append(
            f"{estado_txt} Partido {p['id']} [{p['fase']}]: {p['local']} vs. {p['visitante']}"
        )

    selected = st.selectbox("Elige un enfrentamiento de grupos:", fixture_options, key="sel_grupo")

    try:
        match_id   = int(selected.split("Partido ")[1].split(" [")[0])
        match_data = next(p for p in data.FIXTURE if p["id"] == match_id)
        team_a, team_b = match_data["local"], match_data["visitante"]
        fase_actual    = match_data["fase"]
        a, b           = data.TEAMS[team_a], data.TEAMS[team_b]
    except Exception as e:
        st.error(f"Error al leer fixture: {e}")
        st.stop()

    lk_a = engines.engine_klement(a, b["confed"], es_local=True,  nombre_equipo=team_a)
    lk_b = engines.engine_klement(b, a["confed"], es_local=False, nombre_equipo=team_b)
    lg_a = engines.engine_model_two(a, b["confed"], es_local=True,  nombre_equipo=team_a)
    lg_b = engines.engine_model_two(b, a["confed"], es_local=False, nombre_equipo=team_b)

    usar_calibrador = st.checkbox("🔬 Activar Calibrador con Fuerzas Dinámicas",
                                  value=n_grupos >= 1, key="cal_grupo")

    if st.button("🎲 Correr 10,000 Simulaciones", key="sim_grupo"):
        if usar_calibrador and n_grupos >= 1:
            res_cal = calibrador.recalcular_con_tendencia_real(
                match_id, st.session_state.partidos_jugados,
                st.session_state.fuerzas, lk_a, lk_b, lg_a, lg_b,
            )
            mu_a = res_cal["mu_a"]; mu_b = res_cal["mu_b"]
            pf_a, pf_emp, pf_b = res_cal["pf_a"], res_cal["pf_emp"], res_cal["pf_b"]
            pk_a, pk_emp, pk_b = res_cal["pk_a"], res_cal["pk_emp"], res_cal["pk_b"]
            pg_a, pg_emp, pg_b = res_cal["pg_a"], res_cal["pg_emp"], res_cal["pg_b"]
            w_k, w_g = "Cal.", "Cal."
        else:
            res_raw = engines.ejecutar_montecarlo(lk_a, lk_b, lg_a, lg_b)
            mu_a = res_raw["mu_a"]; mu_b = res_raw["mu_b"]
            pf_a, pf_emp, pf_b = res_raw["pf_a"], res_raw["pf_emp"], res_raw["pf_b"]
            pk_a, pk_emp, pk_b = res_raw["pk_a"], res_raw["pk_emp"], res_raw["pk_b"]
            pg_a, pg_emp, pg_b = res_raw["pg_a"], res_raw["pg_emp"], res_raw["pg_b"]
            w_k, w_g = res_raw["w_k"], res_raw["w_g"]

        _n = 10000
        _sa = stats.poisson.rvs(mu=mu_a, size=_n)
        _sb = stats.poisson.rvs(mu=mu_b, size=_n)
        top5 = Counter(zip(_sa.tolist(), _sb.tolist())).most_common(5)

        st.session_state.update({
            "g_pf_a": pf_a, "g_pf_emp": pf_emp, "g_pf_b": pf_b,
            "g_pk_a": pk_a, "g_pk_emp": pk_emp, "g_pk_b": pk_b,
            "g_pg_a": pg_a, "g_pg_emp": pg_emp, "g_pg_b": pg_b,
            "g_mu_a": mu_a, "g_mu_b": mu_b,
            "g_w_k": w_k,   "g_w_g": w_g,
            "g_top5": top5,
            "g_marc_prob":   top5[0][0],
            "g_marc_prob_p": round(top5[0][1] / _n * 100, 1),
            "g_active_match": f"{team_a} vs. {team_b}",
            "g_active_id":    match_id,
            "g_active_fase":  fase_actual,
            "g_lk_a": lk_a, "g_lk_b": lk_b,
            "g_lg_a": lg_a, "g_lg_b": lg_b,
            "g_active_mu_a": mu_a, "g_active_mu_b": mu_b,
        })

    if st.session_state.get("g_active_match") == f"{team_a} vs. {team_b}":
        s = st.session_state
        st.markdown(f"**Motor →** λ {team_a}: `{s.g_mu_a:.3f}` | λ {team_b}: `{s.g_mu_b:.3f}` "
                    f"&nbsp;·&nbsp; Pesos K: `{s.g_w_k}%` M2: `{s.g_w_g}%`")
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric(f"🏆 {team_a}", f"{s.g_pf_a:.1f}%")
        c2.metric("🤝 Empate",    f"{s.g_pf_emp:.1f}%")
        c3.metric(f"🏆 {team_b}", f"{s.g_pf_b:.1f}%")

        pred = (f"🏆 Gana {team_a}" if s.g_pf_a > s.g_pf_b and s.g_pf_a > s.g_pf_emp
                else f"🏆 Gana {team_b}" if s.g_pf_b > s.g_pf_a and s.g_pf_b > s.g_pf_emp
                else "🤝 Empate")
        st.success(f"**Resultado predicho: {pred}**")

        st.markdown("### 🎯 Marcador Más Probable")
        mg_a, mg_b = s.g_marc_prob
        mc1, mc2, mc3 = st.columns([2, 1, 2])
        mc1.metric(team_a, str(mg_a))
        mc2.markdown("<h2 style='text-align:center;margin-top:18px'>—</h2>", unsafe_allow_html=True)
        mc3.metric(team_b, str(mg_b))
        st.caption(f"Frecuencia: **{s.g_marc_prob_p:.1f}%** de 10,000 simulaciones")

        st.markdown("#### 📋 Top 5 Marcadores")
        top5_rows = []
        for (ga, gb), freq in s.g_top5:
            res_t = f"Gana {team_a}" if ga > gb else (f"Gana {team_b}" if gb > ga else "Empate")
            top5_rows.append({"Marcador": f"{team_a} {ga} – {gb} {team_b}",
                               "Resultado": res_t, "Prob": f"{freq/100:.1f}%"})
        st.table(pd.DataFrame(top5_rows))

        bdf = pd.DataFrame({
            "Resultado": [f"Victoria {team_a}", "Empate", f"Victoria {team_b}"],
            "Prob (%)":  [round(s.g_pf_a,1), round(s.g_pf_emp,1), round(s.g_pf_b,1)],
        }).set_index("Resultado")
        st.bar_chart(bdf)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ELIMINATORIAS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🥊 Eliminatorias — Ronda de 32 → Final")
    st.caption("Sin empates. Si hay igualdad en 90' → prórroga → penales simulados.")

    # Filtro de fase
    fases_elim = ["Ronda de 32", "Ronda de 16", "Cuartos de final", "Semifinal",
                  "Tercer Puesto", "Final"]
    fase_sel = st.selectbox("Fase:", fases_elim, key="fase_elim")

    partidos_fase = [p for p in data.FIXTURE_ELIMINATORIAS if p["fase"] == fase_sel]

    # Construir opciones de partido resolviendo W/L del bracket
    elim_options = []
    for p in partidos_fase:
        loc_r, vis_r = utils.nombre_partido(p, mapa_bracket)
        jugado = p["id"] in {int(k) for k in st.session_state.partidos_eliminatorias}
        icono  = "✅" if jugado else "🔜"
        fecha  = p.get("fecha", "TBD")
        elim_options.append(
            (f"{icono} [{fecha}] {loc_r} vs. {vis_r}", p["id"], loc_r, vis_r)
        )

    if not elim_options:
        st.info("⏳ No hay partidos disponibles en esta fase todavía.")
    else:
        sel_label = st.selectbox("Selecciona partido:",
                                  [o[0] for o in elim_options], key="sel_elim")
        sel_item  = next(o for o in elim_options if o[0] == sel_label)
        e_id, team_a_e, team_b_e = sel_item[1], sel_item[2], sel_item[3]

        # Verificar que ambos equipos ya están resueltos (no son W/L pendientes)
        equipos_validos = (team_a_e in data.TEAMS and team_b_e in data.TEAMS)

        if not equipos_validos:
            st.warning(f"⏳ Esperando resultados anteriores para definir este cruce.")
            st.info(f"**{team_a_e}** vs. **{team_b_e}** — Se conocerán los equipos cuando avancen las rondas previas.")
        else:
            a_e = data.TEAMS[team_a_e]
            b_e = data.TEAMS[team_b_e]

            lk_a_e = engines.engine_klement(a_e, b_e["confed"], True,  team_a_e)
            lk_b_e = engines.engine_klement(b_e, a_e["confed"], False, team_b_e)
            lg_a_e = engines.engine_model_two(a_e, b_e["confed"], True,  team_a_e)
            lg_b_e = engines.engine_model_two(b_e, a_e["confed"], False, team_b_e)

            usar_cal_e = st.checkbox("🔬 Calibrador con Fuerzas Dinámicas",
                                      value=True, key="cal_elim")

            if st.button("🎲 Correr 10,000 Simulaciones (Modo Eliminatoria)", key="sim_elim"):
                if usar_cal_e and n_grupos >= 1:
                    # Combinar historial de grupos + eliminatorias para la tendencia
                    historial_combinado = {**st.session_state.partidos_jugados}
                    for k, v in st.session_state.partidos_eliminatorias.items():
                        historial_combinado[int(k) + 1000] = v
                    res_cal_e = calibrador.recalcular_con_tendencia_real(
                        e_id,
                        historial_combinado,
                        st.session_state.fuerzas,
                        lk_a_e, lk_b_e, lg_a_e, lg_b_e,
                    )
                    mu_a_e = res_cal_e["mu_a"]
                    mu_b_e = res_cal_e["mu_b"]
                else:
                    mu_a_e = 0.5 * lk_a_e + 0.5 * lg_a_e
                    mu_b_e = 0.5 * lk_b_e + 0.5 * lg_b_e

                # Simulación modo eliminatoria (con penales)
                prob_a_e, prob_b_e, pct_pen = calibrador.simular_eliminatoria(mu_a_e, mu_b_e)

                # Top 5 marcadores 90min
                _n = 10000
                _sa_e = stats.poisson.rvs(mu=mu_a_e, size=_n)
                _sb_e = stats.poisson.rvs(mu=mu_b_e, size=_n)
                top5_e = Counter(zip(_sa_e.tolist(), _sb_e.tolist())).most_common(5)

                st.session_state.update({
                    "e_prob_a": prob_a_e, "e_prob_b": prob_b_e,
                    "e_pct_pen": pct_pen,
                    "e_mu_a": mu_a_e, "e_mu_b": mu_b_e,
                    "e_top5": top5_e,
                    "e_marc_prob":   top5_e[0][0],
                    "e_marc_prob_p": round(top5_e[0][1] / _n * 100, 1),
                    "e_active_match": f"{team_a_e} vs. {team_b_e}",
                    "e_active_id": e_id,
                    "e_lk_a": lk_a_e, "e_lk_b": lk_b_e,
                    "e_lg_a": lg_a_e, "e_lg_b": lg_b_e,
                    "e_active_mu_a": mu_a_e, "e_active_mu_b": mu_b_e,
                })

            if st.session_state.get("e_active_match") == f"{team_a_e} vs. {team_b_e}":
                s = st.session_state
                st.markdown(f"**λ {team_a_e}:** `{s.e_mu_a:.3f}` | **λ {team_b_e}:** `{s.e_mu_b:.3f}`")
                st.markdown("---")

                c1, c2 = st.columns(2)
                c1.metric(f"🏆 Pasa {team_a_e}", f"{s.e_prob_a:.1f}%")
                c2.metric(f"🏆 Pasa {team_b_e}", f"{s.e_prob_b:.1f}%")

                if s.e_pct_pen > 0:
                    st.info(f"🔫 Probabilidad de ir a **penales**: {s.e_pct_pen:.1f}% de las simulaciones")

                pred_e = team_a_e if s.e_prob_a >= s.e_prob_b else team_b_e
                st.success(f"**Predicción: 🏆 Pasa {pred_e}**")

                st.markdown("### 🎯 Marcador Más Probable (90 min)")
                mg_a_e, mg_b_e = s.e_marc_prob
                mc1, mc2, mc3 = st.columns([2, 1, 2])
                mc1.metric(team_a_e, str(mg_a_e))
                mc2.markdown("<h2 style='text-align:center;margin-top:18px'>—</h2>", unsafe_allow_html=True)
                mc3.metric(team_b_e, str(mg_b_e))
                st.caption(f"Frecuencia: **{s.e_marc_prob_p:.1f}%** de 10,000 simulaciones")

                st.markdown("#### 📋 Top 5 Marcadores (90 min)")
                top5_e_rows = []
                for (ga, gb), freq in s.e_top5:
                    res_t = (f"Pasa {team_a_e}" if ga > gb
                             else f"Pasa {team_b_e}" if gb > ga else "→ Prórroga/Penales")
                    top5_e_rows.append({"Marcador": f"{team_a_e} {ga} – {gb} {team_b_e}",
                                        "Resultado": res_t, "Prob": f"{freq/100:.1f}%"})
                st.table(pd.DataFrame(top5_e_rows))

                bdf_e = pd.DataFrame({
                    "Equipo": [f"Pasa {team_a_e}", f"Pasa {team_b_e}"],
                    "Prob (%)": [round(s.e_prob_a,1), round(s.e_prob_b,1)],
                }).set_index("Equipo")
                st.bar_chart(bdf_e)

            # ── Registrar resultado de eliminatoria ──────────────────────────
            st.markdown("---")
            st.markdown("#### 💾 Registrar Resultado")
            jugado_e = e_id in {int(k) for k in st.session_state.partidos_eliminatorias}
            if jugado_e:
                rj = st.session_state.partidos_eliminatorias[str(e_id)]
                pen_txt = (f" (Penales: {rj.get('penales_l','?')}–{rj.get('penales_v','?')})"
                           if rj.get("penales_l") is not None else "")
                st.info(f"Ya registrado: **{rj['goles_l']} – {rj['goles_v']}**{pen_txt}")

            cg1, cg2 = st.columns(2)
            with cg1:
                ge_a = st.number_input(f"⚽ Goles {team_a_e} (90')", min_value=0, step=1, key="ge_a")
            with cg2:
                ge_b = st.number_input(f"⚽ Goles {team_b_e} (90')", min_value=0, step=1, key="ge_b")

            hubo_penales = st.checkbox("¿Hubo prórroga y penales?", key="cb_pen")
            pen_a, pen_b = 0, 0
            if hubo_penales:
                cp1, cp2 = st.columns(2)
                with cp1:
                    pen_a = st.number_input(f"🔫 Penales {team_a_e}", min_value=0, step=1, key="pen_a")
                with cp2:
                    pen_b = st.number_input(f"🔫 Penales {team_b_e}", min_value=0, step=1, key="pen_b")

            if st.button("💾 Guardar Resultado Eliminatoria", key="save_elim"):
                resultado_elim = {
                    "local": team_a_e, "visitante": team_b_e,
                    "goles_l": int(ge_a), "goles_v": int(ge_b),
                    "fase": fase_sel,
                }
                if hubo_penales:
                    resultado_elim["penales_l"] = int(pen_a)
                    resultado_elim["penales_v"] = int(pen_b)

                st.session_state.partidos_eliminatorias[str(e_id)] = resultado_elim

                # Actualizar fuerzas dinámicas
                mu_a_sv = st.session_state.get("e_active_mu_a", 1.5)
                mu_b_sv = st.session_state.get("e_active_mu_b", 1.5)
                st.session_state.fuerzas = calibrador.actualizar_fuerzas(
                    st.session_state.fuerzas,
                    team_a_e, team_b_e,
                    int(ge_a), int(ge_b),
                    mu_a_sv, mu_b_sv,
                )

                # Recalcular bracket
                mapa_bracket = utils.resolver_bracket(st.session_state.partidos_eliminatorias)

                # Guardar en GitHub
                guardado = persistence.guardar_estado({
                    "partidos_jugados":       {str(k): v for k, v in st.session_state.partidos_jugados.items()},
                    "audit_history":          st.session_state.audit_history,
                    "fuerzas":                st.session_state.fuerzas,
                    "partidos_eliminatorias": st.session_state.partidos_eliminatorias,
                })

                pen_txt = f" (Penales: {pen_a}–{pen_b})" if hubo_penales else ""
                ganador_e = team_a_e if (ge_a > ge_b or (hubo_penales and pen_a > pen_b)) else team_b_e
                st.success(f"✅ {team_a_e} {ge_a}–{ge_b} {team_b_e}{pen_txt} → **Pasa {ganador_e}**")
                if guardado:
                    st.success("💾 Guardado en GitHub.")
                st.rerun()

    # ── Bracket visual ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🗺️ Estado del Bracket")

    for fase in fases_elim:
        partidos_f = [p for p in data.FIXTURE_ELIMINATORIAS if p["fase"] == fase]
        if not partidos_f:
            continue
        st.markdown(f"**{fase}**")
        cols = st.columns(min(len(partidos_f), 4))
        for i, p in enumerate(partidos_f):
            loc_r, vis_r = utils.nombre_partido(p, mapa_bracket)
            jugado_f = p["id"] in {int(k) for k in st.session_state.partidos_eliminatorias}
            with cols[i % len(cols)]:
                if jugado_f:
                    r = st.session_state.partidos_eliminatorias[str(p["id"])]
                    ganador_f = (r["local"] if r["goles_l"] > r["goles_v"]
                                 else r["visitante"] if r["goles_v"] > r["goles_l"]
                                 else (r["local"] if r.get("penales_l",0) > r.get("penales_v",0)
                                       else r["visitante"]))
                    st.success(f"✅ **{ganador_f}** pasa\n{r['goles_l']}–{r['goles_v']}")
                elif loc_r.startswith("W") or vis_r.startswith("W"):
                    st.info(f"⏳ Por definir")
                else:
                    st.warning(f"🔜 {loc_r}\nvs.\n{vis_r}")
        st.markdown("")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — REGISTRO Y LOG LOSS (Grupos)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("📝 Registrar Marcador Real — Fase de Grupos")

    if "g_active_match" in st.session_state:
        s = st.session_state
        local_name, visitante_name = s.g_active_match.split(" vs. ")

        if s.g_active_id in s.partidos_jugados:
            rj = s.partidos_jugados[s.g_active_id]
            st.info(f"Este partido ya fue registrado: **{rj['goles_l']} – {rj['goles_v']}**")

        cg1, cg2 = st.columns(2)
        with cg1:
            goles_a = st.number_input(f"⚽ Goles {local_name}",    min_value=0, step=1, key="g_r_a")
        with cg2:
            goles_b = st.number_input(f"⚽ Goles {visitante_name}", min_value=0, step=1, key="g_r_b")

        if st.button("💾 Guardar y Actualizar Modelo", key="save_grupo"):
            y_real = 1.0 if goles_a > goles_b else (0.5 if goles_a == goles_b else 0.0)
            p_k = s.g_pk_a/100 if y_real==1.0 else (s.g_pk_emp/100 if y_real==0.5 else s.g_pk_b/100)
            p_g = s.g_pg_a/100 if y_real==1.0 else (s.g_pg_emp/100 if y_real==0.5 else s.g_pg_b/100)
            p_f = s.g_pf_a/100 if y_real==1.0 else (s.g_pf_emp/100 if y_real==0.5 else s.g_pf_b/100)
            ll_k = -np.log(max(0.01, p_k))
            ll_g = -np.log(max(0.01, p_g))
            ll_f = -np.log(max(0.01, p_f))

            mg_a, mg_b       = s.g_marc_prob
            acierto_marcador = (int(goles_a) == mg_a and int(goles_b) == mg_b)
            letra_grupo      = s.g_active_fase.replace("Grupo ", "").strip()

            s.partidos_jugados[s.g_active_id] = {
                "local": local_name, "visitante": visitante_name,
                "goles_l": int(goles_a), "goles_v": int(goles_b),
                "grupo": letra_grupo,
            }
            s.fuerzas = calibrador.actualizar_fuerzas(
                s.fuerzas, local_name, visitante_name,
                int(goles_a), int(goles_b), s.g_active_mu_a, s.g_active_mu_b,
            )
            s.audit_history.append({
                "Partido":           s.g_active_match,
                "Real":              f"{goles_a}–{goles_b}",
                "Pred. Marcador":    f"{mg_a}–{mg_b}",
                "✅ Marcador":       "✅" if acierto_marcador else "❌",
                "Log Loss Klement":  round(ll_k, 3),
                "Log Loss Modelo 2": round(ll_g, 3),
                "Log Loss Fusión":   round(ll_f, 3),
            })

            guardado = persistence.guardar_estado({
                "partidos_jugados":       {str(k): v for k, v in s.partidos_jugados.items()},
                "audit_history":          s.audit_history,
                "fuerzas":                s.fuerzas,
                "partidos_eliminatorias": s.partidos_eliminatorias,
            })

            res_txt = (f"{local_name} gana" if goles_a > goles_b
                       else f"{visitante_name} gana" if goles_b > goles_a else "Empate")
            st.success(f"✅ {local_name} {goles_a}–{goles_b} {visitante_name} → {res_txt}")
            if guardado: st.success("💾 Guardado en GitHub.")
            if acierto_marcador: st.balloons(); st.success("🎯 ¡Marcador exacto!")
            st.info(f"Log Loss → K: `{ll_k:.3f}` | M2: `{ll_g:.3f}` | Fusión: `{ll_f:.3f}`")
    else:
        st.info("ℹ️ Primero corre una simulación en la pestaña 'Grupos — Simulación'.")

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
# TAB 4 — TABLAS DE POSICIONES
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("🏆 Posiciones Finales de Grupos")
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
# TAB 5 — FUERZAS POR EQUIPO
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("⚙️ Fuerzas Dinámicas por Equipo")
    st.caption("Se actualizan automáticamente con cada resultado registrado (grupos + eliminatorias).")

    grupos_filter = ["Todos"] + ["A","B","C","D","E","F","G","H","I","J","K","L"]
    filtro = st.selectbox("Filtrar por grupo:", grupos_filter, key="fil_fuerzas")

    rows = []
    for eq, f in st.session_state.fuerzas.items():
        grupo_eq = data.TEAMS[eq]["grupo"]
        if filtro != "Todos" and grupo_eq != filtro:
            continue
        rows.append({
            "Equipo":  eq,
            "Grupo":   grupo_eq,
            "Ataque":  round(f["ataque"], 3),
            "Defensa": round(f["defensa"], 3),
            "Ranking": data.TEAMS[eq]["ranking"],
        })

    df_f = pd.DataFrame(rows).sort_values(["Ataque"], ascending=False)
    st.dataframe(df_f.set_index("Equipo"), use_container_width=True)

    if st.button("🔄 Recargar historial desde GitHub", key="reload"):
        del st.session_state["_estado_cargado"]
        st.rerun()
