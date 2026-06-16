# persistence.py - Persistencia via JSON en GitHub Repository
# Lee y escribe historial.json directamente en el repo usando la API de GitHub.
# No requiere secrets externos salvo GITHUB_TOKEN (ya disponible en Streamlit Cloud).

import json
import base64
import streamlit as st
import requests

# ── Configuración (se lee desde st.secrets) ──────────────────────────────────
def _cfg():
    try:
        return {
            "token": st.secrets["GITHUB_TOKEN"],
            "owner": st.secrets["GITHUB_OWNER"],   # tu usuario GitHub
            "repo":  st.secrets["GITHUB_REPO"],    # nombre del repo
            "path":  "historial.json",
        }
    except Exception:
        return None

# ── Estructura vacía por defecto ──────────────────────────────────────────────
ESTADO_VACIO = {
    "partidos_jugados": {},   # {id: {local, visitante, goles_l, goles_v, grupo}}
    "audit_history":    [],   # [{Partido, Real, Pred. Marcador, ...}]
    "fuerzas":          {},   # {equipo: {ataque, defensa}}  ← ajuste dinámico
}

# ── LEER desde GitHub ─────────────────────────────────────────────────────────
def cargar_estado():
    cfg = _cfg()
    if not cfg:
        return _estado_desde_session()

    url = f"https://api.github.com/repos/{cfg['owner']}/{cfg['repo']}/contents/{cfg['path']}"
    headers = {"Authorization": f"token {cfg['token']}"}
    r = requests.get(url, headers=headers, timeout=10)

    if r.status_code == 200:
        contenido = base64.b64decode(r.json()["content"]).decode("utf-8")
        data = json.loads(contenido)
        # Compatibilidad: asegurar claves nuevas si el JSON es viejo
        for k, v in ESTADO_VACIO.items():
            if k not in data:
                data[k] = v
        # Convertir claves de partidos_jugados a int (JSON las serializa como str)
        data["partidos_jugados"] = {
            int(k): v for k, v in data["partidos_jugados"].items()
        }
        return data
    elif r.status_code == 404:
        return dict(ESTADO_VACIO)
    else:
        st.warning(f"⚠️ No se pudo leer historial.json (HTTP {r.status_code}). Usando sesión local.")
        return _estado_desde_session()

# ── GUARDAR en GitHub ─────────────────────────────────────────────────────────
def guardar_estado(estado):
    cfg = _cfg()
    if not cfg:
        _guardar_en_session(estado)
        return False

    url = f"https://api.github.com/repos/{cfg['owner']}/{cfg['repo']}/contents/{cfg['path']}"
    headers = {
        "Authorization": f"token {cfg['token']}",
        "Content-Type":  "application/json",
    }

    contenido_b64 = base64.b64encode(
        json.dumps(estado, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    # Necesitamos el SHA actual para hacer PUT (actualizar)
    r_get = requests.get(url, headers=headers, timeout=10)
    sha = r_get.json().get("sha") if r_get.status_code == 200 else None

    payload = {
        "message": "auto: actualizar historial Mundial 2026",
        "content": contenido_b64,
    }
    if sha:
        payload["sha"] = sha

    r_put = requests.put(url, headers=headers, json=payload, timeout=15)
    if r_put.status_code in (200, 201):
        return True
    else:
        st.error(f"❌ Error al guardar en GitHub: {r_put.status_code} — {r_put.json().get('message','')}")
        _guardar_en_session(estado)
        return False

# ── Fallback: session_state si no hay secrets ─────────────────────────────────
def _estado_desde_session():
    if "_estado_persistido" in st.session_state:
        return st.session_state["_estado_persistido"]
    return dict(ESTADO_VACIO)

def _guardar_en_session(estado):
    st.session_state["_estado_persistido"] = estado
