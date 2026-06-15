# data.py - Base de datos paramétrica oficial (48 Selecciones - 72 Partidos de Fase de Grupos)

TEAMS = {
    # GRUPO A
    "México": { "grupo": "A", "ranking": 15, "pib": 11000, "temp": 21.0, "poblacion": 128.5, "confed": "CONCACAF", "campeon": False, "k_noise": -0.15, "m2_noise": 0.40 },
    "Sudáfrica": { "grupo": "A", "ranking": 59, "pib": 6000, "temp": 17.5, "poblacion": 60.6, "confed": "CAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20 },
    "República de Corea": { "grupo": "A", "ranking": 22, "pib": 32000, "temp": 12.5, "poblacion": 51.7, "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.10 },
    "República Checa": { "grupo": "A", "ranking": 36, "pib": 27000, "temp": 8.0, "poblacion": 10.8, "confed": "UEFA", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15 },
    
    # GRUPO B
    "Canadá": { "grupo": "B", "ranking": 49, "pib": 52000, "temp": -5.0, "poblacion": 38.9, "confed": "CONCACAF", "campeon": False, "k_noise": -0.10, "m2_noise": 0.20 },
    "Bosnia y Herzegovina": { "grupo": "B", "ranking": 75, "pib": 9000, "temp": 10.0, "poblacion": 3.2, "confed": "UEFA", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15 },
    "Catar": { "grupo": "B", "ranking": 34, "pib": 82000, "temp": 27.0, "poblacion": 2.7, "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20 },
    "Suiza": { "grupo": "B", "ranking": 19, "pib": 93000, "temp": 5.5, "poblacion": 8.9, "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.15 },
    
    # GRUPO C
    "Brasil": { "grupo": "C", "ranking": 5, "pib": 10000, "temp": 25.0, "poblacion": 215.3, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.40, "m2_noise": 0.45 },
    "Marruecos": { "grupo": "C", "ranking": 13, "pib": 4000, "temp": 17.5, "poblacion": 37.5, "confed": "CAF", "campeon": False, "k_noise": 0.35, "m2_noise": 0.35 },
    "Haití": { "grupo": "C", "ranking": 86, "pib": 1700, "temp": 25.0, "poblacion": 11.7, "confed": "CONCACAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.30 },
    "Escocia": { "grupo": "C", "ranking": 39, "pib": 42000, "temp": 8.0, "poblacion": 5.4, "confed": "UEFA", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20 },
    
    # GRUPO D
    "Estados Unidos": { "grupo": "D", "ranking": 11, "pib": 80000, "temp": 12.0, "poblacion": 334.9, "confed": "CONCACAF", "campeon": False, "k_noise": -0.10, "m2_noise": 0.20 },
    "Paraguay": { "grupo": "D", "ranking": 56, "pib": 5500, "temp": 22.0, "poblacion": 6.7, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.25, "m2_noise": 0.50 },
    "Australia": { "grupo": "D", "ranking": 24, "pib": 65000, "temp": 21.5, "poblacion": 26.0, "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15 },
    "Turquía": { "grupo": "D", "ranking": 40, "pib": 10000, "temp": 12.0, "poblacion": 85.3, "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25 },
    
    # GRUPO E
    "Argentina": { "grupo": "E", "ranking": 1, "pib": 13000, "temp": 15.0, "poblacion": 46.2, "confed": "CONMEBOL", "campeon": True, "k_noise": 0.50, "m2_noise": 0.50 },
    "Jamaica": { "grupo": "E", "ranking": 55, "pib": 5500, "temp": 27.0, "poblacion": 2.8, "confed": "CONCACAF", "campeon": False, "k_noise": 0.05, "m2_noise": 0.15 },
    "Irán": { "grupo": "E", "ranking": 20, "pib": 4000, "temp": 18.0, "poblacion": 88.5, "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20 },
    "Argelia": { "grupo": "E", "ranking": 43, "pib": 4000, "temp": 22.5, "poblacion": 44.9, "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15 },

    # GRUPO F
    "Francia": { "grupo": "F", "ranking": 2, "pib": 43000, "temp": 11.5, "poblacion": 68.0, "confed": "UEFA", "campeon": True, "k_noise": 0.45, "m2_noise": 0.45 },
    "Angola": { "grupo": "F", "ranking": 85, "pib": 2000, "temp": 22.0, "poblacion": 35.6, "confed": "CAF", "campeon": False, "k_noise": 0.05, "m2_noise": 0.10 },
    "Perú": { "grupo": "F", "ranking": 31, "pib": 7000, "temp": 20.0, "poblacion": 34.0, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.20, "m2_noise": 0.30 },
    "Uzbekistán": { "grupo": "F", "ranking": 64, "pib": 2300, "temp": 12.0, "poblacion": 36.0, "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15 },

    # GRUPO G
    "Inglaterra": { "grupo": "G", "ranking": 4, "pib": 46000, "temp": 9.5, "poblacion": 56.5, "confed": "UEFA", "campeon": True, "k_noise": 0.40, "m2_noise": 0.40 },
    "Ecuador": { "grupo": "G", "ranking": 29, "pib": 6300, "temp": 20.0, "poblacion": 18.0, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.25, "m2_noise": 0.35 },
    "Túnez": { "grupo": "G", "ranking": 41, "pib": 3800, "temp": 19.5, "poblacion": 12.3, "confed": "CAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20 },
    "Omán": { "grupo": "G", "ranking": 77, "pib": 21000, "temp": 26.0, "poblacion": 4.5, "confed": "AFC", "campeon": False, "k_noise": 0.05, "m2_noise": 0.10 },

    # GRUPO H
    "Bélgica": { "grupo": "H", "ranking": 3, "pib": 50000, "temp": 10.0, "poblacion": 11.7, "confed": "UEFA", "campeon": False, "k_noise": 0.35, "m2_noise": 0.35 },
    "Chile": { "grupo": "H", "ranking": 42, "pib": 15000, "temp": 14.0, "poblacion": 19.6, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.20, "m2_noise": 0.30 },
    "Egipto": { "grupo": "H", "ranking": 33, "pib": 3700, "temp": 22.0, "poblacion": 110.9, "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.25 },
    "Curazao": { "grupo": "H", "ranking": 90, "pib": 16000, "temp": 27.5, "poblacion": 0.15, "confed": "CONCACAF", "campeon": False, "k_noise": 0.00, "m2_noise": 0.05 },

    # GRUPO I
    "Portugal": { "grupo": "I", "ranking": 6, "pib": 25000, "temp": 15.0, "poblacion": 10.4, "confed": "UEFA", "campeon": False, "k_noise": 0.40, "m2_noise": 0.40 },
    "Colombia": { "grupo": "I", "ranking": 12, "pib": 6600, "temp": 24.0, "poblacion": 51.8, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.30, "m2_noise": 0.40 },
    "Camerún": { "grupo": "I", "ranking": 46, "pib": 1600, "temp": 24.5, "poblacion": 27.9, "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20 },
    "Nueva Zelanda": { "grupo": "I", "ranking": 103, "pib": 48000, "temp": 10.5, "poblacion": 5.1, "confed": "OFC", "campeon": False, "k_noise": 0.05, "m2_noise": 0.10 },

    # GRUPO J
    "España": { "grupo": "J", "ranking": 8, "pib": 30000, "temp": 13.5, "poblacion": 47.5, "confed": "UEFA", "campeon": True, "k_noise": 0.45, "m2_noise": 0.45 },
    "Uruguay": { "grupo": "J", "ranking": 11, "pib": 20000, "temp": 17.5, "poblacion": 3.4, "confed": "CONMEBOL", "campeon": True, "k_noise": 0.35, "m2_noise": 0.40 },
    "Costa de Marfil": { "grupo": "J", "ranking": 38, "pib": 2500, "temp": 26.0, "poblacion": 28.1, "confed": "CAF", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25 },
    "Honduras": { "grupo": "J", "ranking": 78, "pib": 3000, "temp": 25.0, "poblacion": 10.4, "confed": "CONCACAF", "campeon": False, "k_noise": 0.05, "m2_noise": 0.15 },

    # GRUPO K
    "Italia": { "grupo": "K", "ranking": 9, "pib": 35000, "temp": 13.0, "poblacion": 58.9, "confed": "UEFA", "campeon": True, "k_noise": 0.40, "m2_noise": 0.40 },
    "Japón": { "grupo": "K", "ranking": 18, "pib": 34000, "temp": 11.5, "poblacion": 124.6, "confed": "AFC", "campeon": False, "k_noise": 0.25, "m2_noise": 0.25 },
    "Nigeria": { "grupo": "K", "ranking": 28, "pib": 2200, "temp": 27.0, "poblacion": 218.5, "confed": "CAF", "campeon": False, "k_noise": 0.20, "m2_noise": 0.30 },
    "Venezuela": { "grupo": "K", "ranking": 52, "pib": 3500, "temp": 25.0, "poblacion": 28.3, "confed": "CONMEBOL", "campeon": False, "k_noise": 0.15, "m2_noise": 0.35 },

    # GRUPO L
    "Alemania": { "grupo": "L", "ranking": 16, "pib": 48000, "temp": 8.5, "poblacion": 84.0, "confed": "UEFA", "campeon": True, "k_noise": 0.40, "m2_noise": 0.35 },
    "Croacia": { "grupo": "L", "ranking": 10, "pib": 20000, "temp": 12.0, "poblacion": 3.8, "confed": "UEFA", "campeon": False, "k_noise": 0.30, "m2_noise": 0.25 },
    "Panamá": { "grupo": "L", "ranking": 43, "pib": 18000, "temp": 27.0, "poblacion": 4.4, "confed": "CONCACAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.20 },
    "Ghana": { "grupo": "L", "ranking": 60, "pib": 2200, "temp": 27.0, "poblacion": 33.5, "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20 }
}

FIXTURE = []
match_id = 1

# Algoritmo matemático estricto Round-Robin para generar los 6 partidos exactos por cada uno de los 12 grupos
grupos = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
for g in grupos:
    # Filtramos los 4 equipos del grupo actual preservando el orden de inserción
    equipos_grupo = [name for name, info in TEAMS.items() if info["grupo"] == g]
    
    # Combinatorias oficiales Round-Robin de 4 elementos (6 emparejamientos por grupo)
    combinaciones = [
        (equipos_grupo[0], equipos_grupo[1]), # Fecha 1
        (equipos_grupo[2], equipos_grupo[3]),
        (equipos_grupo[0], equipos_grupo[2]), # Fecha 2
        (equipos_grupo[3], equipos_grupo[1]),
        (equipos_grupo[3], equipos_grupo[0]), # Fecha 3
        (equipos_grupo[1], equipos_grupo[2])
    ]
    
    for local, visitante in combinaciones:
        FIXTURE.append({
            "id": match_id,
            "grupo": g,
            "fase": f"Grupo {g}",
            "local": local,
            "visitante": visitante
        })
        match_id += 1
