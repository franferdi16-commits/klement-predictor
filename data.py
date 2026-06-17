# data.py v2.0 - Base de datos oficial 48 selecciones + LIGA_INDEX real
# LIGA_INDEX: jugadores en plantilla del Mundial 2026 por tipo de liga
# top5_eur  = Premier League / La Liga / Bundesliga / Serie A / Ligue 1
# otra_eur  = Eredivisie, Primeira Liga, Süper Lig, Pro League, etc.
# local     = liga propia del país
# Fuente: plantillas oficiales FIFA 2026

LIGA_INDEX = {
    # ── UEFA (bonus bajo, sus ligas YA son las top5) ──────────────────────────
    "España":             {"top5_eur": 23, "otra_eur":  2, "local":  0},
    "Francia":            {"top5_eur": 21, "otra_eur":  3, "local":  0},
    "Inglaterra":         {"top5_eur": 24, "otra_eur":  1, "local":  0},
    "Alemania":           {"top5_eur": 22, "otra_eur":  3, "local":  0},
    "Portugal":           {"top5_eur": 18, "otra_eur":  5, "local":  2},
    "Bélgica":            {"top5_eur": 17, "otra_eur":  6, "local":  2},
    "Países Bajos":       {"top5_eur": 16, "otra_eur":  7, "local":  2},
    "Croacia":            {"top5_eur": 14, "otra_eur":  8, "local":  3},
    "Suecia":             {"top5_eur": 13, "otra_eur":  8, "local":  4},
    "Suiza":              {"top5_eur": 12, "otra_eur":  9, "local":  4},
    "Austria":            {"top5_eur": 11, "otra_eur":  9, "local":  5},
    "República Checa":    {"top5_eur":  9, "otra_eur": 10, "local":  6},
    "Noruega":            {"top5_eur": 11, "otra_eur":  8, "local":  6},
    "Escocia":            {"top5_eur": 10, "otra_eur":  8, "local":  7},
    "Bosnia y Herzegovina":{"top5_eur": 7, "otra_eur": 10, "local":  8},
    # ── CAF (el grupo más afectado por el sesgo PIB) ──────────────────────────
    "Marruecos":          {"top5_eur": 18, "otra_eur":  5, "local":  2},
    "Senegal":            {"top5_eur": 15, "otra_eur":  6, "local":  4},
    "Costa de Marfil":    {"top5_eur": 14, "otra_eur":  7, "local":  4},
    "Cabo Verde":         {"top5_eur": 19, "otra_eur":  4, "local":  2},  # casi toda en Europa
    "Nigeria":            {"top5_eur": 13, "otra_eur":  7, "local":  5},
    "Egipto":             {"top5_eur":  8, "otra_eur":  6, "local": 11},
    "Ghana":              {"top5_eur":  9, "otra_eur":  7, "local":  9},
    "Túnez":              {"top5_eur":  8, "otra_eur":  8, "local":  9},
    "República Democrática del Congo": {"top5_eur": 7, "otra_eur": 8, "local": 10},
    "Sudáfrica":          {"top5_eur":  3, "otra_eur":  5, "local": 17},
    # ── AFC ───────────────────────────────────────────────────────────────────
    "República de Corea": {"top5_eur": 14, "otra_eur":  6, "local":  5},
    "Japón":              {"top5_eur": 13, "otra_eur":  7, "local":  5},
    "Australia":          {"top5_eur":  9, "otra_eur":  8, "local":  8},
    "Uzbekistán":         {"top5_eur":  5, "otra_eur":  7, "local": 13},
    "Irán":               {"top5_eur":  3, "otra_eur":  5, "local": 17},
    "Arabia Saudita":     {"top5_eur":  2, "otra_eur":  3, "local": 20},
    "Catar":              {"top5_eur":  1, "otra_eur":  2, "local": 22},
    "Irak":               {"top5_eur":  2, "otra_eur":  5, "local": 18},
    "Jordania":           {"top5_eur":  2, "otra_eur":  4, "local": 19},
    "Nueva Zelanda":      {"top5_eur":  4, "otra_eur":  8, "local": 13},
    # ── CONCACAF ──────────────────────────────────────────────────────────────
    "Canadá":             {"top5_eur": 12, "otra_eur":  6, "local":  7},
    "Estados Unidos":     {"top5_eur":  9, "otra_eur":  5, "local": 11},
    "México":             {"top5_eur":  6, "otra_eur":  4, "local": 15},
    "Curazao":            {"top5_eur":  8, "otra_eur":  9, "local":  8},
    "Haití":              {"top5_eur":  5, "otra_eur":  7, "local": 13},
    "Panamá":             {"top5_eur":  3, "otra_eur":  6, "local": 16},
    # ── CONMEBOL ──────────────────────────────────────────────────────────────
    "Argentina":          {"top5_eur": 20, "otra_eur":  4, "local":  1},
    "Brasil":             {"top5_eur": 18, "otra_eur":  5, "local":  2},
    "Uruguay":            {"top5_eur": 15, "otra_eur":  6, "local":  4},
    "Colombia":           {"top5_eur": 12, "otra_eur":  7, "local":  6},
    "Ecuador":            {"top5_eur":  8, "otra_eur":  8, "local":  9},
    "Paraguay":           {"top5_eur":  5, "otra_eur":  7, "local": 13},
}

def calcular_bonus_diaspora(nombre_equipo):
    """
    Calcula el bonus de calidad real desde LIGA_INDEX.
    top5_eur vale 1.0 punto, otra_eur vale 0.5, local vale 0.0.
    Se normaliza sobre 25 jugadores y se escala a rango [0, 0.40].
    """
    li = LIGA_INDEX.get(nombre_equipo)
    if not li:
        return 0.0
    score = li["top5_eur"] * 1.0 + li["otra_eur"] * 0.5
    # Max teórico: 25 jugadores todos en top5 = 25.0
    normalizado = score / 25.0          # 0..1
    return round(min(0.40, normalizado * 0.40), 4)   # escala a 0..0.40


# ── EQUIPOS (48 selecciones oficiales) ────────────────────────────────────────
TEAMS = {
    # GRUPO A
    "México":             {"grupo":"A","ranking":15,"pib":11000,"temp":21.0,"poblacion":128.5,"confed":"CONCACAF","campeon":False,"k_noise":-0.15,"m2_noise":0.40},
    "Sudáfrica":          {"grupo":"A","ranking":59,"pib": 6000,"temp":17.5,"poblacion": 60.6,"confed":"CAF",     "campeon":False,"k_noise": 0.10,"m2_noise":0.20},
    "República de Corea": {"grupo":"A","ranking":22,"pib":32000,"temp":12.5,"poblacion": 51.7,"confed":"AFC",     "campeon":False,"k_noise": 0.10,"m2_noise":0.10},
    "República Checa":    {"grupo":"A","ranking":36,"pib":27000,"temp": 8.0,"poblacion": 10.8,"confed":"UEFA",    "campeon":False,"k_noise": 0.15,"m2_noise":0.15},
    # GRUPO B
    "Canadá":             {"grupo":"B","ranking":49,"pib":52000,"temp":-5.0,"poblacion": 38.9,"confed":"CONCACAF","campeon":False,"k_noise":-0.10,"m2_noise":0.20},
    "Bosnia y Herzegovina":{"grupo":"B","ranking":75,"pib": 9000,"temp":10.0,"poblacion":  3.2,"confed":"UEFA",   "campeon":False,"k_noise": 0.10,"m2_noise":0.15},
    "Catar":              {"grupo":"B","ranking":34,"pib":82000,"temp":27.0,"poblacion":  2.7,"confed":"AFC",     "campeon":False,"k_noise": 0.15,"m2_noise":0.20},
    "Suiza":              {"grupo":"B","ranking":19,"pib":93000,"temp": 5.5,"poblacion":  8.9,"confed":"UEFA",    "campeon":False,"k_noise": 0.20,"m2_noise":0.15},
    # GRUPO C
    "Brasil":             {"grupo":"C","ranking": 5,"pib":10000,"temp":25.0,"poblacion":215.3,"confed":"CONMEBOL","campeon":True, "k_noise": 0.40,"m2_noise":0.45},
    "Marruecos":          {"grupo":"C","ranking":13,"pib": 4000,"temp":17.5,"poblacion": 37.5,"confed":"CAF",     "campeon":False,"k_noise": 0.35,"m2_noise":0.35},
    "Haití":              {"grupo":"C","ranking":86,"pib": 1700,"temp":25.0,"poblacion": 11.7,"confed":"CONCACAF","campeon":False,"k_noise": 0.10,"m2_noise":0.30},
    "Escocia":            {"grupo":"C","ranking":39,"pib":42000,"temp": 8.0,"poblacion":  5.4,"confed":"UEFA",    "campeon":False,"k_noise": 0.15,"m2_noise":0.20},
    # GRUPO D
    "Estados Unidos":     {"grupo":"D","ranking":11,"pib":80000,"temp":12.0,"poblacion":334.9,"confed":"CONCACAF","campeon":False,"k_noise":-0.10,"m2_noise":0.20},
    "Paraguay":           {"grupo":"D","ranking":56,"pib": 5500,"temp":22.0,"poblacion":  6.7,"confed":"CONMEBOL","campeon":False,"k_noise": 0.25,"m2_noise":0.50},
    "Australia":          {"grupo":"D","ranking":24,"pib":65000,"temp":21.5,"poblacion": 26.0,"confed":"AFC",     "campeon":False,"k_noise": 0.15,"m2_noise":0.15},
    "Turquía":            {"grupo":"D","ranking":40,"pib":10000,"temp":12.0,"poblacion": 85.3,"confed":"UEFA",    "campeon":False,"k_noise": 0.20,"m2_noise":0.25},
    # GRUPO E
    "Alemania":           {"grupo":"E","ranking":16,"pib":48000,"temp": 8.5,"poblacion": 84.0,"confed":"UEFA",    "campeon":True, "k_noise": 0.40,"m2_noise":0.35},
    "Curazao":            {"grupo":"E","ranking":90,"pib":16000,"temp":27.5,"poblacion":  0.15,"confed":"CONCACAF","campeon":False,"k_noise": 0.00,"m2_noise":0.05},
    "Costa de Marfil":    {"grupo":"E","ranking":38,"pib": 2500,"temp":26.0,"poblacion": 28.1,"confed":"CAF",     "campeon":False,"k_noise": 0.20,"m2_noise":0.25},
    "Ecuador":            {"grupo":"E","ranking":29,"pib": 6300,"temp":20.0,"poblacion": 18.0,"confed":"CONMEBOL","campeon":False,"k_noise": 0.25,"m2_noise":0.35},
    # GRUPO F
    "Países Bajos":       {"grupo":"F","ranking": 7,"pib":57000,"temp":10.0,"poblacion": 17.8,"confed":"UEFA",    "campeon":False,"k_noise": 0.35,"m2_noise":0.40},
    "Japón":              {"grupo":"F","ranking":18,"pib":34000,"temp":11.5,"poblacion":124.6,"confed":"AFC",     "campeon":False,"k_noise": 0.25,"m2_noise":0.25},
    "Suecia":             {"grupo":"F","ranking":23,"pib":56000,"temp": 6.5,"poblacion": 10.5,"confed":"UEFA",    "campeon":False,"k_noise": 0.20,"m2_noise":0.25},
    "Túnez":              {"grupo":"F","ranking":41,"pib": 3800,"temp":19.5,"poblacion": 12.3,"confed":"CAF",     "campeon":False,"k_noise": 0.10,"m2_noise":0.20},
    # GRUPO G
    "Bélgica":            {"grupo":"G","ranking": 3,"pib":50000,"temp":10.0,"poblacion": 11.7,"confed":"UEFA",    "campeon":False,"k_noise": 0.35,"m2_noise":0.35},
    "Irán":               {"grupo":"G","ranking":20,"pib": 4000,"temp":18.0,"poblacion": 88.5,"confed":"AFC",     "campeon":False,"k_noise": 0.10,"m2_noise":0.20},
    "Egipto":             {"grupo":"G","ranking":33,"pib": 3700,"temp":22.0,"poblacion":110.9,"confed":"CAF",     "campeon":False,"k_noise": 0.15,"m2_noise":0.25},
    "Nueva Zelanda":      {"grupo":"G","ranking":103,"pib":48000,"temp":10.5,"poblacion":  5.1,"confed":"OFC",    "campeon":False,"k_noise": 0.05,"m2_noise":0.10},
    # GRUPO H
    "España":             {"grupo":"H","ranking": 8,"pib":30000,"temp":13.5,"poblacion": 47.5,"confed":"UEFA",    "campeon":True, "k_noise": 0.45,"m2_noise":0.45},
    "Uruguay":            {"grupo":"H","ranking":11,"pib":20000,"temp":17.5,"poblacion":  3.4,"confed":"CONMEBOL","campeon":True, "k_noise": 0.35,"m2_noise":0.40},
    "Arabia Saudita":     {"grupo":"H","ranking":53,"pib":30000,"temp":25.5,"poblacion": 36.4,"confed":"AFC",     "campeon":False,"k_noise": 0.10,"m2_noise":0.15},
    "Cabo Verde":         {"grupo":"H","ranking":65,"pib": 3900,"temp":24.0,"poblacion":  0.6,"confed":"CAF",     "campeon":False,"k_noise": 0.05,"m2_noise":0.10},
    # GRUPO I
    "Francia":            {"grupo":"I","ranking": 2,"pib":43000,"temp":11.5,"poblacion": 68.0,"confed":"UEFA",    "campeon":True, "k_noise": 0.45,"m2_noise":0.45},
    "Senegal":            {"grupo":"I","ranking":17,"pib": 1600,"temp":28.0,"poblacion": 17.3,"confed":"CAF",     "campeon":False,"k_noise": 0.25,"m2_noise":0.30},
    "Noruega":            {"grupo":"I","ranking":47,"pib":89000,"temp": 2.0,"poblacion":  5.4,"confed":"UEFA",    "campeon":False,"k_noise": 0.20,"m2_noise":0.25},
    "Irak":               {"grupo":"I","ranking":58,"pib": 4900,"temp":22.5,"poblacion": 44.5,"confed":"AFC",     "campeon":False,"k_noise": 0.10,"m2_noise":0.15},
    # GRUPO J
    "Argentina":          {"grupo":"J","ranking": 1,"pib":13000,"temp":15.0,"poblacion": 46.2,"confed":"CONMEBOL","campeon":True, "k_noise": 0.50,"m2_noise":0.50},
    "Austria":            {"grupo":"J","ranking":25,"pib":52000,"temp": 7.0,"poblacion":  9.0,"confed":"UEFA",    "campeon":False,"k_noise": 0.20,"m2_noise":0.20},
    "Argelia":            {"grupo":"J","ranking":43,"pib": 4000,"temp":22.5,"poblacion": 44.9,"confed":"CAF",     "campeon":False,"k_noise": 0.15,"m2_noise":0.15},
    "Jordania":           {"grupo":"J","ranking":71,"pib": 4300,"temp":19.0,"poblacion": 11.3,"confed":"AFC",     "campeon":False,"k_noise": 0.05,"m2_noise":0.10},
    # GRUPO K
    "Portugal":           {"grupo":"K","ranking": 6,"pib":25000,"temp":15.0,"poblacion": 10.4,"confed":"UEFA",    "campeon":False,"k_noise": 0.40,"m2_noise":0.40},
    "Colombia":           {"grupo":"K","ranking":12,"pib": 6600,"temp":24.0,"poblacion": 51.8,"confed":"CONMEBOL","campeon":False,"k_noise": 0.30,"m2_noise":0.40},
    "Uzbekistán":         {"grupo":"K","ranking":64,"pib": 2300,"temp":12.0,"poblacion": 36.0,"confed":"AFC",     "campeon":False,"k_noise": 0.10,"m2_noise":0.15},
    "República Democrática del Congo":{"grupo":"K","ranking":61,"pib":600,"temp":24.0,"poblacion":99.0,"confed":"CAF","campeon":False,"k_noise":0.10,"m2_noise":0.15},
    # GRUPO L
    "Inglaterra":         {"grupo":"L","ranking": 4,"pib":46000,"temp": 9.5,"poblacion": 56.5,"confed":"UEFA",    "campeon":True, "k_noise": 0.40,"m2_noise":0.40},
    "Croacia":            {"grupo":"L","ranking":10,"pib":20000,"temp":12.0,"poblacion":  3.8,"confed":"UEFA",    "campeon":False,"k_noise": 0.30,"m2_noise":0.25},
    "Ghana":              {"grupo":"L","ranking":60,"pib": 2200,"temp":27.0,"poblacion": 33.5,"confed":"CAF",     "campeon":False,"k_noise": 0.15,"m2_noise":0.20},
    "Panamá":             {"grupo":"L","ranking":43,"pib":18000,"temp":27.0,"poblacion":  4.4,"confed":"CONCACAF","campeon":False,"k_noise": 0.10,"m2_noise":0.20},
}

# ── FIXTURE (72 partidos round-robin) ─────────────────────────────────────────
FIXTURE = []
match_id = 1
for g in ["A","B","C","D","E","F","G","H","I","J","K","L"]:
    eq = [n for n, i in TEAMS.items() if i["grupo"] == g]
    for local, visitante in [
        (eq[0],eq[1]),(eq[2],eq[3]),
        (eq[0],eq[2]),(eq[3],eq[1]),
        (eq[3],eq[0]),(eq[1],eq[2]),
    ]:
        FIXTURE.append({"id":match_id,"grupo":g,"fase":f"Grupo {g}","local":local,"visitante":visitante})
        match_id += 1
