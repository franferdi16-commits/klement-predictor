# data.py - Base de Datos Macroeconómica, Demográfica y Climática Oficial

TEAMS = {
    # --- GRUPO A ---
    "México": {
        "ranking": 15, "pib": 11000, "temp": 21.0, "poblacion": 128.5, 
        "confed": "CONCACAF", "campeon": False, "k_noise": -0.15, "m2_noise": 0.40
    },
    "Corea del Sur": {
        "ranking": 22, "pib": 32000, "temp": 12.5, "poblacion": 51.7, 
        "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.10
    },
    "Chequia": {
        "ranking": 36, "pib": 27000, "temp": 8.0, "poblacion": 10.8, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15
    },
    "Sudáfrica": {
        "ranking": 59, "pib": 6000, "temp": 17.5, "poblacion": 60.6, 
        "confed": "CAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20
    },
    
    # --- GRUPO B ---
    "Canadá": {
        "ranking": 49, "pib": 52000, "temp": -5.0, "poblacion": 38.9, 
        "confed": "CONCACAF", "campeon": False, "k_noise": -0.10, "m2_noise": 0.20
    },
    "Marruecos": {
        "ranking": 13, "pib": 4000, "temp": 17.5, "poblacion": 37.5, 
        "confed": "CAF", "campeon": False, "k_noise": 0.35, "m2_noise": 0.35
    },
    "Colombia": {
        "ranking": 12, "pib": 6500, "temp": 22.0, "poblacion": 51.5, 
        "confed": "CONMEBOL", "campeon": False, "k_noise": 0.30, "m2_noise": 0.50
    },
    "Irlanda": {
        "ranking": 60, "pib": 104000, "temp": 9.5, "poblacion": 5.1, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.10, "m2_noise": 0.10
    },
    
    # --- GRUPO C ---
    "Estados Unidos": {
        "ranking": 11, "pib": 80000, "temp": 12.0, "poblacion": 334.9, 
        "confed": "CONCACAF", "campeon": False, "k_noise": -0.10, "m2_noise": 0.20
    },
    "Paraguay": {
        "ranking": 56, "pib": 5500, "temp": 22.0, "poblacion": 6.7, 
        "confed": "CONMEBOL", "campeon": False, "k_noise": 0.25, "m2_noise": 0.50
    },
    "Ecuador": {
        "ranking": 31, "pib": 6300, "temp": 21.5, "poblacion": 18.0, 
        "confed": "CONMEBOL", "campeon": False, "k_noise": 0.25, "m2_noise": 0.45
    },
    "Fiyi": {
        "ranking": 160, "pib": 5000, "temp": 25.0, "poblacion": 0.9, 
        "confed": "OFC", "campeon": False, "k_noise": 0.05, "m2_noise": 0.05
    },
    
    # --- CABEZAS DE SERIE Y POTENCIAS COMPLEMENTARIAS ---
    "Argentina": {
        "ranking": 1, "pib": 13000, "temp": 14.0, "poblacion": 46.2, 
        "confed": "CONMEBOL", "campeon": True, "k_noise": 0.40, "m2_noise": 0.50
    },
    "Francia": {
        "ranking": 2, "pib": 45000, "temp": 11.0, "poblacion": 68.0, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.30, "m2_noise": 0.30
    },
    "España": {
        "ranking": 3, "pib": 32000, "temp": 14.5, "poblacion": 48.0, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.30, "m2_noise": 0.30
    },
    "Inglaterra": {
        "ranking": 4, "pib": 46000, "temp": 10.5, "poblacion": 56.5, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.25, "m2_noise": 0.20
    },
    "Brasil": {
        "ranking": 5, "pib": 10000, "temp": 25.0, "poblacion": 215.3, 
        "confed": "CONMEBOL", "campeon": False, "k_noise": 0.40, "m2_noise": 0.45
    },
    "Portugal": {
        "ranking": 6, "pib": 26000, "temp": 15.5, "poblacion": 10.4, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.25, "m2_noise": 0.25
    },
    "Países Bajos": {
        "ranking": 7, "pib": 62000, "temp": 10.0, "poblacion": 18.0, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.20
    },
    "Japón": {
        "ranking": 18, "pib": 34000, "temp": 11.5, "poblacion": 125.1, 
        "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15
    }
}

FIXTURE = [
    {"id": 1, "grupo": "A", "fase": "Grupo A", "local": "México", "visitante": "Sudáfrica"},
    {"id": 2, "grupo": "A", "fase": "Grupo A", "local": "Corea del Sur", "visitante": "Chequia"},
    {"id": 3, "grupo": "B", "fase": "Grupo B", "local": "Canadá", "visitante": "Irlanda"},
    {"id": 4, "grupo": "B", "fase": "Grupo B", "local": "Marruecos", "visitante": "Colombia"},
    {"id": 5, "grupo": "C", "fase": "Grupo C", "local": "Estados Unidos", "visitante": "Paraguay"},
    {"id": 6, "grupo": "C", "fase": "Grupo C", "local": "Ecuador", "visitante": "Fiyi"},
    {"id": 7, "grupo": "D", "fase": "Grupo D", "local": "Argentina", "visitante": "Francia"},
    {"id": 8, "grupo": "E", "fase": "Grupo E", "local": "Brasil", "visitante": "Japón"},
    # Fases Finales de Simulación Avanzada
    {"id": 9, "grupo": "Eliminatoria", "fase": "Cuartos de Final", "local": "Argentina", "visitante": "Brasil"},
    {"id": 10, "grupo": "Eliminatoria", "fase": "Semifinal", "local": "Francia", "visitante": "España"},
    {"id": 11, "grupo": "Eliminatoria", "fase": "Final", "local": "Portugal", "visitante": "Países Bajos"},
]
