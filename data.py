# data.py - Base de Datos Macroeconómica, Demográfica y Climática Oficial

TEAMS = {
    # --- GRUPO A ---
    "México": {
        "ranking": 15, "pib": 11000, "temp": 21.0, "poblacion": 128.5, 
        "confed": "CONCACAF", "campeon": False, "k_noise": -0.15, "m2_noise": 0.40
    },
    "República de Corea": {
        "ranking": 22, "pib": 32000, "temp": 12.5, "poblacion": 51.7, 
        "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.10
    },
    "República Checa": {
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
    "Bosnia y Herzegovina": {
        "ranking": 75, "pib": 9000, "temp": 10.0, "poblacion": 3.2, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15
    },
    "Catar": {
        "ranking": 34, "pib": 82000, "temp": 27.0, "poblacion": 2.7, 
        "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20
    },
    "Suiza": {
        "ranking": 19, "pib": 93000, "temp": 5.5, "poblacion": 8.9, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.15
    },
    
    # --- GRUPO C ---
    "Brasil": {
        "ranking": 5, "pib": 10000, "temp": 25.0, "poblacion": 215.3, 
        "confed": "CONMEBOL", "campeon": False, "k_noise": 0.40, "m2_noise": 0.45
    },
    "Marruecos": {
        "ranking": 13, "pib": 4000, "temp": 17.5, "poblacion": 37.5, 
        "confed": "CAF", "campeon": False, "k_noise": 0.35, "m2_noise": 0.35
    },
    "Haití": {
        "ranking": 86, "pib": 1700, "temp": 25.0, "poblacion": 11.7, 
        "confed": "CONCACAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.30
    },
    "Escocia": {
        "ranking": 39, "pib": 42000, "temp": 8.0, "poblacion": 5.4, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20
    },

    # --- GRUPO D ---
    "Estados Unidos": {
        "ranking": 11, "pib": 80000, "temp": 12.0, "poblacion": 334.9, 
        "confed": "CONCACAF", "campeon": False, "k_noise": -0.10, "m2_noise": 0.20
    },
    "Paraguay": {
        "ranking": 56, "pib": 5500, "temp": 22.0, "poblacion": 6.7, 
        "confed": "CONMEBOL", "campeon": False, "k_noise": 0.25, "m2_noise": 0.50
    },
    "Australia": {
        "ranking": 24, "pib": 65000, "temp": 21.5, "poblacion": 26.0, 
        "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15
    },
    "Turquía": {
        "ranking": 40, "pib": 10000, "temp": 12.0, "poblacion": 85.3, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25
    },

    # --- GRUPO E ---
    "Alemania": {
        "ranking": 16, "pib": 48000, "temp": 8.5, "poblacion": 84.4, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.25, "m2_noise": 0.20
    },
    "Curazao": {
        "ranking": 90, "pib": 15000, "temp": 28.0, "poblacion": 0.15, 
        "confed": "CONCACAF", "campeon": False, "k_noise": 0.05, "m2_noise": 0.10
    },
    "Costa de Marfil": {
        "ranking": 38, "pib": 2500, "temp": 26.0, "poblacion": 28.1, 
        "confed": "CAF", "campeon": False, "k_noise": 0.20, "m2_noise": 0.30
    },
    "Ecuador": {
        "ranking": 31, "pib": 6300, "temp": 21.5, "poblacion": 18.0, 
        "confed": "CONMEBOL", "campeon": False, "k_noise": 0.25, "m2_noise": 0.45
    },

    # --- GRUPO F ---
    "Países Bajos": {
        "ranking": 7, "pib": 62000, "temp": 10.0, "poblacion": 18.0, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.20
    },
    "Japón": {
        "ranking": 18, "pib": 34000, "temp": 11.5, "poblacion": 125.1, 
        "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15
    },
    "Suecia": {
        "ranking": 28, "pib": 56000, "temp": 2.0, "poblacion": 10.5, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15
    },
    "Túnez": {
        "ranking": 41, "pib": 3800, "temp": 19.0, "poblacion": 12.4, 
        "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20
    },

    # --- GRUPO G ---
    "Bélgica": {
        "ranking": 3, "pib": 53000, "temp": 10.0, "poblacion": 11.7, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.25, "m2_noise": 0.20
    },
    "Egipto": {
        "ranking": 36, "pib": 3500, "temp": 22.0, "poblacion": 111.0, 
        "confed": "CAF", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25
    },
    "RI de Irán": {
        "ranking": 20, "pib": 4000, "temp": 17.0, "poblacion": 88.5, 
        "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20
    },
    "Nueva Zelanda": {
        "ranking": 103, "pib": 48000, "temp": 10.5, "poblacion": 5.1, 
        "confed": "OFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.10
    },

    # --- GRUPO H ---
    "España": {
        "ranking": 3, "pib": 32000, "temp": 14.5, "poblacion": 48.0, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.30, "m2_noise": 0.30
    },
    "Cabo Verde": {
        "ranking": 65, "pib": 3900, "temp": 24.0, "poblacion": 0.6, 
        "confed": "CAF", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15
    },
    "Arabia Saudí": {
        "ranking": 53, "pib": 30000, "temp": 25.5, "poblacion": 36.4, 
        "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20
    },
    "Uruguay": {
        "ranking": 11, "pib": 20000, "temp": 17.5, "poblacion": 3.4, 
        "confed": "CONMEBOL", "campeon": False, "k_noise": 0.35, "m2_noise": 0.40
    },

    # --- GRUPO I ---
    "Francia": {
        "ranking": 2, "pib": 45000, "temp": 11.0, "poblacion": 68.0, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.30, "m2_noise": 0.30
    },
    "Senegal": {
        "ranking": 17, "pib": 1600, "temp": 28.0, "poblacion": 17.3, 
        "confed": "CAF", "campeon": False, "k_noise": 0.25, "m2_noise": 0.30
    },
    "Irak": {
        "ranking": 58, "pib": 5000, "temp": 22.5, "poblacion": 44.5, 
        "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.20
    },
    "Noruega": {
        "ranking": 47, "pib": 106000, "temp": 2.0, "poblacion": 5.4, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.15
    },

    # --- GRUPO J ---
    "Argentina": {
        "ranking": 1, "pib": 13000, "temp": 14.0, "poblacion": 46.2, 
        "confed": "CONMEBOL", "campeon": True, "k_noise": 0.40, "m2_noise": 0.50
    },
    "Argelia": {
        "ranking": 43, "pib": 4300, "temp": 22.5, "poblacion": 44.9, 
        "confed": "CAF", "campeon": False, "k_noise": 0.20, "m2_noise": 0.25
    },
    "Austria": {
        "ranking": 25, "pib": 52000, "temp": 7.5, "poblacion": 9.1, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.20, "m2_noise": 0.15
    },
    "Jordania": {
        "ranking": 71, "pib": 4300, "temp": 18.0, "poblacion": 11.3, 
        "confed": "AFC", "campeon": False, "k_noise": 0.10, "m2_noise": 0.15
    },

    # --- GRUPO K ---
    "Portugal": {
        "ranking": 6, "pib": 26000, "temp": 15.5, "poblacion": 10.4, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.25, "m2_noise": 0.25
    },
    "RD Congo": {
        "ranking": 63, "pib": 650, "temp": 24.0, "poblacion": 99.0, 
        "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.25
    },
    "Uzbekistán": {
        "ranking": 66, "pib": 2300, "temp": 12.0, "poblacion": 36.0, 
        "confed": "AFC", "campeon": False, "k_noise": 0.15, "m2_noise": 0.15
    },
    "Colombia": {
        "ranking": 12, "pib": 6500, "temp": 22.0, "poblacion": 51.5, 
        "confed": "CONMEBOL", "campeon": False, "k_noise": 0.30, "m2_noise": 0.50
    },

    # --- GRUPO L ---
    "Inglaterra": {
        "ranking": 4, "pib": 46000, "temp": 10.5, "poblacion": 56.5, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.25, "m2_noise": 0.20
    },
    "Croacia": {
        "ranking": 10, "pib": 20000, "temp": 12.5, "poblacion": 3.8, 
        "confed": "UEFA", "campeon": False, "k_noise": 0.30, "m2_noise": 0.25
    },
    "Ghana": {
        "ranking": 61, "pib": 2200, "temp": 27.0, "poblacion": 33.4, 
        "confed": "CAF", "campeon": False, "k_noise": 0.15, "m2_noise": 0.25
    },
    "Panamá": {
        "ranking": 44, "pib": 17000, "temp": 27.0, "poblacion": 4.4, 
        "confed": "CONCACAF", "campeon": False, "k_noise": 0.20, "m2_noise": 0.30
    }
}

FIXTURE = [
    # --- JORNADA 1 ---
    {"id": 1, "grupo": "A", "fase": "Grupo A", "local": "México", "visitante": "Sudáfrica"},
    {"id": 2, "grupo": "A", "fase": "Grupo A", "local": "República de Corea", "visitante": "República Checa"},
    {"id": 3, "grupo": "B", "fase": "Grupo B", "local": "Canadá", "visitante": "Bosnia y Herzegovina"},
    {"id": 4, "grupo": "D", "fase": "Grupo D", "local": "Estados Unidos", "visitante": "Paraguay"},
    {"id": 5, "grupo": "B", "fase": "Grupo B", "local": "Catar", "visitante": "Suiza"},
    {"id": 6, "grupo": "C", "fase": "Grupo C", "local": "Brasil", "visitante": "Marruecos"},
    {"id": 7, "grupo": "C", "fase": "Grupo C", "local": "Haití", "visitante": "Escocia"},
    {"id": 8, "grupo": "D", "fase": "Grupo D", "local": "Australia", "visitante": "Turquía"},
    {"id": 9, "grupo": "E", "fase": "Grupo E", "local": "Alemania", "visitante": "Curazao"},
    {"id": 10, "grupo": "F", "fase": "Grupo F", "local": "Países Bajos", "visitante": "Japón"},
    {"id": 11, "grupo": "E", "fase": "Grupo E", "local": "Costa de Marfil", "visitante": "Ecuador"},
    {"id": 12, "grupo": "F", "fase": "Grupo F", "local": "Suecia", "visitante": "Túnez"},
{"id": 13, "grupo": "H", "fase": "Grupo H", "local": "España", "visitante": "Cabo Verde"},{"id": 14, "grupo": "G", "fase": "Grupo G", "local": "Bélgica", "visitante": "Egipto"},{"id": 15, "grupo": "H", "fase": "Grupo H", "local": "Arabia Saudí", "visitante": "Uruguay"},{"id": 16, "grupo": "G", "fase": "Grupo G", "local": "RI de Irán", "visitante": "Nueva Zelanda"},{"id": 17, "grupo": "I", "fase": "Grupo I", "local": "Francia", "visitante": "Senegal"},{"id": 18, "grupo": "I", "fase": "Grupo I", "local": "Irak", "visitante": "Noruega"},{"id": 19, "grupo": "J", "fase": "Grupo J", "local": "Argentina", "visitante": "Argelia"},{"id": 20, "grupo": "J", "fase": "Grupo J", "local": "Austria", "visitante": "Jordania"},{"id": 21, "grupo": "K", "fase": "Grupo K", "local": "Portugal", "visitante": "RD Congo"},{"id": 22, "grupo": "L", "fase": "Grupo L", "local": "Inglaterra", "visitante": "Croacia"},{"id": 23, "grupo": "L", "fase": "Grupo L", "local": "Ghana", "visitante": "Panamá"},{"id": 24, "grupo": "K", "fase": "Grupo K", "local": "Uzbekistán", "visitante": "Colombia"},# --- JORNADA 2 ---{"id": 25, "grupo": "A", "fase": "Grupo A", "local": "República Checa", "visitante": "Sudáfrica"},{"id": 26, "grupo": "B", "fase": "Grupo B", "local": "Suiza", "visitante": "Bosnia y Herzegovina"},{"id": 27, "grupo": "B", "fase": "Grupo B", "local": "Canadá", "visitante": "Catar"},{"id": 28, "grupo": "A", "fase": "Grupo A", "local": "México", "visitante": "República de Corea"},{"id": 29, "grupo": "D", "fase": "Grupo D", "local": "Estados Unidos", "visitante": "Australia"},{"id": 30, "grupo": "C", "fase": "Grupo C", "local": "Escocia", "visitante": "Marruecos"},{"id": 31, "grupo": "C", "fase": "Grupo C", "local": "Brasil", "visitante": "Haití"},{"id": 32, "grupo": "D", "fase": "Grupo D", "local": "Turquía", "visitante": "Paraguay"},{"id": 33, "grupo": "F", "fase": "Grupo F", "local": "Países Bajos", "visitante": "Suecia"},{"id": 34, "grupo": "E", "fase": "Grupo E", "local": "Alemania", "visitante": "Costa de Marfil"},{"id": 35, "grupo": "E", "fase": "Grupo E", "local": "Ecuador", "visitante": "Curazao"},{"id": 36, "grupo": "F", "fase": "Grupo F", "local": "Túnez", "visitante": "Japón"},{"id": 37, "grupo": "H", "fase": "Grupo H", "local": "España", "visitante": "Arabia Saudí"},{"id": 38, "grupo": "G", "fase": "Grupo G", "local": "Bélgica", "visitante": "RI de Irán"},{"id": 39, "grupo": "H", "fase": "Grupo H", "local": "Uruguay", "visitante": "Cabo Verde"},{"id": 40, "grupo": "G", "fase": "Grupo G", "local": "Nueva Zelanda", "visitante": "Egipto"},{"id": 41, "grupo": "J", "fase": "Grupo J", "local": "Argentina", "visitante": "Austria"},{"id": 42, "grupo": "I", "fase": "Grupo I", "local": "Francia", "visitante": "Irak"},{"id": 43, "grupo": "I", "fase": "Grupo I", "local": "Noruega", "visitante": "Senegal"},{"id": 44, "grupo": "J", "fase": "Grupo J", "local": "Jordania", "visitante": "Argelia"},{"id": 45, "grupo": "K", "fase": "Grupo K", "local": "Portugal", "visitante": "Uzbekistán"},{"id": 46, "grupo": "L", "fase": "Grupo L", "local": "Inglaterra", "visitante": "Ghana"},{"id": 47, "grupo": "L", "fase": "Grupo L", "local": "Panamá", "visitante": "Croacia"},{"id": 48, "grupo": "K", "fase": "Grupo K", "local": "Colombia", "visitante": "RD Congo"},# --- JORNADA 3 (Miércoles 24 de Junio) ---{"id": 49, "grupo": "B", "fase": "Grupo B", "local": "Suiza", "visitante": "Canadá"},{"id": 50, "grupo": "B", "fase": "Grupo B", "local": "Bosnia y Herzegovina", "visitante": "Catar"},{"id": 51, "grupo": "C", "fase": "Grupo C", "local": "Escocia", "visitante": "Brasil"},{"id": 52, "grupo": "C", "fase": "Grupo C", "local": "Marruecos", "visitante": "Haití"},{"id": 53, "grupo": "A", "fase": "Grupo A", "local": "República Checa", "visitante": "México"},{"id": 54, "grupo": "A", "fase": "Grupo A", "local": "Sudáfrica", "visitante": "República de Corea"},# --- JORNADA 3 (Jueves 25 de Junio) ---{"id": 55, "grupo": "E", "fase": "Grupo E", "local": "Curazao", "visitante": "Costa de Marfil"},{"id": 56, "grupo": "E", "fase": "Grupo E", "local": "Ecuador", "visitante": "Alemania"},{"id": 57, "grupo": "F", "fase": "Grupo F", "local": "Japón", "visitante": "Suecia"},{"id": 58, "grupo": "F", "fase": "Grupo F", "local": "Túnez", "visitante": "Países Bajos"},{"id": 59, "grupo": "D", "fase": "Grupo D", "local": "Turquía", "visitante": "Estados Unidos"},{"id": 60, "grupo": "D", "fase": "Grupo D", "local": "Paraguay", "visitante": "Australia"}]
