import random
import string
from datetime import datetime, timezone

def get_rank_info(elo):
    # Formato: Nombre, Subtítulo, Icono, Color, Elo_Min, Elo_Max, Nivel_Interno
    if elo < 200: return ("Hierro I", "Iniciado", "⛓️", "#a19d94", 0, 200, 1)
    elif elo < 400: return ("Hierro II", "Novato", "⛓️", "#a19d94", 200, 400, 2)
    elif elo < 600: return ("Bronce I", "Aprendiz", "🥉", "#cd7f32", 400, 600, 3)
    elif elo < 800: return ("Bronce II", "Luchador", "🥉", "#cd7f32", 600, 800, 4)
    elif elo < 1100: return ("Plata I", "Guerrero", "🥈", "#c0c0c0", 800, 1100, 5)
    elif elo < 1400: return ("Plata II", "Veterano", "🥈", "#c0c0c0", 1100, 1400, 6)
    elif elo < 1800: return ("Oro I", "Élite", "🥇", "#ffd700", 1400, 1800, 7)
    elif elo < 2200: return ("Oro II", "Campeón", "🥇", "#ffd700", 1800, 2200, 8)
    elif elo < 2700: return ("Platino", "Comandante", "💎", "#00ced1", 2200, 2700, 9)
    elif elo < 3500: return ("Diamante", "Señor de la Guerra", "💠", "#b9f2ff", 2700, 3500, 10)
    else: return ("Mítico", "Leyenda Absoluta", "🔥", "#ff4b4b", 3500, 3500, 11)

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
