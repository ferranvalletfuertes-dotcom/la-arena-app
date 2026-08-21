import random
import string
from datetime import datetime, timezone

def get_rank_info(elo):
    if elo < 200: return ("Hierro III", "Esclavo", "🪨", "#7a7a7a", 0, 200, 1)
    elif elo < 300: return ("Hierro II", "Distraído", "⛓️", "#8f8f8f", 200, 300, 2)
    elif elo < 400: return ("Hierro I", "Despertando", "⚙️", "#a3a3a3", 300, 400, 3)
    elif elo < 600: return ("Bronce", "Guerrero", "🥉", "#cd7f32", 400, 600, 4)
    elif elo < 800: return ("Plata", "Dueño del Tiempo", "🥈", "#c0c0c0", 600, 800, 5)
    elif elo < 1000: return ("Oro", "Élite", "🥇", "#ffd700", 800, 1000, 6)
    else: return ("Diamante", "Intocable", "💎", "#00ffff", 1000, 1000, 7)

def calcular_rango(elo):
    info = get_rank_info(elo)
    return info[0], info[1], info[2], info[3]

def tiene_boost_activo(fecha_str):
    if not fecha_str: return False
    try:
        fecha_fin = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
        return datetime.now(timezone.utc) < fecha_fin
    except: return False

def calcular_monedas_base(elo):
    if elo < 200: return 10
    elif elo < 300: return 15
    elif elo < 400: return 20
    elif elo < 600: return 35
    elif elo < 800: return 50
    elif elo < 1000: return 75
    else: return 120

def calcular_riesgo_recompensa(segundos, elo_actual, boost_elo_str, boost_monedas_str):
    base_monedas = calcular_monedas_base(elo_actual)
    minutos = segundos // 60
    if minutos == 0: 
        p_elo = 5; c_elo = 5; coins = 1
    else:
        p_elo = int(minutos * 1.5)
        c_elo = int(minutos * 1.2)
        coins = int(base_monedas * (minutos / 25.0))
        
    if p_elo < 1: p_elo = 1
    if c_elo < 1: c_elo = 1
    if coins < 1: coins = 1

    if tiene_boost_activo(boost_elo_str): p_elo *= 2
    if tiene_boost_activo(boost_monedas_str): coins *= 2
    return p_elo, c_elo, coins

def generar_codigo_sala():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
