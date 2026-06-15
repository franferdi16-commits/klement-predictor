# data.py - BASE DE DATOS OFICIAL Y VERIFICADA FIFA 2026 (48 SELECCIONES)

TEAMS = {
    # --- GRUPO A ---
    "México": { "grupo": "A", "ranking": 15, "pib": 11000, "temp": 21.0, "poblacion": 128.5, "confed": "CONCACAF", "campeon": False, "k_noise": -0.15, "m2_noise": 0.40 },
    "Sudáfrica": { "grupo": "A", "ranking": 59, "pib": 6000, "temp": 17.5, "poblacion": 60.6, "confed": "CAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20 },
    "Corea del Sur": { "grupo": "A", "ranking": 22, "pib": 32000, "temp": 12.5, "poblacion": 51.7, "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.10 },
    "Chequia": { "grupo": "A", "ranking": 36, "pib": 27000, "temp": 8.0, "poblacion": 10.8, "confed": "UEFA", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15 },
    
    # --- GRUPO B ---
    "Canadá": { "grupo": "B", "ranking": 49, "pib": 52000, "temp": -5.0, "poblacion": 38.9, "confed": "CONCACAF", "campeon": False, "k_noise": -0.10, "m2_noise": 0.20 },
    "Bosnia y Herzegovina": { "grupo": "B", "ranking": 75, "pib": 9000, "temp": 10.0, "poblacion": 3.2, "confed": "UEFA", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15 },
    "Catar": { "grupo": "B", "ranking": 34, "pib": 82000, "temp": 27.0, "poblacion": 2.7, "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20 },
    "Suiza": { "grupo": "B", "ranking": 19, "pib": 93000, "temp": 5.5, "poblacion": 8.9, "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.15 },
    
    # --- GRUPO C ---
    "Brasil": { "grupo": "C", "ranking": 5, "pib": 10000, "temp": 25.0, "poblacion": 215.3, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.40, "m2_noise": 0.45 },
    "Marruecos": { "grupo": "C", "ranking": 13, "pib": 4000, "temp": 17.5, "poblacion": 37.5, "confed": "CAF", "campeon": False, "k_noise": 0.35, "m2_noise": 0.35 },
    "Haití": { "grupo": "C", "ranking": 86, "pib": 1700, "temp": 25.0, "poblacion": 11.7, "confed": "CONCACAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.30 },
    "Escocia": { "grupo": "C", "ranking": 39, "pib": 42000, "temp": 8.0, "poblacion": 5.4, "confed": "UEFA", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20 },
    
    # --- GRUPO D ---
    "Estados Unidos": { "grupo": "D", "ranking": 11, "pib": 80000, "temp": 12.0, "poblacion": 334.9, "confed": "CONCACAF", "campeon": False, "k_noise": -0.10, "m2_noise": 0.20 },
    "Paraguay": { "grupo": "D", "ranking": 56, "pib": 5500, "temp": 22.0, "poblacion": 6.7, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.25, "m2_noise": 0.50 },
    "Australia": { "grupo": "D", "ranking": 24, "pib": 65000, "temp": 21.5, "poblacion": 26.0, "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15 },
    "Turquía": { "grupo": "D", "ranking": 40, "pib": 10000, "temp": 12.0, "poblacion": 85.3, "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25 },
    
    # --- GRUPO E ---
    "Alemania": { "grupo": "E", "ranking": 16, "pib": 48000, "temp": 8.5, "poblacion": 84.0, "confed": "UEFA", "campeon": True, "k_noise": 0.40, "m2_noise": 0.35 },
    "Curazao": { "grupo": "E", "ranking": 90, "pib": 16000, "temp": 27.5, "poblacion": 0.15, "confed": "CONCACAF", "campeon": False, "k_noise": 0.00, "m2_noise": 0.05 },
    "Costa de Marfil": { "grupo": "E", "ranking": 38, "pib": 2500, "temp": 26.0, "poblacion": 28.1, "confed": "CAF", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25 },
    "Ecuador": { "grupo": "E", "ranking": 29, "pib": 6300, "temp": 20.0, "poblacion": 18.0, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.25, "m2_noise": 0.35 },

    # --- GRUPO F ---
    "Países Bajos": { "grupo": "F", "ranking": 7, "pib": 57000, "temp": 10.0, "poblacion": 17.8, "confed": "UEFA", "campeon": False, "k_noise": 0.35, "m2_noise": 0.40 },
    "Japón": { "grupo": "F", "ranking": 18, "pib": 34000, "temp": 11.5, "poblacion": 124.6, "confed": "AFC", "campeon": False, "k_noise": 0.25, "m2_noise": 0.25 },
    "Suecia": { "grupo": "F", "ranking": 23, "pib": 56000, "temp": 6.5, "poblacion": 10.5, "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25 },
    "Túnez": { "grupo": "F", "ranking": 41, "pib": 3800, "temp": 19.5, "poblacion": 12.3, "confed": "CAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20 },

    # --- GRUPO G ---
    "Bélgica": { "grupo": "G", "ranking": 3, "pib": 50000, "temp": 10.0, "poblacion": 11.7, "confed": "UEFA", "campeon": False, "k_noise": 0.35, "m2_noise": 0.35 },
    "Egipto": { "grupo": "G", "ranking": 33, "pib": 3700, "temp": 22.0, "poblacion": 110.9, "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.25 },
    "Irán": { "grupo": "G", "ranking": 20, "pib": 4000, "temp": 18.0, "poblacion": 88.5, "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20 },
    "Nueva Zelanda": { "grupo": "G", "ranking": 103, "pib": 48000, "temp": 10.5, "poblacion": 5.1, "confed": "OFC", "campeon": False, "k_noise": 0.05, "m2_noise": 0.10 },

    # --- GRUPO H ---
    "España": { "grupo": "H", "ranking": 8, "pib": 30000, "temp": 13.5, "poblacion": 47.5, "confed": "UEFA", "campeon": True, "k_noise": 0.45, "m2_noise": 0.45 },
    "Cabo Verde": { "grupo": "H", "ranking": 65, "pib": 3900, "temp": 24.0, "poblacion": 0.6, "confed": "CAF", "campeon": False, "k_noise": 0.05, "m2_noise": 0.10 },
    "Arabia Saudita": { "grupo": "H", "ranking": 53, "pib": 30000, "temp": 25.5, "poblacion": 36.4, "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15 },
    "Uruguay": { "grupo": "H", "ranking": 11, "pib": 20000, "temp": 17.5, "poblacion": 3.4, "confed": "CONMEBOL", "campeon": True, "k_noise": 0.35, "m2_noise": 0.40 },

    # --- GRUPO I ---
    "Francia": { "grupo": "I", "ranking": 2, "pib": 43000, "temp": 11.5, "poblacion": 68.0, "confed": "UEFA", "campeon": True, "k_noise": 0.45, "m2_noise": 0.45 },
    "Senegal": { "grupo": "I", "ranking": 17, "pib": 1600, "temp": 28.0, "poblacion": 17.3, "confed": "CAF", "campeon": False, "k_noise": 0.25, "m2_noise": 0.30 },
    "Irak": { "grupo": "I", "ranking": 58, "pib": 4900, "temp": 22.5, "poblacion": 44.5, "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15 },
    "Noruega": { "grupo": "I", "ranking": 47, "pib": 89000, "temp": 2.0, "poblacion": 5.4, "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25 },

    # --- GRUPO J ---
    "Argentina": { "grupo": "J", "ranking": 1, "pib": 13000, "temp": 15.0, "poblacion": 46.2, "confed": "CONMEBOL", "campeon": True, "k_noise": 0.50, "m2_noise": 0.50 },
    "Argelia": { "grupo": "J", "ranking": 43, "pib": 4000, "temp": 22.5, "poblacion": 44.9, "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15 },
    "Austria": { "grupo": "J", "ranking": 25, "pib": 52000, "temp": 7.0, "poblacion": 9.0, "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.20 },
    "Jordania": { "grupo": "J", "ranking": 71, "pib": 4300, "temp": 19.0, "poblacion": 11.3, "confed": "AFC", "campeon": False, "k_noise": 0.05, "m2_noise": 0.10 },

    # --- GRUPO K ---
    "Portugal": { "grupo": "K", "ranking": 6, "pib": 25000, "temp": 15.0, "poblacion": 10.4, "confed": "UEFA", "campeon": False, "k_noise": 0.40, "m2_noise": 0.40 },
    "República Democrática del Congo": { "grupo": "K", "ranking": 61, "pib": 600, "temp": 24.0, "poblacion": 99.0, "confed": "CAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15 },
    "Uzbekistán": { "grupo": "K", "ranking": 64, "pib": 2300, "temp": 12.0, "poblacion": 36.0, "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15 },
    "Colombia": { "grupo": "K", "ranking": 12, "pib": 6600, "temp": 24.0, "poblacion": 51.8, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.30, "m2_noise": 0.40 },

    # --- GRUPO L ---
    "Inglaterra": { "grupo": "L", "ranking": 4, "pib": 46000, "temp": 9.5, "poblacion": 56.5, "confed": "UEFA", "campeon": True, "k_noise": 0.40, "m2_noise": 0.40 },
    "Croacia": { "grupo": "L", "ranking": 10, "pib": 20000, "temp": 12.0, "poblacion": 3.8, "confed": "UEFA", "campeon": False, "k_noise": 0.30, "m2_noise": 0.25 },
    "Ghana": { "grupo": "L", "ranking": 60, "pib": 2200, "temp": 27.0, "poblacion": 33.5, "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20 },
    "Panamá": { "grupo": "L", "ranking": 43, "pib": 18000, "temp": 27.0, "poblacion": 4.4, "confed": "CONCACAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20 }
}

# GENERACIÓN MATEMÁTICA EXACTA DE ENFRENTAMIENTOS ROUND-ROBIN POR GRUPO (72 PARTIDOS)
FIXTURE = []
match_id = 1
grupos = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

for g in grupos:
    eq_g = [name for name, info in TEAMS.items() if info["grupo"] == g]
    
    # Cruces oficiales estandarizados por la FIFA para las 3 jornadas de grupo
    cruces = [
        (eq_g[0], eq_g[1]), (eq_g[2], eq_g[3]),  # Jornada 1
        (eq_g[0], eq_g[2]), (eq_g[3], eq_g[1]),  # Jornada 2
        (eq_g[3], eq_g[0]), (eq_g[1], eq_g[2])   # Jornada 3
    ]
    
    for local, visitante in cruces:
        FIXTURE.append({
            "id": match_id,
            "grupo": g,
            "fase": f"Grupo {g}",
            "local": local,
            "visitante": visitante
        })
        match_id += 1
