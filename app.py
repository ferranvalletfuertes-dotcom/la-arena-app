import streamlit as st
import time
import random
import string
from datetime import datetime, timedelta, timezone
import streamlit.components.v1 as components
from supabase import create_client, Client

st.set_page_config(page_title="Modo Combate | La Arena", layout="centered")

# --- INYECCIÓN DE CSS Y ANIMACIONES ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stButton > button[data-baseweb="button"] {
        background-color: #ff4b4b; 
        color: white; 
        border-radius: 8px; 
        border: none;
        padding: 10px 24px; 
        font-weight: 900; 
        letter-spacing: 1px; 
        text-transform: uppercase;
        transition: all 0.3s ease; 
        box-shadow: 0 4px 10px rgba(255, 75, 75, 0.2);
    }
    
    .stButton > button[data-baseweb="button"]:hover {
        background-color: #ff1a1a; 
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.6); 
        transform: scale(1.02);
    }
    
    .nav-btn > button[data-baseweb="button"] {
        background-color: #1a1a1a !important; 
        border: 1px solid #333 !important;
        color: #888 !important; 
        box-shadow: none !important;
    }
    
    .nav-btn > button[data-baseweb="button"]:hover {
        color: #fff !important; 
        border-color: #ff4b4b !important; 
        background-color: #222 !important;
        transform: none !important;
    }
    
    div[data-testid="stExpander"] { 
        background-color: #161616; 
        border: 1px solid #333; 
        border-radius: 8px; 
    }
    
    .epic-title { 
        text-align: center; 
        color: #ff4b4b; 
        font-size: 4em; 
        text-transform: uppercase; 
        letter-spacing: 4px; 
        text-shadow: 0 0 25px rgba(255,75,75,0.7); 
        margin-bottom: 0px; 
    }
    
    .manifesto { 
        color: #a3a3a3; 
        font-size: 1.2em; 
        text-align: center; 
        font-style: italic; 
        margin-top: 10px; 
        margin-bottom: 40px; 
        line-height: 1.6; 
    }
    
    .highlight { 
        color: #ffffff; 
        font-weight: bold; 
        text-shadow: 0 0 5px rgba(255,255,255,0.3); 
    }
    
    .stTextInput > div > div > input { 
        background-color: #111 !important; 
        color: #00ff00 !important; 
        border: 1px solid #333 !important; 
        font-family: monospace; 
        text-align: center;
        font-weight: bold;
    }

    .neon-red { color: #ff4b4b; text-shadow: 0 0 10px rgba(255, 75, 75, 0.8); font-weight: 900; }
    .neon-green { color: #00ff00; text-shadow: 0 0 10px rgba(0, 255, 0, 0.8); font-weight: 900; }
    
    .rules-box { 
        border: 1px solid #ff4b4b; 
        background-color: #110000; 
        padding: 20px; 
        border-radius: 8px; 
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.3); 
        margin-top: 25px; 
        margin-bottom: 25px; 
    }

    @keyframes float-card {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes pulse-aura {
        0% { box-shadow: 0 0 15px #ff0000, 0 0 5px #ff0000 inset; }
        50% { box-shadow: 0 0 35px #ff0000, 0 0 15px #ff0000 inset; }
        100% { box-shadow: 0 0 15px #ff0000, 0 0 5px #ff0000 inset; }
    }
    
    @keyframes pulse-fuego {
        0% { box-shadow: 0 0 15px #aa00ff, 0 0 5px #aa00ff inset; }
        50% { box-shadow: 0 0 35px #aa00ff, 0 0 15px #aa00ff inset; }
        100% { box-shadow: 0 0 15px #aa00ff, 0 0 5px #aa00ff inset; }
    }
    
    @keyframes pulse-sombra {
        0% { box-shadow: 0 0 15px #00aaff, 0 0 5px #00aaff inset; }
        50% { box-shadow: 0 0 35px #00aaff, 0 0 15px #00aaff inset; }
        100% { box-shadow: 0 0 15px #00aaff, 0 0 5px #00aaff inset; }
    }
    
    @keyframes chest-shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(3px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(3px, 1px) rotate(-1deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        90% { transform: translate(1px, 2px) rotate(0deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    
    @keyframes rank-up-pop {
        0% { transform: scale(0.5); opacity: 0; }
        70% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }

    .fut-card { 
        transition: filter 0.3s ease; 
    }
    
    .fut-card:hover { 
        filter: brightness(1.2); 
        cursor: pointer; 
    }
    
    .anim-float { 
        animation: float-card 3.5s ease-in-out infinite; 
    }
    
    .anim-aura { 
        animation: float-card 3.5s ease-in-out infinite, pulse-aura 2s infinite !important; 
        border: 2px solid #ff0000 !important; 
    }
    
    .anim-fuego { 
        animation: float-card 3.5s ease-in-out infinite, pulse-fuego 2s infinite !important; 
        border: 2px solid #aa00ff !important; 
    }
    
    .anim-sombra { 
        animation: float-card 3.5s ease-in-out infinite, pulse-sombra 2s infinite !important; 
        border: 2px solid #00aaff !important; 
    }
    
    .chest-anim { 
        font-size: 100px; 
        animation: chest-shake 0.5s infinite; 
        text-align: center; 
        margin: 20px 0; 
        text-shadow: 0 0 30px #ffd700; 
    }
    
    .rank-up-box {
        animation: rank-up-pop 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    </style>
""".replace('\n', ''), unsafe_allow_html=True)

# --- CONEXIÓN A LA BÓVEDA ---
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

try:
    supabase: Client = init_connection()
except Exception as e:
    st.error("❌ Fallo crítico: No se pudo conectar a la base de datos.")
    st.stop()

# --- MEMORIA ABSOLUTA Y EXPANDIDA ---
if 'usuario_id' not in st.session_state:
    st.session_state.usuario_id = None
if 'estado' not in st.session_state:
    st.session_state.estado = "login"
if 'puntos_elo' not in st.session_state:
    st.session_state.puntos_elo = 100
if 'racha' not in st.session_state:
    st.session_state.racha = 0
if 'monedas' not in st.session_state:
    st.session_state.monedas = 0
if 'nombre_guerra' not in st.session_state:
    st.session_state.nombre_guerra = ""
if 'ultima_pildora' not in st.session_state:
    st.session_state.ultima_pildora = None
if 'partida_id' not in st.session_state:
    st.session_state.partida_id = None
if 'inicio_busqueda' not in st.session_state:
    st.session_state.inicio_busqueda = 0
if 'rival_nombre' not in st.session_state:
    st.session_state.rival_nombre = "Desconocido"
if 'rival_elo' not in st.session_state:
    st.session_state.rival_elo = 100
if 'monedas_ganadas_recientes' not in st.session_state:
    st.session_state.monedas_ganadas_recientes = 0
if 'mision_actual' not in st.session_state:
    st.session_state.mision_actual = ""
if 'rival_mision' not in st.session_state:
    st.session_state.rival_mision = "Desconocido"
if 'tiempo_combate' not in st.session_state:
    st.session_state.tiempo_combate = 10
if 'elo_premio' not in st.session_state:
    st.session_state.elo_premio = 0
if 'elo_castigo' not in st.session_state:
    st.session_state.elo_castigo = 0
if 'skin_activa' not in st.session_state:
    st.session_state.skin_activa = 'default'
if 'inv_aura' not in st.session_state:
    st.session_state.inv_aura = False
if 'inv_corona' not in st.session_state:
    st.session_state.inv_corona = False
if 'inv_sombra' not in st.session_state:
    st.session_state.inv_sombra = False
if 'inv_fuego' not in st.session_state:
    st.session_state.inv_fuego = False
if 'boost_elo' not in st.session_state:
    st.session_state.boost_elo = None
if 'boost_monedas' not in st.session_state:
    st.session_state.boost_monedas = None
if 'rival_skin' not in st.session_state:
    st.session_state.rival_skin = 'default'
if 'tipo_partida' not in st.session_state:
    st.session_state.tipo_partida = "publica"
if 'codigo_sala' not in st.session_state:
    st.session_state.codigo_sala = ""
if 'premio_cofre' not in st.session_state:
    st.session_state.premio_cofre = ""
if 'premio_duplicado' not in st.session_state:
    st.session_state.premio_duplicado = False

# NUEVAS VARIABLES PARA EL CUARTEL GENERAL (ESTADÍSTICAS)
if 'victorias' not in st.session_state:
    st.session_state.victorias = 0
if 'derrotas' not in st.session_state:
    st.session_state.derrotas = 0
if 'minutos_focus' not in st.session_state:
    st.session_state.minutos_focus = 0
if 'rango_alcanzado_nombre' not in st.session_state:
    st.session_state.rango_alcanzado_nombre = ""
if 'rango_alcanzado_color' not in st.session_state:
    st.session_state.rango_alcanzado_color = ""

# MISIONES DIARIAS
if 'ultima_fecha_misiones' not in st.session_state:
    st.session_state.ultima_fecha_misiones = ""
if 'progreso_m1' not in st.session_state:
    st.session_state.progreso_m1 = 0
if 'progreso_m2' not in st.session_state:
    st.session_state.progreso_m2 = 0
if 'progreso_m3' not in st.session_state:
    st.session_state.progreso_m3 = 0
if 'm1_reclamada' not in st.session_state:
    st.session_state.m1_reclamada = False
if 'm2_reclamada' not in st.session_state:
    st.session_state.m2_reclamada = False
if 'm3_reclamada' not in st.session_state:
    st.session_state.m3_reclamada = False

# ORÁCULO: MEMORIA DE LA MISIÓN RANDOM
if 'input_mision_texto' not in st.session_state:
    st.session_state.input_mision_texto = ""

pildoras = [
    {"autor": "Marco Aurelio", "texto": "Tienes poder sobre tu mente, no sobre los acontecimientos externos. Date cuenta de esto."},
    {"autor": "Naval Ravikant", "texto": "Si no puedes ver el lado positivo, estás mirando con los ojos del ego."},
    {"autor": "David Goggins", "texto": "El sufrimiento es la única forma de crecer. Domina tu mente."},
    {"autor": "Séneca", "texto": "No es que tengamos poco tiempo, sino que perdemos mucho."}
]

# --- EL ORÁCULO DE LA DISCIPLINA (100 MISIONES DE VALOR REAL) ---
MISIONES_DESARROLLO = [
    "Bloque de Deep Work: 0 móvil, 0 distracciones. Solo la tarea más difícil.", "Leer 10 páginas de filosofía estoica o ensayo.", 
    "Hacer 100 flexiones estrictas (divide en series si es necesario).", "Limpiar y organizar el espacio de trabajo como un quirófano.",
    "Sesión de meditación de 15 minutos en silencio absoluto.", "Escribir 500 palabras sobre tus objetivos a 5 años.",
    "Estirar todo el cuerpo durante 20 minutos sin interrupciones.", "Aprender un concepto nuevo de tu sector industrial.",
    "Barrer, fregar y ordenar una habitación de tu casa al 100%.", "Hacer 50 sentadillas y 50 abdominales explosivas.",
    "Planificar tu semana entera hora por hora en el calendario.", "Leer 15 páginas de un libro técnico o financiero.",
    "Vaciar la bandeja de entrada del correo a Cero (Inbox Zero).", "Escribir en papel 3 cosas por las que estás agradecido.",
    "Hacer una rutina de Yoga o Movilidad de 30 minutos.", "Avanzar en ese proyecto que llevas procrastinando 1 mes.",
    "Practicar un idioma extranjero de forma intensiva.", "Escuchar un podcast de desarrollo personal tomando notas.",
    "Diseñar tu menú de comidas saludables para los próximos 3 días.", "Hacer 200 saltos de comba o jumping jacks.",
    "Revisar tus finanzas: ingresos, gastos y ahorro del mes.", "Visualización activa: Imaginar tu fracaso si no trabajas hoy.",
    "Beber 1 litro de agua e hidratar el cerebro antes de seguir.", "Desinstalar o bloquear una app tóxica de tu móvil.",
    "Llamar a un familiar o mentor que te inspire respeto.", "Estudiar la biografía de un líder histórico.",
    "Hacer una caminata rápida o correr 3km sin música.", "Tomar una ducha de agua fría extrema.",
    "Identificar tu mayor debilidad actual y trazar un plan para matarla.", "Practicar respiración Wim Hof (3 rondas completas).",
    "No quejarte de nada ni de nadie durante todo el día de hoy.", "Redactar tu 'Antivisión': en quién te convertirás si eres vago.",
    "Trabajar de pie durante los próximos 45 minutos.", "Hacer una sesión de 100 burpees.",
    "Optimizar tu currículum o perfil profesional de LinkedIn.", "Aprender los atajos de teclado del programa que más usas.",
    "Eliminar archivos inútiles de tu ordenador (limpieza digital).", "Hacer 5 series al fallo de dominadas o flexiones.",
    "Investigar cómo diversificar tus fuentes de ingresos.", "Anotar 5 ideas de negocio o mejoras para tu trabajo.",
    "Practicar el silencio: no hablar a menos que sea 100% necesario.", "Aprender sobre inversión pasiva o fondos indexados.",
    "Limpiar la cocina a fondo, dejando el fregadero impecable.", "Repasar tus metas anuales y tachar lo irrelevante.",
    "Trabajar ininterrumpidamente hasta que duela el cerebro.", "Analizar tus rutinas de sueño y planear cómo dormir 8h reales.",
    "Hacer un ayuno intermitente o saltarte la comida basura hoy.", "Ver un documental técnico y hacer un resumen escrito.",
    "Ordenar tu armario y desechar la ropa que ya no usas.", "Leer sobre inteligencia emocional y aplicar un concepto hoy.",
    "Trazar el organigrama mental de tu vida y tus pilares.", "Hacer 15 minutos de planchas (planks) acumulados.",
    "Evitar el azúcar y los procesados al 100% durante 24 horas.", "Escribirle a alguien que admires pidiéndole un consejo.",
    "Reflexionar sobre la muerte (Memento Mori) y la urgencia de vivir.", "Leer un artículo sobre física cuántica o astronomía.",
    "No usar redes sociales hasta que caiga el sol.", "Crear una base de datos para organizar tus conocimientos (Notion/Obsidian).",
    "Realizar ejercicios de Kegel o core avanzado.", "Automatizar una tarea repetitiva que odies hacer.",
    "Preparar la ropa y los objetivos de mañana antes de dormir.", "Leer 20 páginas de la biografía de Elon Musk o Steve Jobs.",
    "Buscar 3 formas de ahorrar dinero esta semana.", "Hacer un entrenamiento de fuerza con tu peso corporal.",
    "Aprender a usar la terminal/consola de tu ordenador.", "Crear una copia de seguridad de todos tus datos importantes.",
    "Tener una conversación difícil que has estado evitando.", "Eliminar suscripciones o gastos hormiga de tus tarjetas.",
    "Consumir contenido exclusivo de matemáticas o lógica.", "Escribir tu propio manifiesto de guerra personal.",
    "Realizar una sesión de alta intensidad HIIT de 20 minutos.", "Aprender los fundamentos de la programación en Python/SQL.",
    "Organizar los cables y la limpieza física de tu set-up.", "Analizar tu lenguaje corporal en el espejo y mejorarlo.",
    "Dedicar tiempo a entender el mercado cripto/blockchain.", "Hacer 100 sentadillas búlgaras (50 por pierna).",
    "Planear un fin de semana de desconexión total en la naturaleza.", "Aprender a cocinar un plato altamente nutritivo y barato.",
    "Escribir un ensayo crítico sobre una opinión impopular que tengas.", "Desuscribirte de correos publicitarios (limpiar newsletter).",
    "Pasar 30 minutos al sol sin distracciones tecnológicas.", "Aprender técnicas de persuasión y ventas.",
    "Evaluar a tus 5 amigos más cercanos: ¿Te suman o te restan?", "Leer sobre economía austriaca o macroeconomía básica.",
    "Escribir un diario de errores: fallos recientes y cómo no repetirlos.", "Practicar mecanografía para aumentar tus pulsaciones por minuto.",
    "No consumir pornografía ni contenido basura. Dopamina limpia.", "Mejorar la seguridad de tus contraseñas usando un gestor.",
    "Aprender sobre inteligencia artificial y automatización de IA.", "Hacer 10 series de sprints cuesta arriba.",
    "Ver un TED Talk sobre psicología humana o neurociencia.", "Diseñar una rutina matutina inquebrantable de 60 minutos.",
    "Auditar tu postura en la silla y corregirla conscientemente.", "Identificar qué tarea te da el 80% de tus resultados (Ley de Pareto).",
    "Hacer una lista de los peores escenarios posibles y prepararte para ellos.", "Aprender primeros auxilios básicos o maniobra de Heimlich.",
    "Construir tu propia página web o portafolio personal.", "Renunciar a la cafeína durante todo el día para resetear receptores.",
    "Memorizar frases clave en latín estoico (Amor Fati, Veni Vidi Vici).", "Investigar la historia militar de Roma o Esparta para forjar carácter."
]

# --- MOTORES MATEMÁTICOS DE RANGO Y ELO ---
def get_rank_info(elo):
    # Retorna: Nombre, Subtitulo, Icono, Color, Elo_Min, Elo_Max, Nivel_Indice
    if elo < 200: 
        return ("Hierro III", "Esclavo", "🪨", "#7a7a7a", 0, 200, 1)
    elif elo < 300: 
        return ("Hierro II", "Distraído", "⛓️", "#8f8f8f", 200, 300, 2)
    elif elo < 400: 
        return ("Hierro I", "Despertando", "⚙️", "#a3a3a3", 300, 400, 3)
    elif elo < 600: 
        return ("Bronce", "Guerrero", "🥉", "#cd7f32", 400, 600, 4)
    elif elo < 800: 
        return ("Plata", "Dueño del Tiempo", "🥈", "#c0c0c0", 600, 800, 5)
    elif elo < 1000: 
        return ("Oro", "Élite", "🥇", "#ffd700", 800, 1000, 6)
    else: 
        return ("Diamante", "Intocable", "💎", "#00ffff", 1000, 1000, 7)

def calcular_rango(elo):
    info = get_rank_info(elo)
    return info[0], info[1], info[2], info[3]

def tiene_boost_activo(fecha_str):
    if not fecha_str: 
        return False
    try:
        fecha_fin = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
        return datetime.now(timezone.utc) < fecha_fin
    except: 
        return False

def calcular_monedas_base(elo):
    if elo < 200: 
        return 10
    elif elo < 300: 
        return 15
    elif elo < 400: 
        return 20
    elif elo < 600: 
        return 35
    elif elo < 800: 
        return 50
    elif elo < 1000: 
        return 75
    else: 
        return 120

def calcular_riesgo_recompensa(segundos, elo_actual, boost_elo_str, boost_monedas_str):
    base_monedas = calcular_monedas_base(elo_actual)
    
    if segundos == 10: 
        p_elo = 5
        c_elo = 5
        coins = 1 
    elif segundos == 1500: 
        p_elo = 25
        c_elo = 20
        coins = base_monedas * 1 
    elif segundos == 3000: 
        p_elo = 55
        c_elo = 40
        coins = int(base_monedas * 2.5) 
    elif segundos == 5400: 
        p_elo = 100
        c_elo = 80
        coins = base_monedas * 5 
    else: 
        p_elo = 25
        c_elo = 25
        coins = base_monedas

    if tiene_boost_activo(boost_elo_str): 
        p_elo *= 2
        
    if tiene_boost_activo(boost_monedas_str): 
        coins *= 2
        
    return p_elo, c_elo, coins

def generar_carta_html(nombre, elo, rango_i, rango_c, subtitulo, skin='default'):
    display_name = f"👑 {nombre}" if skin == 'corona' else nombre
    
    if skin == 'aura':
        color_borde = "#ff0000"
        clase_animacion = "anim-aura"
    elif skin == 'fuego':
        color_borde = "#aa00ff"
        clase_animacion = "anim-fuego"
    elif skin == 'sombra':
        color_borde = "#00aaff"
        clase_animacion = "anim-sombra"
    else:
        color_borde = rango_c
        clase_animacion = "anim-float"
        
    if skin in ['aura', 'fuego', 'sombra']:
        efecto_sombra = ""
    else:
        efecto_sombra = f"box-shadow: 0 0 20px {color_borde}30;"

    html_bruto = f"""
    <div class="fut-card {clase_animacion}" style="background: linear-gradient(135deg, #161616 0%, #050505 100%); border: 2px solid {color_borde}; border-radius: 12px; width: 140px; margin: 10px; padding: 15px 10px; position: relative; {efecto_sombra} display: inline-block; text-align: center; transition: all 0.3s ease;">
        <div style="position: absolute; top: 8px; left: 12px; color: {color_borde}; font-weight: 900; font-size: 20px; font-family: monospace; text-shadow: 0 0 5px {color_borde};">{elo}</div>
        <div style="position: absolute; top: 8px; right: 12px; font-size: 20px; filter: drop-shadow(0 0 5px {color_borde});">{rango_i}</div>
        <div style="margin-top: 35px; margin-bottom: 10px;">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="{color_borde}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.9; filter: drop-shadow(0 0 8px {color_borde});">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
        </div>
        <h4 style="color: white; margin: 0; font-size: 14px; text-transform: uppercase; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: 1px;">{display_name}</h4>
        <div style="color: #666; font-size: 11px; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px; font-weight: bold;">{subtitulo}</div>
    </div>
    """
    return html_bruto.replace("\n", "")

def generar_html_mision(titulo, desc, oro, completada):
    if completada:
        color_borde = "#00ff00"
        opacidad = "0.5"
    else:
        color_borde = "#333"
        opacidad = "1"
        
    html_mision = f"""
    <div style="background-color: #121212; border: 1px solid {color_borde}; border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 10px; opacity: {opacidad}; transition: all 0.3s ease; box-shadow: 0 0 10px {color_borde}40;">
        <h4 style="color: white; margin: 0 0 5px 0; font-size: 14px; text-transform: uppercase;">{titulo}</h4>
        <p style="color: #888; font-size: 11px; margin: 0 0 10px 0;">{desc}</p>
        <h3 style="color: #ffd700; margin: 0; text-shadow: 0 0 5px rgba(255,215,0,0.5);">🪙 {oro}</h3>
    </div>
    """
    return html_mision.replace("\n", "")

def render_navbar(origen):
    st.markdown("<hr style='border: 1px solid #333; margin-top: 40px;'>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 0.05, 1, 0.05, 1, 0.05, 1])
    
    with c1:
        st.markdown("<div class='nav-btn'>".replace('\n', ''), unsafe_allow_html=True)
        if st.button("🏠 LOBBY", use_container_width=True, key=f"nav_lobby_{origen}"): 
            st.session_state.estado = "lobby"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c2: 
        st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>".replace('\n', ''), unsafe_allow_html=True)
        
    with c3:
        st.markdown("<div class='nav-btn'>".replace('\n', ''), unsafe_allow_html=True)
        if st.button("🛒 TIENDA", use_container_width=True, key=f"nav_tienda_{origen}"): 
            st.session_state.estado = "tienda"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c4: 
        st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>".replace('\n', ''), unsafe_allow_html=True)
        
    with c5:
        st.markdown("<div class='nav-btn'>".replace('\n', ''), unsafe_allow_html=True)
        if st.button("🏛️ LEYENDAS", use_container_width=True, key=f"nav_salon_{origen}"): 
            st.session_state.estado = "salon"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c6: 
        st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>".replace('\n', ''), unsafe_allow_html=True)

    with c7:
        st.markdown("<div class='nav-btn'>".replace('\n', ''), unsafe_allow_html=True)
        if st.button("🛡️ CUARTEL", use_container_width=True, key=f"nav_cuartel_{origen}"): 
            st.session_state.estado = "cuartel"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def generar_codigo_sala():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

# ==========================================================
# RUTAS DE LA APLICACIÓN
# ==========================================================

# --- LA PUERTA DE SEGURIDAD ---
if st.session_state.estado == "login":
    st.markdown("<h1 class='epic-title'>⚔️ LA ARENA</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class='manifesto'>
            El mundo está lleno de gente que abandona cuando duele.<br>
            <span class='highlight'>Nosotros venimos a romper al 99%.</span><br>
            Forja tu disciplina. Aplasta a tus rivales. Haz que tu nombre importe.
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    st.divider()
    
    tab1, tab2 = st.tabs(["🚪 ENTRAR AL COLISEO", "📝 FORJAR UNA LEYENDA"])
    
    with tab1:
        email_log = st.text_input("Correo electrónico", key="log_email")
        pass_log = st.text_input("Contraseña", type="password", key="log_pass")
        
        if st.button("ACCEDER", type="primary", use_container_width=True):
            try:
                respuesta = supabase.auth.sign_in_with_password({"email": email_log, "password": pass_log})
                user_id = respuesta.user.id
                st.session_state.usuario_id = user_id
                
                datos = supabase.table("jugadores").select("*").eq("id", user_id).execute()
                
                if len(datos.data) > 0:
                    d = datos.data[0]
                    st.session_state.puntos_elo = d.get('elo', 100)
                    st.session_state.racha = d.get('racha', 0)
                    st.session_state.monedas = d.get('monedas', 0)
                    st.session_state.nombre_guerra = d.get('nombre', 'Guerrero')
                    st.session_state.skin_activa = d.get('skin_activa', 'default')
                    st.session_state.inv_aura = d.get('inventario_aura', False)
                    st.session_state.inv_corona = d.get('inventario_corona', False)
                    st.session_state.inv_sombra = d.get('inv_sombra', False)
                    st.session_state.inv_fuego = d.get('inv_fuego', False)
                    st.session_state.boost_elo = d.get('boost_elo_hasta')
                    st.session_state.boost_monedas = d.get('boost_monedas_hasta')
                    
                    # CARGAMOS NUEVAS ESTADÍSTICAS DEL CUARTEL GENERAL
                    st.session_state.victorias = d.get('victorias', 0)
                    st.session_state.derrotas = d.get('derrotas', 0)
                    st.session_state.minutos_focus = d.get('minutos_focus', 0)
                    
                    fecha_db = d.get('ultima_fecha_misiones')
                    hoy_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
                    
                    if fecha_db != hoy_str:
                        supabase.table("jugadores").update({
                            "ultima_fecha_misiones": hoy_str, 
                            "progreso_m1": 0, 
                            "progreso_m2": 0, 
                            "progreso_m3": 0, 
                            "m1_reclamada": False, 
                            "m2_reclamada": False, 
                            "m3_reclamada": False
                        }).eq("id", user_id).execute()
                        
                        st.session_state.ultima_fecha_misiones = hoy_str
                        st.session_state.progreso_m1 = 0
                        st.session_state.progreso_m2 = 0
                        st.session_state.progreso_m3 = 0
                        st.session_state.m1_reclamada = False
                        st.session_state.m2_reclamada = False
                        st.session_state.m3_reclamada = False
                    else:
                        st.session_state.ultima_fecha_misiones = fecha_db
                        st.session_state.progreso_m1 = d.get('progreso_m1', 0)
                        st.session_state.progreso_m2 = d.get('progreso_m2', 0)
                        st.session_state.progreso_m3 = d.get('progreso_m3', 0)
                        st.session_state.m1_reclamada = d.get('m1_reclamada', False)
                        st.session_state.m2_reclamada = d.get('m2_reclamada', False)
                        st.session_state.m3_reclamada = d.get('m3_reclamada', False)
                else:
                    st.error("No se encontraron los datos del guerrero.")
                    st.stop()
                    
                st.session_state.estado = "lobby"
                st.rerun()
            except Exception as e:
                st.error("❌ El sistema no reconoce tus credenciales. ¿Te has acobardado?")
                
    with tab2:
        email_reg = st.text_input("Correo electrónico", key="reg_email")
        nombre_reg = st.text_input("¿Bajo qué nombre derramarás sangre?", key="reg_nombre")
        pass_reg = st.text_input("Contraseña (El candado de tu mente)", type="password", key="reg_pass")
        
        if st.button("JURAR LEALTAD A LA ARENA", type="primary", use_container_width=True):
            if not nombre_reg:
                st.error("Necesitas un nombre de guerra para que puedan recordarte.")
            else:
                try:
                    auth_resp = supabase.auth.sign_up({"email": email_reg, "password": pass_reg})
                    hoy_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
                    supabase.table("jugadores").insert({
                        "id": auth_resp.user.id, 
                        "elo": 100, 
                        "racha": 0, 
                        "monedas": 0, 
                        "nombre": nombre_reg, 
                        "ultima_fecha_misiones": hoy_str,
                        "victorias": 0,
                        "derrotas": 0,
                        "minutos_focus": 0
                    }).execute()
                    st.success("¡Tu nombre está grabado en la piedra! Pasa a la pestaña de 'Entrar'.")
                except Exception as e:
                    st.error(f"Fallo en el registro.")

# --- EL LOBBY ---
elif st.session_state.estado == "lobby":
    st.session_state.partida_id = None 
    st.session_state.rival_nombre = "Desconocido"
    rango_n, rango_s, rango_i, rango_c = calcular_rango(st.session_state.puntos_elo)
    
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; letter-spacing: 2px;'>⚔️ MODO COMBATE</h1>", unsafe_allow_html=True)
    
    boosts_html = ""
    if tiene_boost_activo(st.session_state.boost_elo): 
        boosts_html += "<span style='background:#ff4b4b; color:white; padding:2px 8px; border-radius:10px; font-size:12px; font-weight:bold; margin-right:5px;'>⚡ x2 ELO</span>"
    if tiene_boost_activo(st.session_state.boost_monedas): 
        boosts_html += "<span style='background:#ffd700; color:black; padding:2px 8px; border-radius:10px; font-size:12px; font-weight:bold;'>💰 x2 MONEDAS</span>"
        
    st.markdown(f"<h3 style='text-align: center; color: white; text-transform: uppercase;'>Bienvenido, {st.session_state.nombre_guerra} <br><div style='margin-top:10px;'>{boosts_html}</div></h3>".replace('\n', ''), unsafe_allow_html=True)
    
    st.divider()
    
    carta_propia = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, rango_i, rango_c, "TU LEYENDA", st.session_state.skin_activa)
    st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'>{carta_propia}</div>".replace('\n', ''), unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around; text-align: center; background-color: #121212; padding: 25px; border-radius: 12px; border: 1px solid {rango_c}; box-shadow: 0 4px 20px {rango_c}40;'>
            <div>
                <p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase;'>Tu Rango</p>
                <h2 style='margin: 0; color: {rango_c};'>{rango_i} {rango_n}</h2>
            </div>
            <div style='border-left: 1px solid #333; border-right: 1px solid #333; padding: 0 20px;'>
                <p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase;'>ELO</p>
                <h2 style='margin: 0; color: white;'>{st.session_state.puntos_elo} pts</h2>
            </div>
            <div>
                <p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase;'>Bóveda</p>
                <h2 style='margin: 0; color: #ffd700;'>🪙 {st.session_state.monedas}</h2>
            </div>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #00ff00; margin-top: 40px; text-shadow: 0 0 10px rgba(0,255,0,0.4);'>📜 CONTRATOS MERCENARIOS</h3>", unsafe_allow_html=True)
    
    pasos_totales = 4 
    pasos_actuales = min(st.session_state.progreso_m1, 1) + min(st.session_state.progreso_m2, 2) + min(st.session_state.progreso_m3, 1)
    porcentaje = int((pasos_actuales / pasos_totales) * 100)
    
    st.markdown(f"""
        <div style='width: 100%; background-color: #333; border-radius: 10px; margin-bottom: 20px;'>
            <div style='width: {porcentaje}%; height: 15px; background: linear-gradient(90deg, #008000, #00ff00); border-radius: 10px; box-shadow: 0 0 10px #00ff00; transition: width 0.5s ease;'></div>
        </div>
        <p style='text-align: center; color: #888; font-size: 12px; margin-top: -10px;'>Progreso Diario: {porcentaje}%</p>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    c_m1, c_m2, c_m3 = st.columns(3)
    
    with c_m1:
        st.markdown(generar_html_mision("Primer Sangrado", "Gana 1 combate", 50, st.session_state.m1_reclamada), unsafe_allow_html=True)
        if st.session_state.m1_reclamada: 
            st.button("✅ RECLAMADO", disabled=True, key="btn_m1_d", use_container_width=True)
        elif st.session_state.progreso_m1 >= 1:
            if st.button("🎁 RECLAMAR", type="primary", key="btn_m1_c", use_container_width=True):
                st.session_state.monedas += 50
                st.session_state.m1_reclamada = True
                supabase.table("jugadores").update({
                    "monedas": st.session_state.monedas, 
                    "m1_reclamada": True
                }).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else: 
            st.button("Falta 1", disabled=True, key="btn_m1_f", use_container_width=True)
            
    with c_m2:
        st.markdown(generar_html_mision("Asesino a Sueldo", "Gana 2 escaramuzas (25m)", 100, st.session_state.m2_reclamada), unsafe_allow_html=True)
        if st.session_state.m2_reclamada: 
            st.button("✅ RECLAMADO", disabled=True, key="btn_m2_d", use_container_width=True)
        elif st.session_state.progreso_m2 >= 2:
            if st.button("🎁 RECLAMAR", type="primary", key="btn_m2_c", use_container_width=True):
                st.session_state.monedas += 100
                st.session_state.m2_reclamada = True
                supabase.table("jugadores").update({
                    "monedas": st.session_state.monedas, 
                    "m2_reclamada": True
                }).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else: 
            faltantes = 2 - st.session_state.progreso_m2
            st.button(f"Faltan {faltantes}", disabled=True, key="btn_m2_f", use_container_width=True)
            
    with c_m3:
        st.markdown(generar_html_mision("El Titán", "Sobrevive 1 asalto (90m)", 300, st.session_state.m3_reclamada), unsafe_allow_html=True)
        if st.session_state.m3_reclamada: 
            st.button("✅ RECLAMADO", disabled=True, key="btn_m3_d", use_container_width=True)
        elif st.session_state.progreso_m3 >= 1:
            if st.button("🎁 RECLAMAR", type="primary", key="btn_m3_c", use_container_width=True):
                st.session_state.monedas += 300
                st.session_state.m3_reclamada = True
                supabase.table("jugadores").update({
                    "monedas": st.session_state.monedas, 
                    "m3_reclamada": True
                }).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else: 
            st.button("Falta 1", disabled=True, key="btn_m3_f", use_container_width=True)

    st.write("") 
    st.divider()
    
    st.markdown("""
        <div class="rules-box">
            <h3 style="text-align: center; color: #ff4b4b; text-transform: uppercase; margin-top: 0; text-shadow: 0 0 10px rgba(255, 75, 75, 0.5);">⚠️ Las Leyes de la Arena</h3>
            <ul style="list-style-type: none; padding-left: 0; color: #ccc; font-size: 15px; line-height: 1.8;">
                <li style="margin-bottom: 10px;">🟢 <span class="neon-green">CÓMO GANAR:</span> Cumple la misión y sobrevive sin salir de la aplicación.</li>
                <li style="margin-bottom: 10px;">🔴 <span class="neon-red">CÓMO PERDER:</span> Si cambias de pestaña o pulsas "Me Rindo", tu C4 explota.</li>
                <li>⚔️ <strong style="color: #ffd700;">EL PACTO:</strong> Si no trabajas, estarás engañando al sistema. Nunca a ti mismo.</li>
            </ul>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #ff4b4b;'>🔥 DECLARACIÓN DE INTENCIONES</h3>", unsafe_allow_html=True)
    
    c_texto, c_dado = st.columns([5, 1])
    
    with c_dado:
        st.write("")
        if st.button("🎲", help="¿No sabes qué hacer? Deja que el Oráculo decida tu destino.", use_container_width=True):
            st.session_state.input_mision_texto = random.choice(MISIONES_DESARROLLO)
            st.rerun()
            
    with c_texto:
        mision_input = st.text_input("", value=st.session_state.input_mision_texto, placeholder="Ej: Terminar el ensayo de Filosofía...", label_visibility="collapsed")
        st.session_state.input_mision_texto = mision_input 
    
    tiempo_opts = {
        "⚙️ Modo Test (10 Segundos | Riesgo: 5 ELO)": 10, 
        "⚔️ Escaramuza (25 Minutos | Riesgo: 20 ELO)": 1500, 
        "🔥 Asalto Profundo (50 Minutos | Riesgo: 40 ELO)": 3000, 
        "💀 Modo Titán (90 Minutos | Riesgo: 80 ELO)": 5400
    }
    tiempo_str = st.selectbox("Duración de la batalla:", list(tiempo_opts.keys()))
    
    c_pub, c_priv = st.columns(2)
    with c_pub:
        if st.button("🌍 BÚSQUEDA MUNDIAL", use_container_width=True, type="primary"):
            if not st.session_state.input_mision_texto: 
                st.error("Un guerrero no entra sin propósito. Declara tu misión o usa el dado 🎲.")
            else:
                limite_fantasmas = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
                supabase.table("partidas").delete().eq("estado", "esperando").lt("ultima_actividad", limite_fantasmas).execute()
                
                st.session_state.mision_actual = st.session_state.input_mision_texto
                st.session_state.tiempo_combate = tiempo_opts[tiempo_str]
                
                w_elo, l_elo, coins = calcular_riesgo_recompensa(st.session_state.tiempo_combate, st.session_state.puntos_elo, st.session_state.boost_elo, st.session_state.boost_monedas)
                st.session_state.elo_premio = w_elo
                st.session_state.elo_castigo = l_elo
                st.session_state.monedas_ganadas_recientes = coins
                
                st.session_state.tipo_partida = "publica"
                st.session_state.codigo_sala = ""
                st.session_state.inicio_busqueda = time.time()
                st.session_state.estado = "buscando"
                st.rerun()

    st.markdown("<h3 style='text-align: center; color: #888; margin-top: 30px;'>🤝 DUELO PRIVADO (SALAS DE SANGRE)</h3>", unsafe_allow_html=True)
    
    c_p1, c_p2 = st.columns([2, 1])
    with c_p1: 
        codigo_input = st.text_input("", placeholder="Pega un código o déjalo vacío para crear", label_visibility="collapsed", key="input_cod_priv")
    with c_p2:
        if st.button("🚪 CREAR / UNIRSE", use_container_width=True):
            if not st.session_state.input_mision_texto: 
                st.error("Declara tu misión primero o usa el dado 🎲.")
            else:
                st.session_state.mision_actual = st.session_state.input_mision_texto
                st.session_state.tiempo_combate = tiempo_opts[tiempo_str]
                
                w_elo, l_elo, coins = calcular_riesgo_recompensa(st.session_state.tiempo_combate, st.session_state.puntos_elo, st.session_state.boost_elo, st.session_state.boost_monedas)
                st.session_state.elo_premio = w_elo
                st.session_state.elo_castigo = l_elo
                st.session_state.monedas_ganadas_recientes = coins
                
                st.session_state.tipo_partida = "privada"
                st.session_state.codigo_sala = codigo_input.upper().strip() if codigo_input else generar_codigo_sala()
                st.session_state.inicio_busqueda = time.time()
                st.session_state.estado = "buscando_privada"
                st.rerun()

    render_navbar("lobby")

# --- EL CUARTEL GENERAL (PERFIL Y ESTADÍSTICAS) ---
elif st.session_state.estado == "cuartel":
    
    info_rango = get_rank_info(st.session_state.puntos_elo)
    rango_n, rango_s, rango_i, rango_c, elo_min, elo_max, rango_nivel = info_rango
    
    st.markdown("<h1 style='text-align: center; color: #fff; letter-spacing: 2px;'>🛡️ CUARTEL GENERAL</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: {rango_c}; margin-bottom: 30px;'>Registro de Guerra de {st.session_state.nombre_guerra}</h4>", unsafe_allow_html=True)
    
    # CÁLCULO DE ELO Y BARRA DE PROGRESO
    if elo_min == elo_max:
        porcentaje_elo = 100
        texto_progreso = f"RANGO MÁXIMO ALCANZADO ({st.session_state.puntos_elo} ELO)"
    else:
        puntos_conseguidos = st.session_state.puntos_elo - elo_min
        puntos_rango = elo_max - elo_min
        porcentaje_elo = int((puntos_conseguidos / puntos_rango) * 100)
        texto_progreso = f"{st.session_state.puntos_elo} / {elo_max} ELO para el siguiente rango"

    st.markdown(f"""
        <div style='background-color: #111; border: 1px solid {rango_c}; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 0 15px {rango_c}30;'>
            <h3 style='color: white; margin-top: 0; text-transform: uppercase;'>PROGRESO DE LIGA: {rango_i} {rango_n}</h3>
            <div style='width: 100%; background-color: #333; border-radius: 10px; margin: 15px 0;'>
                <div style='width: {porcentaje_elo}%; height: 20px; background: linear-gradient(90deg, #111, {rango_c}); border-radius: 10px; box-shadow: 0 0 10px {rango_c}; transition: width 0.5s ease;'></div>
            </div>
            <p style='color: #888; font-size: 14px; font-weight: bold; margin: 0;'>{texto_progreso} ({porcentaje_elo}%)</p>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)

    # CÁLCULO DE ESTADÍSTICAS MATEMÁTICAS
    total_partidas = st.session_state.victorias + st.session_state.derrotas
    winrate = int((st.session_state.victorias / total_partidas * 100) if total_partidas > 0 else 0)
    horas_focus = round(st.session_state.minutos_focus / 60, 1)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div style='background-color: #161616; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center;'>
                <p style='color: #888; font-size: 12px; text-transform: uppercase; margin: 0;'>Winrate</p>
                <h2 style='color: #00ff00; margin: 5px 0;'>{winrate}%</h2>
                <p style='color: #555; font-size: 10px; margin: 0;'>{st.session_state.victorias} V / {st.session_state.derrotas} D</p>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div style='background-color: #161616; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center;'>
                <p style='color: #888; font-size: 12px; text-transform: uppercase; margin: 0;'>Tiempo Profundo</p>
                <h2 style='color: #00aaff; margin: 5px 0;'>{horas_focus}h</h2>
                <p style='color: #555; font-size: 10px; margin: 0;'>{st.session_state.minutos_focus} Minutos Totales</p>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div style='background-color: #161616; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center;'>
                <p style='color: #888; font-size: 12px; text-transform: uppercase; margin: 0;'>Mejor Racha</p>
                <h2 style='color: #ff4b4b; margin: 5px 0;'>🔥 {st.session_state.racha}</h2>
                <p style='color: #555; font-size: 10px; margin: 0;'>Victorias Seguidas</p>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    render_navbar("cuartel")

# --- LA TIENDA (EL CASINO) ---
elif st.session_state.estado == "tienda":
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    
    st.markdown("<h1 style='text-align: center; color: #ffd700; letter-spacing: 2px;'>🛒 EL MERCADO NEGRO</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>La avaricia es el motor del imperio.</h4>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background-color: #1a1a1a; border: 1px solid #ffd700; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 30px;'>
            <p style='margin:0; color:#aaa; font-size:14px; text-transform:uppercase;'>Fondos Disponibles</p>
            <h2 style='margin:0; color:#ffd700; font-size:36px; text-shadow: 0 0 15px rgba(255,215,0,0.4);'>🪙 {st.session_state.monedas}</h2>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    st.markdown("### 🎲 EL COFRE DEL GLADIADOR (GACHA)")
    st.markdown(f"""
        <div style='background:#121212; border:2px solid #ffd700; padding:20px; text-align:center; border-radius:8px; box-shadow: 0 0 20px rgba(255,215,0,0.2);'>
            <h1 style='font-size: 80px; margin:0;'>🧰</h1>
            <h3 style='color: white; margin-top: 10px;'>Cofre Misterioso</h3>
            <p style='color: #888; font-size: 12px;'>Probabilidades: 🟦 Raro (70%) | 🟪 Épico (20%) | 🟥 Mítico (9%) | 🟨 Legendario (1%)</p>
            <h2 style='color:#ffd700; margin-bottom: 20px;'>🪙 1000</h2>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    if st.button("🎲 ABRIR COFRE (1000 Monedas)", type="primary", use_container_width=True):
        if st.session_state.monedas >= 1000:
            st.session_state.monedas -= 1000
            supabase.table("jugadores").update({"monedas": st.session_state.monedas}).eq("id", st.session_state.usuario_id).execute()
            st.session_state.estado = "cofre_animacion"
            st.rerun()
        else:
            st.error("No tienes fondos para el azar.")
    
    st.markdown("### 🧬 BOOSTS DIRECTOS (24 Horas)")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("""
            <div style='background:#121212; border:1px solid #333; padding:15px; text-align:center; border-radius:8px;'>
                <h3>⚡ x2 ELO</h3>
                <p style='color:#888; font-size:12px;'>Multiplica tus ganancias de rango.</p>
                <h3 style='color:#ffd700;'>🪙 150</h3>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)
        if st.button("COMPRAR BOOST ELO", key="b_elo", use_container_width=True):
            if st.session_state.monedas >= 150:
                st.session_state.monedas -= 150
                fin = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
                st.session_state.boost_elo = fin
                supabase.table("jugadores").update({
                    "monedas": st.session_state.monedas, 
                    "boost_elo_hasta": fin
                }).eq("id", st.session_state.usuario_id).execute()
                st.success("¡Boost ELO Activado!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("No tienes oro suficiente.")
            
    with b2:
        st.markdown("""
            <div style='background:#121212; border:1px solid #333; padding:15px; text-align:center; border-radius:8px;'>
                <h3>💰 x2 MONEDAS</h3>
                <p style='color:#888; font-size:12px;'>Multiplica tus ingresos de victoria.</p>
                <h3 style='color:#ffd700;'>🪙 200</h3>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)
        if st.button("COMPRAR BOOST ORO", key="b_oro", use_container_width=True):
            if st.session_state.monedas >= 200:
                st.session_state.monedas -= 200
                fin = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
                st.session_state.boost_monedas = fin
                supabase.table("jugadores").update({
                    "monedas": st.session_state.monedas, 
                    "boost_monedas_hasta": fin
                }).eq("id", st.session_state.usuario_id).execute()
                st.success("¡Boost Monedas Activado!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Faltan fondos.")

    st.markdown("### 🔥 COMPRA DIRECTA (INFLACIÓN APLICADA)")
    
    t1, t2 = st.columns(2)
    
    carta_aura = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'aura')
    with t1:
        st.markdown(f"""
            <div style='background:#121212; border:1px solid #ff4b4b; padding:15px; text-align:center; border-radius:8px;'>
                {carta_aura}
                <h4 style='margin-top:10px;'>Aura Sanguinaria</h4>
                <p style='color:#ff4b4b;'>Rareza: Mítica</p>
                <h3 style='color:#ffd700;'>🪙 5000</h3>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)
        
        if st.session_state.inv_aura:
            if st.session_state.skin_activa == 'aura':
                st.info("EQUIPADA")
            elif st.button("EQUIPAR", key="eq_aura", use_container_width=True): 
                st.session_state.skin_activa = 'aura'
                supabase.table("jugadores").update({"skin_activa": "aura"}).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else:
            if st.button("COMPRAR", key="cp_aura", use_container_width=True):
                if st.session_state.monedas >= 5000:
                    st.session_state.monedas -= 5000
                    st.session_state.inv_aura = True
                    supabase.table("jugadores").update({
                        "monedas": st.session_state.monedas, 
                        "inventario_aura": True
                    }).eq("id", st.session_state.usuario_id).execute()
                    st.success("Desbloqueada")
                    st.rerun()
                else:
                    st.error("Ahorra, pobre.")
                
    carta_corona = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'corona')
    with t2:
        st.markdown(f"""
            <div style='background:#121212; border:1px solid #ffd700; padding:15px; text-align:center; border-radius:8px;'>
                {carta_corona}
                <h4 style='margin-top:10px;'>Corona del Rey</h4>
                <p style='color:#ffd700;'>Rareza: Legendaria</p>
                <h3 style='color:#ffd700;'>🪙 10000</h3>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)
        
        if st.session_state.inv_corona:
            if st.session_state.skin_activa == 'corona':
                st.info("EQUIPADA")
            elif st.button("EQUIPAR", key="eq_cor", use_container_width=True): 
                st.session_state.skin_activa = 'corona'
                supabase.table("jugadores").update({"skin_activa": "corona"}).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else:
            if st.button("COMPRAR", key="cp_cor", use_container_width=True):
                if st.session_state.monedas >= 10000:
                    st.session_state.monedas -= 10000
                    st.session_state.inv_corona = True
                    supabase.table("jugadores").update({
                        "monedas": st.session_state.monedas, 
                        "inventario_corona": True
                    }).eq("id", st.session_state.usuario_id).execute()
                    st.success("El Rey.")
                    st.rerun()
                else:
                    st.error("Sigue peleando.")
                
    st.markdown("### 🌀 COMPRA SECUNDARIA")
    
    t3, t4 = st.columns(2)
    
    carta_sombra = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'sombra')
    with t3:
        st.markdown(f"""
            <div style='background:#121212; border:1px solid #00aaff; padding:15px; text-align:center; border-radius:8px;'>
                {carta_sombra}
                <h4 style='margin-top:10px;'>Sombra Persistente</h4>
                <p style='color:#00aaff;'>Rareza: Rara</p>
                <h3 style='color:#ffd700;'>🪙 1500</h3>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)
        
        if st.session_state.inv_sombra:
            if st.session_state.skin_activa == 'sombra':
                st.info("EQUIPADA")
            elif st.button("EQUIPAR", key="eq_som", use_container_width=True): 
                st.session_state.skin_activa = 'sombra'
                supabase.table("jugadores").update({"skin_activa": "sombra"}).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else:
            if st.button("COMPRAR", key="cp_som", use_container_width=True):
                if st.session_state.monedas >= 1500:
                    st.session_state.monedas -= 1500
                    st.session_state.inv_sombra = True
                    supabase.table("jugadores").update({
                        "monedas": st.session_state.monedas, 
                        "inv_sombra": True
                    }).eq("id", st.session_state.usuario_id).execute()
                    st.rerun()
                else:
                    st.error("Ahorra.")

    carta_fuego = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'fuego')
    with t4:
        st.markdown(f"""
            <div style='background:#121212; border:1px solid #aa00ff; padding:15px; text-align:center; border-radius:8px;'>
                {carta_fuego}
                <h4 style='margin-top:10px;'>Fuego Fatuo</h4>
                <p style='color:#aa00ff;'>Rareza: Épica</p>
                <h3 style='color:#ffd700;'>🪙 2500</h3>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)
        
        if st.session_state.inv_fuego:
            if st.session_state.skin_activa == 'fuego':
                st.info("EQUIPADA")
            elif st.button("EQUIPAR", key="eq_fue", use_container_width=True): 
                st.session_state.skin_activa = 'fuego'
                supabase.table("jugadores").update({"skin_activa": "fuego"}).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else:
            if st.button("COMPRAR", key="cp_fue", use_container_width=True):
                if st.session_state.monedas >= 2500:
                    st.session_state.monedas -= 2500
                    st.session_state.inv_fuego = True
                    supabase.table("jugadores").update({
                        "monedas": st.session_state.monedas, 
                        "inv_fuego": True
                    }).eq("id", st.session_state.usuario_id).execute()
                    st.rerun()
                else:
                    st.error("Ahorra.")

    if st.button("✖ QUITAR SKIN ACTUAL", use_container_width=True):
        st.session_state.skin_activa = 'default'
        supabase.table("jugadores").update({"skin_activa": "default"}).eq("id", st.session_state.usuario_id).execute()
        st.rerun()
    
    render_navbar("tienda")

# --- ANIMACIÓN DEL COFRE MISTERIOSO ---
elif st.session_state.estado == "cofre_animacion":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/foley/creaky_door_open.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#ffd700;'>FORZANDO LA CERRADURA...</h2>", unsafe_allow_html=True)
    st.markdown("<div class='chest-anim'>🧰</div>", unsafe_allow_html=True)
    
    if st.button("💥 REVELAR EL CONTENIDO 💥", type="primary", use_container_width=True):
        tirada = random.randint(1, 100)
        st.session_state.premio_duplicado = False
        
        if tirada <= 70: 
            st.session_state.premio_cofre = "sombra"
            if st.session_state.inv_sombra: 
                st.session_state.premio_duplicado = True
            else: 
                st.session_state.inv_sombra = True
                supabase.table("jugadores").update({"inv_sombra": True}).eq("id", st.session_state.usuario_id).execute()
        elif tirada <= 90: 
            st.session_state.premio_cofre = "fuego"
            if st.session_state.inv_fuego: 
                st.session_state.premio_duplicado = True
            else:
                st.session_state.inv_fuego = True
                supabase.table("jugadores").update({"inv_fuego": True}).eq("id", st.session_state.usuario_id).execute()
        elif tirada <= 99: 
            st.session_state.premio_cofre = "aura"
            if st.session_state.inv_aura: 
                st.session_state.premio_duplicado = True
            else:
                st.session_state.inv_aura = True
                supabase.table("jugadores").update({"inventario_aura": True}).eq("id", st.session_state.usuario_id).execute()
        else: 
            st.session_state.premio_cofre = "corona"
            if st.session_state.inv_corona: 
                st.session_state.premio_duplicado = True
            else:
                st.session_state.inv_corona = True
                supabase.table("jugadores").update({"inventario_corona": True}).eq("id", st.session_state.usuario_id).execute()
        
        if st.session_state.premio_duplicado:
            st.session_state.monedas += 300
            supabase.table("jugadores").update({"monedas": st.session_state.monedas}).eq("id", st.session_state.usuario_id).execute()
            
        st.session_state.estado = "cofre_resultado"
        st.rerun()

# --- RESULTADO DEL COFRE ---
elif st.session_state.estado == "cofre_resultado":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/foley/glass_shatter.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#fff;'>EL COFRE SE HA ABIERTO</h1>", unsafe_allow_html=True)
    
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    carta_premio = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "NUEVA SKIN", st.session_state.premio_cofre)
    
    if st.session_state.premio_cofre == "sombra": 
        titulo_premio = "🟦 SOMBRA PERSISTENTE (RARO)"
    elif st.session_state.premio_cofre == "fuego": 
        titulo_premio = "🟪 FUEGO FATUO (ÉPICO)"
    elif st.session_state.premio_cofre == "aura": 
        titulo_premio = "🟥 AURA SANGUINARIA (MÍTICO)"
    else: 
        titulo_premio = "🟨 CORONA DEL REY (LEGENDARIO) 🟨"

    st.markdown(f"""
        <div style='text-align: center; margin: 30px 0;'>
            {carta_premio}
            <h2 style='margin-top: 20px;'>{titulo_premio}</h2>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    if st.session_state.premio_duplicado:
        st.warning("⚠️ Ya tenías esta skin en tu inventario. El sistema la ha fundido en 300 Monedas a tu favor.")
    else:
        st.success("¡Skin añadida a tu inventario para siempre!")
        
    if st.button("Volver a la Tienda", use_container_width=True):
        st.session_state.estado = "tienda"
        st.rerun()

# --- EL SALÓN DE LOS DIOSES (TEMPORADAS) ---
elif st.session_state.estado == "salon":
    st.markdown("<h1 style='text-align: center; color: #ffd700; letter-spacing: 2px; text-shadow: 0 0 20px rgba(255,215,0,0.5);'>🏛️ SALÓN DE LOS DIOSES</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Las leyendas nunca mueren. Solo trascienden.</h4>", unsafe_allow_html=True)
    st.divider()

    fecha_fin_temporada = datetime(2026, 9, 1, 0, 0, 0, tzinfo=timezone.utc)
    ahora = datetime.now(timezone.utc)
    diferencia = fecha_fin_temporada - ahora
    dias = diferencia.days
    segundos = diferencia.seconds
    horas = segundos // 3600

    st.markdown(f"""
        <div style='background-color: #111; border: 1px solid #333; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 30px;'>
            <h3 style='color: #ff4b4b; margin-top: 0; text-transform: uppercase;'>⏳ CIERRE DE LA TEMPORADA 1</h3>
            <p style='color: #888; font-size: 14px;'>Al llegar a cero, el ELO se reseteará. Solo los 3 mejores serán grabados en la piedra eterna.</p>
            <h1 style='color: white; font-family: monospace; font-size: 45px; margin: 10px 0; text-shadow: 0 0 10px rgba(255,255,255,0.3);'>
                {dias}D : {horas}H
            </h1>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #fff;'>🏆 ASPIRANTES A LEYENDA (TOP 3 ACTUAL)</h3>", unsafe_allow_html=True)
    
    ranking = supabase.table("jugadores").select("elo, nombre, skin_activa").order("elo", desc=True).limit(3).execute()
    if ranking.data:
        cartas_html = "<div style='display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; padding: 10px 0;'>"
        for i, jugador in enumerate(ranking.data):
            _, _, i_rank, c_rank = calcular_rango(jugador['elo'])
            cartas_html += generar_carta_html(jugador['nombre'], jugador['elo'], i_rank, c_rank, f"ASPIRANTE #{i+1}", jugador.get('skin_activa', 'default'))
        cartas_html += "</div>"
        st.markdown(cartas_html.replace('\n', ''), unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #ffd700; margin-top: 40px;'>📜 LEYENDAS INMORTALES</h3>", unsafe_allow_html=True)
    
    leyendas = supabase.table("leyendas").select("*").order("temporada", desc=True).execute()
    if leyendas.data:
        for l in leyendas.data:
            st.markdown(f"""
                <div style='background:#1a1a1a; border-left:4px solid {l['rango_color']}; padding:15px; margin-bottom:10px;'>
                    <h4 style='margin:0; color:white;'>Temporada {l['temporada']}: {l['nombre']}</h4>
                    <p style='margin:0; color:#888;'>{l['rango_icono']} {l['rango_nombre']} - {l['elo_final']} ELO Final</p>
                </div>
            """.replace('\n', ''), unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='text-align:center; padding:30px; border:1px dashed #333;'>
                <p style='color:#555; font-style:italic;'>El pedestal está vacío.</p>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    render_navbar("salon")

# --- EMPAREJAMIENTO MULTIJUGADOR ---
elif st.session_state.estado == "buscando" or st.session_state.estado == "buscando_privada":
    st.markdown("<audio autoplay loop src='https://actions.google.com/sounds/v1/alarms/beep_short.ogg'></audio>", unsafe_allow_html=True)
    
    tiempo_espera = time.time() - st.session_state.inicio_busqueda
    if st.session_state.estado == "buscando":
        st.markdown(f"<h2 style='text-align: center; color: #ff4b4b; animation: pulse 1.5s infinite;'>📡 Rastreando la red pública ({int(tiempo_espera)}s)...</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #ff4b4b;'>🤝 SALA DE SANGRE</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background-color: #111; border: 2px dashed #ff4b4b; padding: 20px; text-align: center; margin: 20px 0; border-radius: 10px;'>
                <p style='color: #888; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px;'>Pásale este código a tu rival</p>
                <h1 style='color: white; font-size: 60px; font-family: monospace; margin: 0; letter-spacing: 5px; text-shadow: 0 0 15px rgba(255,255,255,0.4);'>{st.session_state.codigo_sala}</h1>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #666;'>Esperando conexión... ({int(tiempo_espera)}s)</p>", unsafe_allow_html=True)
    
    if st.session_state.estado == "buscando" and tiempo_espera > 15:
        if st.session_state.partida_id: 
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
        st.session_state.partida_id = None
        st.session_state.rival_nombre = "EL GUARDIÁN"
        st.session_state.rival_elo = st.session_state.puntos_elo + 15
        st.session_state.rival_mision = "Quebrantar tu voluntad."
        st.session_state.rival_skin = 'aura' 
        st.session_state.estado = "duelo"
        st.rerun()
    
    if st.button("Cancelar Búsqueda" if st.session_state.estado == "buscando" else "Destruir Sala y Volver", use_container_width=True):
        if st.session_state.partida_id: 
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
        st.session_state.estado = "lobby"
        st.rerun()

    if not st.session_state.partida_id:
        if st.session_state.estado == "buscando":
            rango_min = st.session_state.puntos_elo - 150
            rango_max = st.session_state.puntos_elo + 150
            disponibles = supabase.table("partidas").select("*").eq("estado", "esperando").eq("tipo", "publica").eq("tiempo_batalla", st.session_state.tiempo_combate).neq("jugador1", st.session_state.usuario_id).gte("jugador1_elo", rango_min).lte("jugador1_elo", rango_max).execute()
        else:
            disponibles = supabase.table("partidas").select("*").eq("estado", "esperando").eq("tipo", "privada").eq("codigo_sala", st.session_state.codigo_sala).neq("jugador1", st.session_state.usuario_id).execute()
            
        if len(disponibles.data) > 0:
            sala = disponibles.data[0]
            st.session_state.partida_id = sala['id']
            ahora = datetime.now(timezone.utc).isoformat()
            
            supabase.table("partidas").update({
                "jugador2": st.session_state.usuario_id, 
                "estado": "luchando", 
                "ultima_actividad": ahora, 
                "jugador2_mision": st.session_state.mision_actual
            }).eq("id", sala['id']).execute()
            
            rival_db = supabase.table("jugadores").select("nombre, elo, skin_activa").eq("id", sala['jugador1']).execute()
            if rival_db.data: 
                st.session_state.rival_nombre = rival_db.data[0]['nombre']
                st.session_state.rival_elo = rival_db.data[0]['elo']
                st.session_state.rival_skin = rival_db.data[0].get('skin_activa', 'default')
            else: 
                st.session_state.rival_nombre = "Anónimo"
                st.session_state.rival_elo = 100
                st.session_state.rival_skin = 'default'
                
            st.session_state.rival_mision = sala.get('jugador1_mision', "Sobrevivir")
            st.session_state.estado = "duelo"
            st.rerun()
        else:
            tipo_p = "publica" if st.session_state.estado == "buscando" else "privada"
            cod_s = "" if st.session_state.estado == "buscando" else st.session_state.codigo_sala
            nueva = supabase.table("partidas").insert({
                "jugador1": st.session_state.usuario_id, 
                "estado": "esperando", 
                "tipo": "publica", 
                "codigo_sala": cod_s, 
                "jugador1_elo": st.session_state.puntos_elo, 
                "tiempo_batalla": st.session_state.tiempo_combate, 
                "jugador1_mision": st.session_state.mision_actual
            }).execute()
            st.session_state.partida_id = nueva.data[0]['id']
            st.rerun()
    else:
        ahora = datetime.now(timezone.utc).isoformat()
        supabase.table("partidas").update({"ultima_actividad": ahora}).eq("id", st.session_state.partida_id).execute()
        estado_sala = supabase.table("partidas").select("*").eq("id", st.session_state.partida_id).execute()
        
        if len(estado_sala.data) > 0 and estado_sala.data[0]['estado'] == 'luchando':
            sala = estado_sala.data[0]
            rival_db = supabase.table("jugadores").select("nombre, elo, skin_activa").eq("id", sala['jugador2']).execute()
            if rival_db.data: 
                st.session_state.rival_nombre = rival_db.data[0]['nombre']
                st.session_state.rival_elo = rival_db.data[0]['elo']
                st.session_state.rival_skin = rival_db.data[0].get('skin_activa', 'default')
            else: 
                st.session_state.rival_nombre = "Anónimo"
                st.session_state.rival_elo = 100
                st.session_state.rival_skin = 'default'
                
            st.session_state.rival_mision = sala.get('jugador2_mision', "Sobrevivir")
            st.session_state.estado = "duelo"
            st.rerun()
        else:
            with st.spinner("Rastreando..." if st.session_state.estado == "buscando" else "Vigilando la puerta..."): 
                time.sleep(2)
                st.rerun()

# --- LA ARENA DE DUELO ---
elif st.session_state.estado == "duelo":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/weapons/metal_clang.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; text-transform: uppercase; letter-spacing: 3px;'>🔥 DUELO A MUERTE 🔥</h1>", unsafe_allow_html=True)
    
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    _, _, riv_i, riv_c = calcular_rango(st.session_state.rival_elo)
    
    carta_tu = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "TÚ", st.session_state.skin_activa)
    carta_riv = generar_carta_html(st.session_state.rival_nombre, st.session_state.rival_elo, riv_i, riv_c, "ENEMIGO", st.session_state.get('rival_skin', 'default'))
    
    st.markdown(f"""
        <div style='display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; margin-top: 20px;'>
            {carta_tu}
            <h1 style='color: #ff4b4b; font-size: 50px; font-style: italic; text-shadow: 0 0 20px #ff4b4b;'>VS</h1>
            {carta_riv}
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='display: flex; justify-content: space-between; background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; margin-top: 15px;'>
            <div style='text-align: left; width: 45%;'>
                <p style='color: {tu_c}; margin: 0; font-weight: bold; font-size: 12px;'>TU OBJETIVO</p>
                <p style='color: white; font-family: monospace; font-size: 14px; margin: 0;'>{st.session_state.mision_actual}</p>
            </div>
            <div style='border-left: 1px solid #333;'></div>
            <div style='text-align: right; width: 45%;'>
                <p style='color: {riv_c}; margin: 0; font-weight: bold; font-size: 12px;'>OBJETIVO ENEMIGO</p>
                <p style='color: white; font-family: monospace; font-size: 14px; margin: 0;'>{st.session_state.rival_mision}</p>
            </div>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #0a0a0a; border: 2px solid #ff4b4b; border-radius: 15px; padding: 20px; margin: 30px 0; box-shadow: 0 0 30px rgba(255, 75, 75, 0.2);'>
            <div id='reloj-container' style='text-align: center; font-size: 80px; font-family: monospace; font-weight: bold; color: white;'>--:--</div>
            <div id='audio-container'></div>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    if st.button("💀 ME RINDO (Tocar el móvil)", type="primary", use_container_width=True):
        st.session_state.puntos_elo = max(0, st.session_state.puntos_elo - st.session_state.elo_castigo)
        st.session_state.racha = 0
        st.session_state.derrotas += 1
        st.session_state.minutos_focus += int(st.session_state.tiempo_combate / 60)
        
        supabase.table("jugadores").update({
            "elo": st.session_state.puntos_elo, 
            "racha": st.session_state.racha,
            "derrotas": st.session_state.derrotas,
            "minutos_focus": st.session_state.minutos_focus
        }).eq("id", st.session_state.usuario_id).execute()
        
        supabase.table("historial").insert({
            "jugador_id": st.session_state.usuario_id, 
            "rival_nombre": st.session_state.rival_nombre, 
            "resultado": "derrota", 
            "puntos_cambio": -st.session_state.elo_castigo
        }).execute()
        
        if st.session_state.partida_id:
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
            
        st.session_state.estado = "derrota"
        st.rerun()
            
    if st.button("VICTORIA_SECRETA", key="btn_victoria"):
        viejo_rango_idx = get_rank_info(st.session_state.puntos_elo)[6]
        
        st.session_state.puntos_elo += st.session_state.elo_premio
        st.session_state.racha += 1
        st.session_state.monedas += st.session_state.monedas_ganadas_recientes
        st.session_state.victorias += 1
        st.session_state.minutos_focus += int(st.session_state.tiempo_combate / 60)
        
        st.session_state.progreso_m1 += 1  
        if st.session_state.tiempo_combate == 1500: 
            st.session_state.progreso_m2 += 1
        elif st.session_state.tiempo_combate == 5400: 
            st.session_state.progreso_m3 += 1
            
        supabase.table("jugadores").update({
            "elo": st.session_state.puntos_elo, 
            "racha": st.session_state.racha, 
            "monedas": st.session_state.monedas, 
            "progreso_m1": st.session_state.progreso_m1, 
            "progreso_m2": st.session_state.progreso_m2, 
            "progreso_m3": st.session_state.progreso_m3,
            "victorias": st.session_state.victorias,
            "minutos_focus": st.session_state.minutos_focus
        }).eq("id", st.session_state.usuario_id).execute()
        
        supabase.table("historial").insert({
            "jugador_id": st.session_state.usuario_id, 
            "rival_nombre": st.session_state.rival_nombre, 
            "resultado": "victoria", 
            "puntos_cambio": st.session_state.elo_premio
        }).execute()
        
        if st.session_state.partida_id:
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
            
        st.session_state.ultima_pildora = random.choice(pildoras)
        
        # MOTOR DE ASCENSO
        nuevo_rango = get_rank_info(st.session_state.puntos_elo)
        if nuevo_rango[6] > viejo_rango_idx:
            st.session_state.rango_alcanzado_nombre = f"{nuevo_rango[2]} {nuevo_rango[0]} - {nuevo_rango[1]}"
            st.session_state.rango_alcanzado_color = nuevo_rango[3]
            st.session_state.estado = "ascenso"
        else:
            st.session_state.estado = "victoria"
            
        st.rerun()

    components.html(f"""
        <script>
            const parentDoc = window.parent.document;
            const todosLosBotones = parentDoc.querySelectorAll('button');
            todosLosBotones.forEach(btn => {{ 
                if(btn.innerText.includes('VICTORIA_SECRETA')) btn.closest('div[data-testid="stButton"]').style.display = 'none'; 
            }});
            
            let tiempoRestante = {st.session_state.tiempo_combate}; 
            let latidoReproducido = false;
            
            function actualizarReloj() {{
                let m = Math.floor(tiempoRestante / 60);
                let s = tiempoRestante % 60;
                let fmt = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
                parentDoc.getElementById('reloj-container').innerText = fmt;
                
                if (tiempoRestante <= 5 && tiempoRestante > 0 && !latidoReproducido) {{
                    parentDoc.getElementById('audio-container').innerHTML = "<audio autoplay src='https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg'></audio>";
                    latidoReproducido = true;
                }}
            }}
            
            actualizarReloj();
            
            const intervalo = setInterval(function() {{
                tiempoRestante--;
                actualizarReloj();
                if (tiempoRestante <= 0) {{ 
                    clearInterval(intervalo); 
                    todosLosBotones.forEach(btn => {{ 
                        if(btn.innerText.includes('VICTORIA_SECRETA')) btn.click(); 
                    }}); 
                }}
            }}, 1000);
            
            parentDoc.addEventListener('visibilitychange', function() {{ 
                if (parentDoc.visibilityState === 'hidden') {{ 
                    clearInterval(intervalo); 
                    todosLosBotones.forEach(btn => {{ 
                        if(btn.innerText.includes('ME RINDO')) btn.click(); 
                    }}); 
                }} 
            }});
        </script>
    """, height=0, width=0)

# --- PANTALLAS FINALES ---
elif st.session_state.estado == "derrota":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #ff1a1a; font-size: 4em; text-transform: uppercase;'>💀 DERROTA</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #ff4b4b; font-size: 3em;'>-{st.session_state.elo_castigo} ELO</h2>", unsafe_allow_html=True)
    st.error(f"Abandonaste tu misión: *'{st.session_state.mision_actual}'*. **{st.session_state.rival_nombre}** se ha llevado la gloria por tu debilidad.")
    st.write("")
    if st.button("Tragar el orgullo y volver", use_container_width=True): 
        st.session_state.estado = "lobby"
        st.rerun()

elif st.session_state.estado == "ascenso":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/crowds/crowd_cheering.ogg'></audio>", unsafe_allow_html=True)
    color = st.session_state.rango_alcanzado_color
    st.markdown(f"""
        <div class="rank-up-box" style="background-color: #111; border: 4px solid {color}; border-radius: 20px; padding: 40px; text-align: center; margin: 40px 0; box-shadow: 0 0 50px {color};">
            <h1 style="color: white; font-size: 3em; margin: 0; text-transform: uppercase; letter-spacing: 2px;">¡ASCENSO CONSEGUIDO!</h1>
            <p style="color: #aaa; font-size: 1.2em; margin-top: 10px;">Has roto tus límites y cruzado a la siguiente liga.</p>
            <h1 style="color: {color}; font-size: 4em; margin: 20px 0; text-shadow: 0 0 20px {color};">{st.session_state.rango_alcanzado_nombre}</h1>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    if st.button("ACEPTAR MI NUEVO PODER", type="primary", use_container_width=True):
        st.session_state.estado = "victoria"
        st.rerun()
        
elif st.session_state.estado == "victoria":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/crowds/crowd_cheering.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #00ff00; font-size: 4em; text-transform: uppercase; text-shadow: 0 0 20px rgba(0,255,0,0.4);'>🏆 VICTORIA</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #00ff00; font-size: 3em;'>+{st.session_state.elo_premio} ELO</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.4);'>🪙 +{st.session_state.monedas_ganadas_recientes} MONEDAS A LA BÓVEDA</h3>", unsafe_allow_html=True)
    st.success(f"Misión Cumplida: *'{st.session_state.mision_actual}'*. Tu disciplina de hierro ha aplastado a **{st.session_state.rival_nombre}**.")
    
    st.markdown(f"""
        <div style='background-color: #1a1a1a; padding: 20px; border-left: 5px solid #00ff00; margin: 20px 0;'>
            <p style='font-style: italic; font-size: 1.2em; color: #ddd;'>"{st.session_state.ultima_pildora['texto']}"</p>
            <p style='text-align: right; color: #00ff00; font-weight: bold;'>— {st.session_state.ultima_pildora['autor']}</p>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    
    if st.button("Reclamar y Volver", use_container_width=True): 
        st.session_state.estado = "lobby"
        st.rerun()
