TEAMS = {
    "México": { "grupo": "A", "ranking": 15, "pib": 11000, "temp": 21.0, "poblacion": 128.5, "confed": "CONCACAF", "campeon": False, "k_noise": -0.15, "m2_noise": 0.40 },
    "República de Corea": { "grupo": "A", "ranking": 22, "pib": 32000, "temp": 12.5, "poblacion": 51.7, "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.10 },
    "República Checa": { "grupo": "A", "ranking": 36, "pib": 27000, "temp": 8.0, "poblacion": 10.8, "confed": "UEFA", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15 },
    "Sudáfrica": { "grupo": "A", "ranking": 59, "pib": 6000, "temp": 17.5, "poblacion": 60.6, "confed": "CAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20 },
    "Canadá": { "grupo": "B", "ranking": 49, "pib": 52000, "temp": -5.0, "poblacion": 38.9, "confed": "CONCACAF", "campeon": False, "k_noise": -0.10, "m2_noise": 0.20 },
    "Bosnia y Herzegovina": { "grupo": "B", "ranking": 75, "pib": 9000, "temp": 10.0, "poblacion": 3.2, "confed": "UEFA", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15 },
    "Catar": { "grupo": "B", "ranking": 34, "pib": 82000, "temp": 27.0, "poblacion": 2.7, "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20 },
    "Suiza": { "grupo": "B", "ranking": 19, "pib": 93000, "temp": 5.5, "poblacion": 8.9, "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.15 },
    "Brasil": { "grupo": "C", "ranking": 5, "pib": 10000, "temp": 25.0, "poblacion": 215.3, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.40, "m2_noise": 0.45 },
    "Marruecos": { "grupo": "C", "ranking": 13, "pib": 4000, "temp": 17.5, "poblacion": 37.5, "confed": "CAF", "campeon": False, "k_noise": 0.35, "m2_noise": 0.35 },
    "Haití": { "grupo": "C", "ranking": 86, "pib": 1700, "temp": 25.0, "poblacion": 11.7, "confed": "CONCACAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.30 },
    "Escocia": { "grupo": "C", "ranking": 39, "pib": 42000, "temp": 8.0, "poblacion": 5.4, "confed": "UEFA", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20 },
    "Estados Unidos": { "grupo": "D", "ranking": 11, "pib": 80000, "temp": 12.0, "poblacion": 334.9, "confed": "CONCACAF", "campeon": False, "k_noise": -0.10, "m2_noise": 0.20 },
    "Paraguay": { "grupo": "D", "ranking": 56, "pib": 5500, "temp": 22.0, "poblacion": 6.7, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.25, "m2_noise": 0.50 },
    "Australia": { "grupo": "D", "ranking": 24, "pib": 65000, "temp": 21.5, "poblacion": 26.0, "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15 },
    "Turquía": { "grupo": "D", "ranking": 40, "pib": 10000, "temp": 12.0, "poblacion": 85.3, "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25 },
    # ... agregar todos los equipos aquí
}

FIXTURE = [
    {"id": 1, "grupo": "A", "fase": "Grupo A", "local": "México", "visitante": "Sudáfrica"},
    {"id": 2, "grupo": "A", "fase": "Grupo A", "local": "República de Corea", "visitante": "República Checa"},
    {"id": 3, "grupo": "B", "fase": "Grupo B", "local": "Canadá", "visitante": "Bosnia y Herzegovina"},
    {"id": 4, "grupo": "D", "fase": "Grupo D", "local": "Estados Unidos", "visitante": "Paraguay"},
    {"id": 5, "grupo": "B", "fase": "Grupo B", "local": "Catar", "visitante": "Suiza"},
    {"id": 6, "grupo": "C", "fase": "Grupo C", "local": "Brasil", "visitante": "Marruecos"},
    {"id": 7, "grupo": "C", "fase": "Grupo C", "local": "Haití", "visitante": "Escocia"},
    {"id": 8, "grupo": "D", "fase": "Grupo D", "local": "Australia", "visitante": "Turquía"},
    # ... agregar todos los partidos aquí
    {"id": 60, "grupo": "L", "fase": "Grupo L", "local": "Panamá", "visitante": "Croacia"}
]
