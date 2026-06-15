# utils.py - Procesador y Ordenamiento de Tablas de Posiciones de Grupos
import pandas as pd
import data

def calcular_tabla_grupo(letra_grupo, partidos_jugados):
    """Filtra y procesa los puntos reales acumulados de un grupo específico"""
    
    # SOLUCIÓN 1: Extraemos los equipos directamente de TEAMS para evitar 
    # iterar innecesariamente sobre los 72 partidos del fixture dinámico.
    equipos_grupo = [name for name, info in data.TEAMS.items() if info["grupo"] == letra_grupo]
            
    if not equipos_grupo:
        return None

    # Inicializar la estructura vacía del grupo con tipos de datos nativos enteros
    tabla = {eq: {"PJ": 0, "PG": 0, "PE": 0, "PP": 0, "GF": 0, "GC": 0, "GD": 0, "Pts": 0} for eq in equipos_grupo}

    # Recorrer los marcadores almacenados de manera segura en el session_state
    for p_id, r in partidos_jugados.items():
        if r["grupo"] == letra_grupo:
            loc, vis = r["local"], r["visitante"]
            gl, gv = r["goles_l"], r["goles_v"]

            # Validación de seguridad por si las claves mutaron
            if loc in tabla and vis in tabla:
                tabla[loc]["PJ"] += 1
                tabla[vis]["PJ"] += 1
                tabla[loc]["GF"] += gl
                tabla[loc]["GC"] += gv
                tabla[vis]["GF"] += gv
                tabla[vis]["GC"] += gl

                # Asignación estricta de puntos oficiales FIFA
                if gl > gv:
                    tabla[loc]["PG"] += 1
                    tabla[loc]["Pts"] += 3
                    tabla[vis]["PP"] += 1
                elif gl == gv:
                    tabla[loc]["PE"] += 1
                    tabla[loc]["Pts"] += 1
                    tabla[vis]["PE"] += 1
                    tabla[vis]["Pts"] += 1
                else:
                    tabla[vis]["PG"] += 1
                    tabla[vis]["Pts"] += 3
                    tabla[loc]["PP"] += 1

                # Cálculo de la diferencia de goles
                tabla[loc]["GD"] = tabla[loc]["GF"] - tabla[loc]["GC"]
                tabla[vis]["GD"] = tabla[vis]["GF"] - tabla[vis]["GC"]

    # Convertir a DataFrame y ordenar estrictamente bajo métricas oficiales FIFA
    df = pd.DataFrame.from_dict(tabla, orient='index').reset_index()
    df = df.rename(columns={'index': 'Equipo'})
    
    # SOLUCIÓN 2: Añadimos 'Equipo' como criterio de desempate final alfabético 
    # para garantizar un ordenamiento estricto y determinista en la UI de Streamlit.
    df = df.sort_values(by=["Pts", "GD", "GF", "Equipo"], ascending=[False, False, False, True]).reset_index(drop=True)
    
    # Ajustamos el índice visual para que inicie en 1 en lugar de 0 (Formato de tabla de posiciones)
    df.index += 1
    return df
