import streamlit as st
import time
import random
from datetime import datetime, timedelta, timezone
import streamlit.components.v1 as components
from supabase import create_client, Client

# --- IMPORTACIONES MODULARES (TU NUEVO EJÉRCITO) ---
from datos import pildoras, MISIONES_DESARROLLO, MISIONES_FISICAS, MISIONES_SOCIALES, MISIONES_MENTALES, MISIONES_ORDEN
from motor import get_rank_info, calcular_rango, calcular_riesgo_recompensa, generar_codigo_sala, tiene_boost_activo
from interfaz import cargar_css, generar_carta_html, generar_html_mision, render_top_bar
LOGO_URL = "https://raw.githubusercontent.com/ferranvalletfuertes-dotcom/la-arena-app/main/logo.png"

st.set_page_config(page_title="Modo Combate | La Arena", page_icon=LOGO_URL, layout="centered")

# Inyectar CSS modular
cargar_css()

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
if 'idioma' not in st.session_state: st.session_state.idioma = 'en' # Ponemos inglés por defecto para atacar el mercado global
if 'usuario_id' not in st.session_state: st.session_state.usuario_id = None
if 'estado' not in st.session_state: st.session_state.estado = "login"
if 'puntos_elo' not in st.session_state: st.session_state.puntos_elo = 100
if 'racha' not in st.session_state: st.session_state.racha = 0
if 'monedas' not in st.session_state: st.session_state.monedas = 0
if 'nombre_guerra' not in st.session_state: st.session_state.nombre_guerra = ""
if 'ultima_pildora' not in st.session_state: st.session_state.ultima_pildora = None
if 'partida_id' not in st.session_state: st.session_state.partida_id = None
if 'inicio_busqueda' not in st.session_state: st.session_state.inicio_busqueda = 0
if 'rival_nombre' not in st.session_state: st.session_state.rival_nombre = "Desconocido"
if 'rival_elo' not in st.session_state: st.session_state.rival_elo = 100
if 'monedas_ganadas_recientes' not in st.session_state: st.session_state.monedas_ganadas_recientes = 0
if 'mision_actual' not in st.session_state: st.session_state.mision_actual = ""
if 'rival_mision' not in st.session_state: st.session_state.rival_mision = "Desconocido"
if 'tiempo_combate' not in st.session_state: st.session_state.tiempo_combate = 10
if 'elo_premio' not in st.session_state: st.session_state.elo_premio = 0
if 'elo_castigo' not in st.session_state: st.session_state.elo_castigo = 0
if 'skin_activa' not in st.session_state: st.session_state.skin_activa = 'default'
if 'inv_aura' not in st.session_state: st.session_state.inv_aura = False
if 'inv_corona' not in st.session_state: st.session_state.inv_corona = False
if 'inv_sombra' not in st.session_state: st.session_state.inv_sombra = False
if 'inv_fuego' not in st.session_state: st.session_state.inv_fuego = False
if 'boost_elo' not in st.session_state: st.session_state.boost_elo = None
if 'boost_monedas' not in st.session_state: st.session_state.boost_monedas = None
if 'rival_skin' not in st.session_state: st.session_state.rival_skin = 'default'
if 'tipo_partida' not in st.session_state: st.session_state.tipo_partida = "publica"
if 'codigo_sala' not in st.session_state: st.session_state.codigo_sala = ""
if 'premio_cofre' not in st.session_state: st.session_state.premio_cofre = ""
if 'premio_duplicado' not in st.session_state: st.session_state.premio_duplicado = False

# ESTADÍSTICAS Y MISIONES
if 'victorias' not in st.session_state: st.session_state.victorias = 0
if 'derrotas' not in st.session_state: st.session_state.derrotas = 0
if 'minutos_focus' not in st.session_state: st.session_state.minutos_focus = 0
if 'rango_alcanzado_nombre' not in st.session_state: st.session_state.rango_alcanzado_nombre = ""
if 'rango_alcanzado_color' not in st.session_state: st.session_state.rango_alcanzado_color = ""
if 'ultima_fecha_misiones' not in st.session_state: st.session_state.ultima_fecha_misiones = ""
if 'progreso_m1' not in st.session_state: st.session_state.progreso_m1 = 0
if 'progreso_m2' not in st.session_state: st.session_state.progreso_m2 = 0
if 'progreso_m3' not in st.session_state: st.session_state.progreso_m3 = 0
if 'm1_reclamada' not in st.session_state: st.session_state.m1_reclamada = False
if 'm2_reclamada' not in st.session_state: st.session_state.m2_reclamada = False
if 'm3_reclamada' not in st.session_state: st.session_state.m3_reclamada = False
if 'input_mision_texto' not in st.session_state: st.session_state.input_mision_texto = ""
if 'bautismo_visto' not in st.session_state: st.session_state.bautismo_visto = False

# MISIONES DEL GREMIO
if 'gremio_fecha' not in st.session_state: st.session_state.gremio_fecha = ""
if 'gremio_m1' not in st.session_state: st.session_state.gremio_m1 = False
if 'gremio_m2' not in st.session_state: st.session_state.gremio_m2 = False
if 'gremio_m3' not in st.session_state: st.session_state.gremio_m3 = False
if 'gremio_m4' not in st.session_state: st.session_state.gremio_m4 = False

# --- MOTOR DE TRADUCCIÓN NATIVO (NIVEL 8) ---
# --- MOTOR DE TRADUCCIÓN NATIVO (NIVEL 8) ---
# --- MOTOR DE TRADUCCIÓN NATIVO (NIVEL 8) ---
# --- MOTOR DE TRADUCCIÓN NATIVO (NIVEL 8) ---
DIC = {
    "es": {
        "log_title": "MÁS QUE UNA APP. UN COLISEO.", "log_manifesto": "El mundo moderno te quiere débil, distraído y adicto. La Arena es tu cura.", "log_carcel_tit": "⛓️ EL CENTINELA", "log_carcel_desc": "Inicia un combate. Si abandonas la app, tu escudo colapsa y tu rango es destruido.", "log_mercado_tit": "🛒 EL MERCADO NEGRO", "log_mercado_desc": "Gana oro con tu sudor. Compra skins, auras y multiplicadores.", "log_ranking_tit": "🏆 LA TABERNA", "log_ranking_desc": "Compara tu ELO con guerreros de todo el mundo. Solo la élite asciende.", "tab_login": "🔑 ENTRAR AL COLISEO", "tab_reg": "🩸 JURAMENTO DE SANGRE", "ph_email": "Tu correo de combate", "ph_pass": "Tu contraseña", "btn_acceder": "ENTRAR A LA ARENA", "ph_name": "Nombre de Guerra (Ej: Espartano)", "ph_ref": "Código de Embajador (Opcional)", "btn_jurar": "JURAR LEALTAD", "ajustes_titulo": "⚙️ Ajustes de Perfil", "ajustes_nombre": "Cambiar nombre (cambiará tu código)", "ajustes_musica": "Radio de Combate (Música)", "ajustes_volumen": "Volumen de la Radio", "ajustes_idioma": "Idioma / Language", "ajustes_btn": "ACTUALIZAR AJUSTES",
        # LOBBY
        "lob_titulo": "⚔️ MODO COMBATE", "lob_bienvenido": "Bienvenido", "lob_leyenda": "TU LEYENDA", "lob_rango": "Tu Rango", "lob_boveda": "Bóveda", "lob_contratos": "📜 CONTRATOS MERCENARIOS", "lob_progreso": "Progreso Diario", "lob_reclamado": "✅ RECLAMADO", "lob_reclamar": "🎁 RECLAMAR", "lob_falta": "Falta", "lob_faltan": "Faltan", "lob_leyes_tit": "⚠️ Las Leyes de la Arena", "lob_leyes_1": "📱 <span class='neon-green'>CÓMO SE JUEGA:</span> Abre esto en tu móvil, déjalo en la mesa y ve a trabajar en tu PC o en tus libros.", "lob_leyes_2": "🔴 <span class='neon-red'>CÓMO PIERDES:</span> Si coges el móvil y cambias de app, tu escudo colapsa y pierdes ELO.", "lob_leyes_3": "⚔️ <strong style='color: #ffd700;'>EL PACTO:</strong> Convierte tu móvil en tu propio vigilante. No te engañes a ti mismo.", "lob_declaracion": "🔥 DECLARACIÓN DE INTENCIONES", "lob_ph_mision": "Ej: Terminar el ensayo de Filosofía...", "lob_duracion": "Duración de la batalla:", "lob_busqueda": "🌍 BÚSQUEDA MUNDIAL", "lob_duelo_priv": "🤝 DUELO PRIVADO", "lob_ph_codigo": "Pega código o vacío para crear", "lob_btn_priv": "🚪 CREAR / UNIRSE",
        # TIENDA
        "tie_tit": "🛒 EL MERCADO NEGRO", "tie_fondos": "Fondos Disponibles", "tie_cofre_tit": "### 🎲 EL COFRE DEL GLADIADOR", "tie_cofre_sub": "Cofre Misterioso", "tie_cofre_btn": "🎲 ABRIR COFRE (1000 Monedas)", "tie_boosts": "### 🧬 BOOSTS DIRECTOS (24H)", "tie_comprar": "COMPRAR", "tie_equipar": "EQUIPAR", "tie_equipada": "EQUIPADA", "tie_compra_dir": "### 🔥 COMPRA DIRECTA", "tie_quitar": "✖ QUITAR SKIN ACTUAL", "tie_oculto_tit": "👁️ EL MERCADO OCULTO", "tie_oculto_desc": "Solo los guerreros que han superado los 1000 ELO son dignos de introducir la palabra de paso.", "tie_oculto_ph": "Código de Ascensión", "tie_oculto_btn": "⚡ DESCIFRAR",
        # GREMIO
        "gre_tit": "⚔️ EL GREMIO", "gre_sub": "Conquista la realidad fuera de la pantalla", "gre_mis": "📜 MISIONES DIARIAS", "gre_aviso": "El sistema no puede verificar tu mundo físico. Tu honor es tu única garantía. Engañar al sistema corrompe tu disciplina real.", "gre_sup": "✅ SUPERADO", "gre_hacer": "🩸 LO HE HECHO",
        # MUNDO
        "mun_tit": "🌍 LA PLAZA PÚBLICA", "mun_sub": "El mundo está observando.", "mun_tab1": "🌍 EL RADAR", "mun_tab2": "💬 LA TABERNA", "mun_top": "🏆 TOP GLOBAL", "mun_muro": "📡 MURO EN DIRECTO", "mun_silencio": "El silencio reina en la arena...", "mun_leyendas": "📜 LEYENDAS INMORTALES", "mun_ley_sub": "El Salón de los Dioses. Solo los ganadores de temporadas pasadas.", "mun_ley_vacio": "El pedestal está vacío. Sé tú el primero.", "mun_chat_tit": "💬 LA TABERNA GLOBAL", "mun_chat_vacio": "La taberna está vacía. Escribe el primer mensaje.", "mun_chat_err": "⚠️ Error al cargar la taberna.", "mun_ph_chat": "Habla, guerrero...", "mun_btn_chat": "ENVIAR"
    },
    "en": {
        "log_title": "MORE THAN AN APP. A COLOSSEUM.", "log_manifesto": "The modern world wants you weak, distracted, and addicted. The Arena is your cure.", "log_carcel_tit": "⛓️ THE SENTINEL", "log_carcel_desc": "Start a combat. If you leave the app, your shield collapses and your rank is destroyed.", "log_mercado_tit": "🛒 THE BLACK MARKET", "log_mercado_desc": "Earn gold with your sweat. Buy skins, auras, and multipliers.", "log_ranking_tit": "🏆 THE TAVERN", "log_ranking_desc": "Compare your ELO with warriors worldwide. Only the elite ascend.", "tab_login": "🔑 ENTER COLOSSEUM", "tab_reg": "🩸 BLOOD OATH", "ph_email": "Your combat email", "ph_pass": "Your password", "btn_acceder": "ENTER THE ARENA", "ph_name": "War Name (Ex: Spartan)", "ph_ref": "Ambassador Code (Optional)", "btn_jurar": "SWEAR LOYALTY", "ajustes_titulo": "⚙️ Profile Settings", "ajustes_nombre": "Change name (will change your code)", "ajustes_musica": "Combat Radio (Music)", "ajustes_volumen": "Radio Volume", "ajustes_idioma": "Language / Idioma", "ajustes_btn": "UPDATE SETTINGS",
        # LOBBY
        "lob_titulo": "⚔️ COMBAT MODE", "lob_bienvenido": "Welcome", "lob_leyenda": "YOUR LEGEND", "lob_rango": "Your Rank", "lob_boveda": "Vault", "lob_contratos": "📜 MERCENARY CONTRACTS", "lob_progreso": "Daily Progress", "lob_reclamado": "✅ CLAIMED", "lob_reclamar": "🎁 CLAIM", "lob_falta": "Need", "lob_faltan": "Need", "lob_leyes_tit": "⚠️ The Laws of the Arena", "lob_leyes_1": "📱 <span class='neon-green'>HOW TO PLAY:</span> Open this on your phone, leave it on the desk and work on your PC or books.", "lob_leyes_2": "🔴 <span class='neon-red'>HOW YOU LOSE:</span> If you pick up your phone and change apps, your shield collapses and you lose ELO.", "lob_leyes_3": "⚔️ <strong style='color: #ffd700;'>THE PACT:</strong> Turn your phone into your own warden. Do not deceive yourself.", "lob_declaracion": "🔥 DECLARATION OF INTENT", "lob_ph_mision": "Ex: Finish the Philosophy essay...", "lob_duracion": "Battle duration:", "lob_busqueda": "🌍 GLOBAL SEARCH", "lob_duelo_priv": "🤝 PRIVATE DUEL", "lob_ph_codigo": "Paste code or leave empty to create", "lob_btn_priv": "🚪 CREATE / JOIN",
        # TIENDA
        "tie_tit": "🛒 THE BLACK MARKET", "tie_fondos": "Available Funds", "tie_cofre_tit": "### 🎲 GLADIATOR'S CHEST", "tie_cofre_sub": "Mystery Chest", "tie_cofre_btn": "🎲 OPEN CHEST (1000 Coins)", "tie_boosts": "### 🧬 DIRECT BOOSTS (24H)", "tie_comprar": "BUY", "tie_equipar": "EQUIP", "tie_equipada": "EQUIPPED", "tie_compra_dir": "### 🔥 DIRECT PURCHASE", "tie_quitar": "✖ REMOVE CURRENT SKIN", "tie_oculto_tit": "👁️ THE HIDDEN MARKET", "tie_oculto_desc": "Only warriors who have surpassed 1000 ELO are worthy of entering the password.", "tie_oculto_ph": "Ascension Code", "tie_oculto_btn": "⚡ DECIPHER",
        # GREMIO
        "gre_tit": "⚔️ THE GUILD", "gre_sub": "Conquer reality off-screen", "gre_mis": "📜 DAILY MISSIONS", "gre_aviso": "The system cannot verify your physical world. Your honor is your only guarantee. Cheating the system corrupts your real discipline.", "gre_sup": "✅ COMPLETED", "gre_hacer": "🩸 I DID IT",
        # MUNDO
        "mun_tit": "🌍 THE PUBLIC SQUARE", "mun_sub": "The world is watching.", "mun_tab1": "🌍 THE RADAR", "mun_tab2": "💬 THE TAVERN", "mun_top": "🏆 GLOBAL TOP", "mun_muro": "📡 LIVE FEED", "mun_silencio": "Silence rules the arena...", "mun_leyendas": "📜 IMMORTAL LEGENDS", "mun_ley_sub": "The Hall of Gods. Only past season winners.", "mun_ley_vacio": "The pedestal is empty. Be the first.", "mun_chat_tit": "💬 GLOBAL TAVERN", "mun_chat_vacio": "The tavern is empty. Write the first message.", "mun_chat_err": "⚠️ Error loading the tavern.", "mun_ph_chat": "Speak, warrior...", "mun_btn_chat": "SEND"
    }
}

def t(clave):
    idioma = st.session_state.get('idioma', 'es')
    return DIC.get(idioma, DIC["es"]).get(clave, clave)

def render_navbar(activo):
    import streamlit as st
    idioma = st.session_state.get('idioma', 'es')
    
    # Diccionario blindado e independiente
    nav_txt = {
        "es": ["🔥 LOBBY", "🌍 MUNDO", "🛡️ CUARTEL", "🛒 TIENDA", "⚔️ GREMIO"],
        "en": ["🔥 LOBBY", "🌍 WORLD", "🛡️ BARRACKS", "🛒 STORE", "⚔️ GUILD"]
    }
    txt = nav_txt.get(idioma, nav_txt["es"])

    st.write("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        if st.button(txt[0], use_container_width=True, type="primary" if activo == "lobby" else "secondary", key=f"btn_global_1_{activo}"):
            st.session_state.estado = "lobby"; st.rerun()
    with c2:
        if st.button(txt[1], use_container_width=True, type="primary" if activo == "mundo" else "secondary", key=f"btn_global_2_{activo}"):
            st.session_state.estado = "mundo"; st.rerun()
    with c3:
        if st.button(txt[2], use_container_width=True, type="primary" if activo == "cuartel" else "secondary", key=f"btn_global_3_{activo}"):
            st.session_state.estado = "cuartel"; st.rerun()
    with c4:
        if st.button(txt[3], use_container_width=True, type="primary" if activo == "tienda" else "secondary", key=f"btn_global_4_{activo}"):
            st.session_state.estado = "tienda"; st.rerun()
    with c5:
        if st.button(txt[4], use_container_width=True, type="primary" if activo == "gremio" else "secondary", key=f"btn_global_5_{activo}"):
            st.session_state.estado = "gremio"; st.rerun()
# ==========================================================
# RUTAS DE LA APLICACIÓN
# ==========================================================

# --- RADIO DE COMBATE ---
if 'musica_fondo' not in st.session_state: st.session_state.musica_fondo = "Lo-Fi (Concentración)"
if 'volumen' not in st.session_state: st.session_state.volumen = 0.2

CINTAS_AUDIO = {
    "Silencio Total": "",
    "Lo-Fi (Concentración)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "Dreamcore (Viaje)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "Phonk / Epic (Guerra)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "Synthwave (Nocturno)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
}
# --- LA PUERTA DE SEGURIDAD (SPLIT-SCREEN Y BILINGÜE) ---
if st.session_state.estado == "login":
    render_top_bar() 
    lang = st.session_state.idioma 
    
    st.write("") 
    c_hero, c_espacio, c_login = st.columns([1.2, 0.1, 1])
    
    with c_hero:
        st.markdown(f"<div style='text-align: left;'><img src='{LOGO_URL}' width='150' class='logo-breathe' style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='epic-title' style='text-align: left;'>{DIC[lang]['log_title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='manifesto' style='text-align: left; margin-bottom: 25px;'>{DIC[lang]['log_manifesto']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='background: linear-gradient(90deg, #161616 0%, transparent 100%); border-left: 3px solid #ff4b4b; padding: 15px; margin-bottom: 15px; border-radius: 4px;'>
                <h4 style='color: white; margin: 0; font-size: 15px; text-transform: uppercase;'>{DIC[lang]['log_carcel_tit']}</h4>
                <p style='color: #888; margin: 0; font-size: 13px;'>{DIC[lang]['log_carcel_desc']}</p>
            </div>
            <div style='background: linear-gradient(90deg, #161616 0%, transparent 100%); border-left: 3px solid #ffd700; padding: 15px; margin-bottom: 15px; border-radius: 4px;'>
                <h4 style='color: white; margin: 0; font-size: 15px; text-transform: uppercase;'>{DIC[lang]['log_mercado_tit']}</h4>
                <p style='color: #888; margin: 0; font-size: 13px;'>{DIC[lang]['log_mercado_desc']}</p>
            </div>
            <div style='background: linear-gradient(90deg, #161616 0%, transparent 100%); border-left: 3px solid #00ff00; padding: 15px; border-radius: 4px;'>
                <h4 style='color: white; margin: 0; font-size: 15px; text-transform: uppercase;'>{DIC[lang]['log_ranking_tit']}</h4>
                <p style='color: #888; margin: 0; font-size: 13px;'>{DIC[lang]['log_ranking_desc']}</p>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    with c_login:
        st.write(""); st.write("")
        tab1, tab2 = st.tabs([DIC[lang]['tab_login'], DIC[lang]['tab_reg']])
        
        with tab1:
            email_log = st.text_input(DIC[lang]['ph_email'], key="log_email")
            pass_log = st.text_input(DIC[lang]['ph_pass'], type="password", key="log_pass")
            if st.button(DIC[lang]['btn_acceder'], type="primary", use_container_width=True):
                try:
                    respuesta = supabase.auth.sign_in_with_password({"email": email_log, "password": pass_log})
                    user_id = respuesta.user.id; st.session_state.usuario_id = user_id
                    datos = supabase.table("jugadores").select("*").eq("id", user_id).execute()
                    
                    if len(datos.data) > 0:
                        d = datos.data[0]
                        st.session_state.puntos_elo = d.get('elo', 100)
                        st.session_state.racha = d.get('racha', 0)
                        st.session_state.monedas = d.get('monedas', 0)
                        st.session_state.nombre_guerra = d.get('nombre', 'Guerrero')
                        st.session_state.musica_fondo = d.get('musica') if d.get('musica') else 'Lo-Fi (Concentración)'
                        st.session_state.volumen = d.get('volumen') if d.get('volumen') is not None else 0.2
                        st.session_state.skin_activa = d.get('skin_activa', 'default')
                        st.session_state.inv_aura = d.get('inventario_aura', False)
                        st.session_state.inv_corona = d.get('inventario_corona', False)
                        st.session_state.inv_sombra = d.get('inv_sombra', False)
                        st.session_state.inv_fuego = d.get('inv_fuego', False)
                        st.session_state.boost_elo = d.get('boost_elo_hasta')
                        st.session_state.boost_monedas = d.get('boost_monedas_hasta')
                        st.session_state.victorias = d.get('victorias', 0)
                        st.session_state.derrotas = d.get('derrotas', 0)
                        st.session_state.minutos_focus = d.get('minutos_focus', 0)
                        st.session_state.bautismo_visto = d.get('bautismo_completado', False)
                        
                        st.session_state.gremio_fecha = d.get('gremio_fecha', "")
                        st.session_state.gremio_m1 = d.get('gremio_m1', False)
                        st.session_state.gremio_m2 = d.get('gremio_m2', False)
                        st.session_state.gremio_m3 = d.get('gremio_m3', False)
                        st.session_state.gremio_m4 = d.get('gremio_m4', False)
                        
                        fecha_db = d.get('ultima_fecha_misiones'); hoy_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
                        if fecha_db != hoy_str:
                            supabase.table("jugadores").update({"ultima_fecha_misiones": hoy_str, "progreso_m1": 0, "progreso_m2": 0, "progreso_m3": 0, "m1_reclamada": False, "m2_reclamada": False, "m3_reclamada": False}).eq("id", user_id).execute()
                            st.session_state.ultima_fecha_misiones = hoy_str; st.session_state.progreso_m1 = 0; st.session_state.progreso_m2 = 0; st.session_state.progreso_m3 = 0; st.session_state.m1_reclamada = False; st.session_state.m2_reclamada = False; st.session_state.m3_reclamada = False
                        else:
                            st.session_state.ultima_fecha_misiones = fecha_db; st.session_state.progreso_m1 = d.get('progreso_m1', 0); st.session_state.progreso_m2 = d.get('progreso_m2', 0); st.session_state.progreso_m3 = d.get('progreso_m3', 0); st.session_state.m1_reclamada = d.get('m1_reclamada', False); st.session_state.m2_reclamada = d.get('m2_reclamada', False); st.session_state.m3_reclamada = d.get('m3_reclamada', False)
                            
                        if not st.session_state.bautismo_visto: st.session_state.estado = "bautismo"
                        else: st.session_state.estado = "lobby"
                    else: st.error("No se encontraron los datos del guerrero."); st.stop()
                    st.rerun()
                except Exception as e: st.error("❌ El sistema no reconoce tus credenciales.")
                    
        with tab2:
            email_reg = st.text_input(DIC[lang]['ph_email'], key="reg_email")
            nombre_reg = st.text_input(DIC[lang]['ph_name'], key="reg_nombre")
            pass_reg = st.text_input(DIC[lang]['ph_pass'], type="password", key="reg_pass")
            referido_reg = st.text_input(DIC[lang]['ph_ref'], key="reg_ref")
            
            if st.button(DIC[lang]['btn_jurar'], type="primary", use_container_width=True):
                if not nombre_reg: 
                    st.error("Necesitas un nombre de guerra.")
                else:
                    try:
                        monedas_iniciales = 0
                        if referido_reg:
                            reclutador_data = supabase.table("jugadores").select("id, monedas").eq("nombre", referido_reg.strip()).execute()
                            if len(reclutador_data.data) > 0:
                                r_id = reclutador_data.data[0]['id']
                                r_monedas = reclutador_data.data[0]['monedas']
                                supabase.table("jugadores").update({"monedas": r_monedas + 1000}).eq("id", r_id).execute()
                                monedas_iniciales = 500
                                st.success(f"¡Reclutado por {referido_reg}! Entras con 500 monedas extra.")
                            else: 
                                st.warning("Código de embajador no existe.")
                                
                        auth_resp = supabase.auth.sign_up({"email": email_reg, "password": pass_reg})
                        hoy_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
                        supabase.table("jugadores").insert({
                            "id": auth_resp.user.id, "elo": 100, "racha": 0, "monedas": monedas_iniciales, 
                            "nombre": nombre_reg, "ultima_fecha_misiones": hoy_str, "victorias": 0, "derrotas": 0,
                            "minutos_focus": 0, "bautismo_completado": False, "gremio_fecha": "", "referido_por": referido_reg if referido_reg else None
                        }).execute()
                        st.success("¡Registrado! Ve a 'Entrar al Coliseo'.")
                    except Exception as e: 
                        st.error("Fallo en el registro.")
# --- EL LOBBY BILINGÜE ---
# --- EL LOBBY BILINGÜE ---
elif st.session_state.estado == "lobby":
    render_top_bar()
    st.session_state.partida_id = None
    st.session_state.rival_nombre = "Desconocido"
    rango_n, rango_s, rango_i, rango_c = calcular_rango(st.session_state.puntos_elo)

    st.markdown(f"<div style='text-align: center;'><img src='{LOGO_URL}' width='80' style='border-radius: 15px; box-shadow: 0 0 15px #ff4b4b; margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='epic-title'>{t('lob_titulo')}</h1>", unsafe_allow_html=True)
    
    boosts_html = ""
    if tiene_boost_activo(st.session_state.boost_elo): boosts_html += "<span style='background:#ff4b4b; color:white; padding:2px 8px; border-radius:10px; font-size:12px; font-weight:bold; margin-right:5px;'>⚡ x2 ELO</span>"
    if tiene_boost_activo(st.session_state.boost_monedas): boosts_html += "<span style='background:#ffd700; color:black; padding:2px 8px; border-radius:10px; font-size:12px; font-weight:bold;'>💰 x2 MONEDAS</span>"
    
    st.markdown(f"<h3 style='text-align: center; color: white; text-transform: uppercase;'>{t('lob_bienvenido')}, {st.session_state.nombre_guerra} <br><div style='margin-top:10px;'>{boosts_html}</div></h3>".replace('\n', ''), unsafe_allow_html=True)
    st.divider()
    
    carta_propia = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, rango_i, rango_c, t('lob_leyenda'), st.session_state.skin_activa)
    st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'>{carta_propia}</div>".replace('\n', ''), unsafe_allow_html=True)
    
    st.markdown(f"<div style='display: flex; justify-content: space-around; text-align: center; background-color: #121212; padding: 25px; border-radius: 12px; border: 1px solid {rango_c}; box-shadow: 0 4px 20px {rango_c}40;'><div><p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase;'>{t('lob_rango')}</p><h2 style='margin: 0; color: {rango_c};'>{rango_i} {rango_n}</h2></div><div style='border-left: 1px solid #333; border-right: 1px solid #333; padding: 0 20px;'><p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase;'>ELO</p><h2 style='margin: 0; color: white;'>{st.session_state.puntos_elo} pts</h2></div><div><p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase;'>{t('lob_boveda')}</p><h2 style='margin: 0; color: #ffd700;'>🪙 {st.session_state.monedas}</h2></div></div>".replace('\n', ''), unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='text-align: center; color: #00ff00; margin-top: 40px; text-shadow: 0 0 10px rgba(0,255,0,0.4);'>{t('lob_contratos')}</h3>", unsafe_allow_html=True)
    
    pasos_totales = 4
    pasos_actuales = min(st.session_state.progreso_m1, 1) + min(st.session_state.progreso_m2, 2) + min(st.session_state.progreso_m3, 1)
    porcentaje = int((pasos_actuales / pasos_totales) * 100)
    st.markdown(f"<div style='width: 100%; background-color: #333; border-radius: 10px; margin-bottom: 20px;'><div style='width: {porcentaje}%; height: 15px; background: linear-gradient(90deg, #008000, #00ff00); border-radius: 10px; box-shadow: 0 0 10px #00ff00; transition: width 0.5s ease;'></div></div><p style='text-align: center; color: #888; font-size: 12px; margin-top: -10px;'>{t('lob_progreso')}: {porcentaje}%</p>".replace('\n', ''), unsafe_allow_html=True)
    
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown(generar_html_mision("Primer Sangrado", "Gana 1 combate", 50, st.session_state.m1_reclamada), unsafe_allow_html=True)
        if st.session_state.m1_reclamada: 
            st.button(t('lob_reclamado'), disabled=True, key="btn_m1_d", use_container_width=True)
        elif st.session_state.progreso_m1 >= 1:
            if st.button(t('lob_reclamar'), type="primary", key="btn_m1_c", use_container_width=True):
                st.session_state.monedas += 50
                st.session_state.m1_reclamada = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "m1_reclamada": True}).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else: 
            st.button(f"{t('lob_falta')} 1", disabled=True, key="btn_m1_f", use_container_width=True)
    with c_m2:
        st.markdown(generar_html_mision("Asesino a Sueldo", "Gana 2 escaramuzas", 100, st.session_state.m2_reclamada), unsafe_allow_html=True)
        if st.session_state.m2_reclamada: 
            st.button(t('lob_reclamado'), disabled=True, key="btn_m2_d", use_container_width=True)
        elif st.session_state.progreso_m2 >= 2:
            if st.button(t('lob_reclamar'), type="primary", key="btn_m2_c", use_container_width=True):
                st.session_state.monedas += 100
                st.session_state.m2_reclamada = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "m2_reclamada": True}).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else: 
            st.button(f"{t('lob_faltan')} {2 - st.session_state.progreso_m2}", disabled=True, key="btn_m2_f", use_container_width=True)
    with c_m3:
        st.markdown(generar_html_mision("El Titán", "Sobrevive 1 asalto", 300, st.session_state.m3_reclamada), unsafe_allow_html=True)
        if st.session_state.m3_reclamada: 
            st.button(t('lob_reclamado'), disabled=True, key="btn_m3_d", use_container_width=True)
        elif st.session_state.progreso_m3 >= 1:
            if st.button(t('lob_reclamar'), type="primary", key="btn_m3_c", use_container_width=True):
                st.session_state.monedas += 300
                st.session_state.m3_reclamada = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "m3_reclamada": True}).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else: 
            st.button(f"{t('lob_falta')} 1", disabled=True, key="btn_m3_f", use_container_width=True)

    st.write(""); st.divider()
    st.markdown(f"""
        <div class="rules-box">
            <h3 style="text-align: center; color: #ff4b4b; text-transform: uppercase; margin-top: 0;">{t('lob_leyes_tit')}</h3>
            <ul style="list-style-type: none; padding-left: 0; color: #ccc; font-size: 15px; line-height: 1.8;">
                <li style="margin-bottom: 10px;">{t('lob_leyes_1')}</li>
                <li style="margin-bottom: 10px;">{t('lob_leyes_2')}</li>
                <li>{t('lob_leyes_3')}</li>
            </ul>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)

    st.markdown(f"<h3 style='text-align: center; color: #ff4b4b;'>{t('lob_declaracion')}</h3>", unsafe_allow_html=True)
    c_texto, c_dado = st.columns([5, 1])
    with c_dado:
        st.write("")
        if st.button("🎲", help="Oráculo", use_container_width=True):
            st.session_state.input_mision_texto = random.choice(MISIONES_DESARROLLO)
            st.rerun()
    with c_texto:
        mision_input = st.text_input("", value=st.session_state.input_mision_texto, placeholder=t('lob_ph_mision'), label_visibility="collapsed")
        st.session_state.input_mision_texto = mision_input 
    
    tiempo_opts = {
        "⚙️ Modo Test (10 Segundos)": 10,
        "⏱️ 15 Minutos": 900,
        "⏱️ 20 Minutos": 1200,
        "⚔️ Escaramuza (25 Minutos)": 1500,
        "⏱️ 30 Minutos": 1800,
        "⏱️ 35 Minutos": 2100,
        "⏱️ 40 Minutos": 2400,
        "⏱️ 45 Minutos": 2700,
        "🔥 Asalto Profundo (50 Minutos)": 3000,
        "⏱️ 55 Minutos": 3300,
        "⏱️ 60 Minutos": 3600,
        "⏱️ 65 Minutos": 3900,
        "⏱️ 70 Minutos": 4200,
        "⏱️ 75 Minutos": 4500,
        "⏱️ 80 Minutos": 4800,
        "⏱️ 85 Minutos": 5100,
        "💀 Modo Titán (90 Minutos)": 5400,
        "⏱️ 95 Minutos": 5700,
        "⏱️ 100 Minutos": 6000
    }

    tiempo_str = st.selectbox(t('lob_duracion'), list(tiempo_opts.keys()))
    
    c_pub, c_priv = st.columns(2)
    with c_pub:
        if st.button(t('lob_busqueda'), use_container_width=True, type="primary"):
            if not st.session_state.input_mision_texto: 
                st.error("Un guerrero no entra sin propósito. Declara tu misión o usa el dado 🎲.")
            else:
                limite_fantasmas = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
                supabase.table("partidas").delete().eq("estado", "esperando").lt("ultima_actividad", limite_fantasmas).execute()
                st.session_state.mision_actual = st.session_state.input_mision_texto
                st.session_state.tiempo_combate = tiempo_opts[tiempo_str]
                w_elo, l_elo, coins = calcular_riesgo_recompensa(st.session_state.tiempo_combate, st.session_state.puntos_elo, st.session_state.boost_elo, st.session_state.boost_monedas)
                st.session_state.elo_premio = w_elo; st.session_state.elo_castigo = l_elo; st.session_state.monedas_ganadas_recientes = coins
                st.session_state.tipo_partida = "publica"
                st.session_state.codigo_sala = ""
                st.session_state.inicio_busqueda = time.time(); st.session_state.estado = "buscando"; st.rerun()
                
    st.markdown(f"<h3 style='text-align: center; color: #888; margin-top: 30px;'>{t('lob_duelo_priv')}</h3>", unsafe_allow_html=True)
    c_p1, c_p2 = st.columns([2, 1])
    with c_p1: 
        codigo_input = st.text_input("", placeholder=t('lob_ph_codigo'), label_visibility="collapsed", key="input_cod_priv")
    with c_p2:
        if st.button(t('lob_btn_priv'), use_container_width=True):
            codigo_secreto = codigo_input.upper().strip()
            
            if codigo_secreto == "NIVEL8":
                st.session_state.monedas += 777
                supabase.table("jugadores").update({"monedas": st.session_state.monedas}).eq("id", st.session_state.usuario_id).execute()
                st.balloons()
                st.success("💻 ACCESO CLASIFICADO: Has descubierto el Protocolo Nivel 8. El Arquitecto te observa. +777 Monedas transferidas.")
                time.sleep(3)
                st.rerun()
            elif not st.session_state.input_mision_texto: 
                st.error("Un guerrero no entra sin propósito. Declara tu misión o usa el dado 🎲.")
            else:
                st.session_state.mision_actual = st.session_state.input_mision_texto
                st.session_state.tiempo_combate = tiempo_opts[tiempo_str]
                w_elo, l_elo, coins = calcular_riesgo_recompensa(st.session_state.tiempo_combate, st.session_state.puntos_elo, st.session_state.boost_elo, st.session_state.boost_monedas)
                st.session_state.elo_premio = w_elo; st.session_state.elo_castigo = l_elo; st.session_state.monedas_ganadas_recientes = coins
                st.session_state.tipo_partida = "privada"
                st.session_state.codigo_sala = codigo_secreto if codigo_secreto else generar_codigo_sala()
                st.session_state.inicio_busqueda = time.time(); st.session_state.estado = "buscando_privada"; st.rerun()
                
    render_navbar("lobby")
# --- MISIONES SECUNDARIAS (GREMIO) ---
elif st.session_state.estado == "gremio":
    render_top_bar()
    
    st.markdown("<h1 class='epic-title' style='color: #00ff00;'>⚔️ EL GREMIO</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #888; margin-bottom: 40px; text-transform: uppercase; letter-spacing: 2px;'>Conquista la realidad fuera de la pantalla</h4>", unsafe_allow_html=True)

    hoy_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    if st.session_state.gremio_fecha != hoy_str:
        supabase.table("jugadores").update({"gremio_fecha": hoy_str, "gremio_m1": False, "gremio_m2": False, "gremio_m3": False, "gremio_m4": False}).eq("id", st.session_state.usuario_id).execute()
        st.session_state.gremio_fecha = hoy_str; st.session_state.gremio_m1 = False; st.session_state.gremio_m2 = False; st.session_state.gremio_m3 = False; st.session_state.gremio_m4 = False

    st.markdown("""
        <div style='background-color: #111; border-left: 4px solid #00ff00; border-radius: 8px; padding: 20px; margin-bottom: 40px; box-shadow: 0 4px 15px rgba(0,255,0,0.1);'>
            <h3 style='color: white; margin-top: 0; display: flex; justify-content: space-between;'>
                <span>📜 MISIONES DIARIAS</span>
                <span style='color: #ffd700;'>Bóveda: 🪙 {monedas}</span>
            </h3>
            <p style='color: #888; margin: 0; font-size: 14px;'>El sistema no puede verificar tu mundo físico. Tu honor es tu única garantía. Engañar al sistema corrompe tu disciplina real.</p>
        </div>
    """.replace('{monedas}', str(st.session_state.monedas)), unsafe_allow_html=True)

    random.seed(f"{st.session_state.usuario_id}_{hoy_str}")
    t1, d1 = "FÍSICO", random.choice(MISIONES_FISICAS)
    t2, d2 = "SOCIAL", random.choice(MISIONES_SOCIALES)
    t3, d3 = "MENTAL", random.choice(MISIONES_MENTALES)
    t4, d4 = "DISCIPLINA", random.choice(MISIONES_ORDEN)
    random.seed() 

    # --- DISEÑO ESPACIADO EN 2 COLUMNAS ---
    g1, g2 = st.columns(2)
    
    with g1:
        st.markdown(f"<div style='margin-bottom: 10px;'>", unsafe_allow_html=True)
        st.markdown(generar_html_mision(t1, d1, 15, st.session_state.gremio_m1), unsafe_allow_html=True)
        if st.session_state.gremio_m1: 
            st.button("✅ SUPERADO", disabled=True, key="g_m1_d", use_container_width=True)
        else:
            if st.button("🩸 LO HE HECHO", type="primary", key="g_m1_c", use_container_width=True):
                st.session_state.monedas += 15; st.session_state.gremio_m1 = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "gremio_m1": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)
                
        st.markdown(f"<div style='margin-bottom: 10px;'>", unsafe_allow_html=True)
        st.markdown(generar_html_mision(t2, d2, 15, st.session_state.gremio_m2), unsafe_allow_html=True)
        if st.session_state.gremio_m2: 
            st.button("✅ SUPERADO", disabled=True, key="g_m2_d", use_container_width=True)
        else:
            if st.button("🩸 LO HE HECHO", type="primary", key="g_m2_c", use_container_width=True):
                st.session_state.monedas += 15; st.session_state.gremio_m2 = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "gremio_m2": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with g2:
        st.markdown(f"<div style='margin-bottom: 10px;'>", unsafe_allow_html=True)
        st.markdown(generar_html_mision(t3, d3, 15, st.session_state.gremio_m3), unsafe_allow_html=True)
        if st.session_state.gremio_m3: 
            st.button("✅ SUPERADO", disabled=True, key="g_m3_d", use_container_width=True)
        else:
            if st.button("🩸 LO HE HECHO", type="primary", key="g_m3_c", use_container_width=True):
                st.session_state.monedas += 15; st.session_state.gremio_m3 = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "gremio_m3": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)
                
        st.markdown(f"<div style='margin-bottom: 10px;'>", unsafe_allow_html=True)
        st.markdown(generar_html_mision(t4, d4, 15, st.session_state.gremio_m4), unsafe_allow_html=True)
        if st.session_state.gremio_m4: 
            st.button("✅ SUPERADO", disabled=True, key="g_m4_d", use_container_width=True)
        else:
            if st.button("🩸 LO HE HECHO", type="primary", key="g_m4_c", use_container_width=True):
                st.session_state.monedas += 15; st.session_state.gremio_m4 = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "gremio_m4": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")
    render_navbar("gremio")
# --- LA PLAZA PÚBLICA (MUNDO + CHAT) ---
# --- LA PLAZA PÚBLICA (MUNDO + CHAT) ---
elif st.session_state.estado == "mundo":
    st.markdown(f"<h1 style='text-align: center; color: #fff; letter-spacing: 2px;'>{t('mun_tit')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: gray; margin-bottom: 20px;'>{t('mun_sub')}</h4>", unsafe_allow_html=True)
    
    tab_radar, tab_taberna = st.tabs([t('mun_tab1'), t('mun_tab2')])
    
    with tab_radar:
        c_feed, c_rank = st.columns([1.2, 1])
        with c_rank:
            st.markdown(f"<h3 style='color: #ffd700; text-align: center;'>{t('mun_top')}</h3>", unsafe_allow_html=True)
            st.markdown("<div style='background-color: #111; border: 1px solid #333; border-radius: 12px; padding: 15px;'>", unsafe_allow_html=True)
            top_players = supabase.table("jugadores").select("nombre, elo, skin_activa").order("elo", desc=True).limit(10).execute()
            if top_players.data:
                for idx, p in enumerate(top_players.data):
                    p_nombre = p['nombre']; p_elo = p['elo']; r_n, r_s, r_i, r_c = calcular_rango(p_elo)
                    color_pos = "#ffd700" if idx == 0 else "#c0c0c0" if idx == 1 else "#cd7f32" if idx == 2 else "#888"
                    st.markdown(f"<div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; padding: 10px 0;'><div style='display: flex; align-items: center; gap: 10px;'><strong style='color: {color_pos}; font-size: 18px;'>#{idx+1}</strong><span style='color: white; font-weight: bold;'>{p_nombre}</span></div><div style='text-align: right;'><span style='color: {r_c}; font-size: 12px;'>{r_i} {p_elo} pts</span></div></div>".replace('\n', ''), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_feed:
            st.markdown(f"<h3 style='color: #00aaff; text-align: center;'>{t('mun_muro')}</h3>", unsafe_allow_html=True)
            st.markdown("<div class='feed-box' style='background-color: #0a0a0a; border: 1px solid #333; border-radius: 12px; padding: 15px; height: 450px; overflow-y: auto;'>", unsafe_allow_html=True)
            feed = supabase.table("historial").select("*").order("id", desc=True).limit(15).execute()
            if feed.data:
                for f in feed.data:
                    res = f['resultado']; puntos = f['puntos_cambio']; j_nom = f.get('jugador_nombre', 'Un guerrero')
                    
                    texto_es = f"**{j_nom}** completó su misión y roba <span style='color:#00ff00;'>+{puntos} ELO</span>." if res == "victoria" else f"El escudo de **{j_nom}** colapsó. Pierde <span style='color:#ff4b4b;'>{puntos} ELO</span>."
                    texto_en = f"**{j_nom}** completed the mission and steals <span style='color:#00ff00;'>+{puntos} ELO</span>." if res == "victoria" else f"**{j_nom}**'s shield collapsed. Loses <span style='color:#ff4b4b;'>{puntos} ELO</span>."
                    texto = texto_en if st.session_state.get('idioma') == 'en' else texto_es
                    
                    color = "#00ff00" if res == "victoria" else "#ff4b4b"
                    icono = "🟢" if res == "victoria" else "🔴"
                    
                    st.markdown(f"<div style='background-color: #111; border-left: 3px solid {color}; padding: 10px; margin-bottom: 8px; border-radius: 4px;'><p style='color: #ccc; margin: 0; font-size: 13px;'>{icono} {texto}</p></div>".replace('\n', ''), unsafe_allow_html=True)
            else: st.markdown(f"<p style='text-align: center; color: #555;'>{t('mun_silencio')}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown(f"<h3 style='text-align: center; color: #ffd700; margin-top: 20px;'>{t('mun_leyendas')}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #888; font-size: 14px;'>{t('mun_ley_sub')}</p>", unsafe_allow_html=True)
        leyendas = supabase.table("leyendas").select("*").order("temporada", desc=True).execute()
        if leyendas.data:
            for l in leyendas.data:
                st.markdown(f"<div style='background:#1a1a1a; border-left:4px solid {l['rango_color']}; padding:15px; margin-bottom:10px;'><h4 style='margin:0; color:white;'>Temporada {l['temporada']}: {l['nombre']}</h4><p style='margin:0; color:#888;'>{l['rango_icono']} {l['rango_nombre']} - {l['elo_final']} ELO</p></div>".replace('\n', ''), unsafe_allow_html=True)
        else: st.markdown(f"<div style='text-align:center; padding:30px; border:1px dashed #333;'><p style='color:#555; font-style:italic;'>{t('mun_ley_vacio')}</p></div>".replace('\n', ''), unsafe_allow_html=True)

    with tab_taberna:
        st.markdown(f"<h3 style='color: #ff4b4b; text-align: center;'>{t('mun_chat_tit')}</h3>", unsafe_allow_html=True)
        
        st.markdown("<div class='feed-box' style='background-color: #0a0a0a; border: 1px solid #333; border-radius: 12px; padding: 15px; height: 400px; overflow-y: auto; display: flex; flex-direction: column-reverse;'>", unsafe_allow_html=True)
        try:
            chat_data = supabase.table("chat_global").select("*").order("fecha", desc=True).limit(30).execute()
            chat_html = ""
            if chat_data.data:
                for msg in chat_data.data:
                    es_mio = msg['jugador_id'] == st.session_state.usuario_id
                    bg_color = "#1a1a1a" if es_mio else "#111"
                    borde = "#ff4b4b" if es_mio else "#333"
                    chat_html += f"<div style='background-color: {bg_color}; border-left: 3px solid {borde}; padding: 10px; margin-bottom: 8px; border-radius: 4px; text-align: left;'><strong style='color: {borde}; font-size: 12px;'>{msg['nombre_jugador']}</strong><br><span style='color: #ccc; font-size: 14px;'>{msg['mensaje']}</span></div>"
                st.markdown(chat_html, unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='text-align: center; color: #555;'>{t('mun_chat_vacio')}</p>", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"<p style='text-align: center; color: #ff4b4b;'>{t('mun_chat_err')}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            c_input, c_btn = st.columns([4, 1])
            with c_input:
                nuevo_msg = st.text_input("Mensaje", label_visibility="collapsed", placeholder=t('mun_ph_chat'))
            with c_btn:
                submit_btn = st.form_submit_button(t('mun_btn_chat'), use_container_width=True)
            
            if submit_btn and nuevo_msg.strip():
                try:
                    supabase.table("chat_global").insert({
                        "jugador_id": st.session_state.usuario_id,
                        "nombre_jugador": st.session_state.nombre_guerra,
                        "mensaje": nuevo_msg.strip()
                    }).execute()
                    st.rerun()
                except Exception as e:
                    st.error("Error al enviar el mensaje.")
                    
    render_navbar("mundo")

elif st.session_state.estado == "tienda":
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    st.markdown(f"<h1 style='text-align: center; color: #ffd700; letter-spacing: 2px;'>{t('tie_tit')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: #1a1a1a; border: 1px solid #ffd700; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 30px;'><p style='margin:0; color:#aaa; font-size:14px;'>{t('tie_fondos')}</p><h2 style='margin:0; color:#ffd700; font-size:36px;'>🪙 {st.session_state.monedas}</h2></div>".replace('\n', ''), unsafe_allow_html=True)
    
    st.markdown(t('tie_cofre_tit'))
    st.markdown(f"<div style='background:#121212; border:2px solid #ffd700; padding:20px; text-align:center; border-radius:8px;'><h1 style='font-size: 80px; margin:0;'>🧰</h1><h3 style='color: white; margin-top: 10px;'>{t('tie_cofre_sub')}</h3><p style='color: #888; font-size: 12px;'>🟦 70% | 🟪 20% | 🟥 9% | 🟨 1%</p><h2 style='color:#ffd700; margin-bottom: 20px;'>🪙 1000</h2></div>".replace('\n', ''), unsafe_allow_html=True)
    if st.button(t('tie_cofre_btn'), type="primary", use_container_width=True):
        if st.session_state.monedas >= 1000:
            st.session_state.monedas -= 1000; supabase.table("jugadores").update({"monedas": st.session_state.monedas}).eq("id", st.session_state.usuario_id).execute()
            st.session_state.estado = "cofre_animacion"; st.rerun()
        else: st.error("No tienes fondos para el azar.")
    
    st.markdown(t('tie_boosts'))
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("<div style='background:#121212; border:1px solid #333; padding:15px; text-align:center; border-radius:8px;'><h3>⚡ x2 ELO</h3><h3 style='color:#ffd700;'>🪙 150</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.button(t('tie_comprar'), key="b_elo", use_container_width=True):
            if st.session_state.monedas >= 150:
                st.session_state.monedas -= 150; fin = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
                st.session_state.boost_elo = fin; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "boost_elo_hasta": fin}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
            else: st.error("No tienes oro.")
    with b2:
        st.markdown("<div style='background:#121212; border:1px solid #333; padding:15px; text-align:center; border-radius:8px;'><h3>💰 x2 ORO</h3><h3 style='color:#ffd700;'>🪙 200</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.button(t('tie_comprar'), key="b_oro", use_container_width=True):
            if st.session_state.monedas >= 200:
                st.session_state.monedas -= 200; fin = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
                st.session_state.boost_monedas = fin; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "boost_monedas_hasta": fin}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
            else: st.error("No tienes oro.")

    st.markdown(t('tie_compra_dir'))
    t1, t2 = st.columns(2)
    carta_aura = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'aura')
    with t1:
        st.markdown(f"<div style='background:#121212; border:1px solid #ff4b4b; padding:15px; text-align:center; border-radius:8px;'>{carta_aura}<h4 style='margin-top:10px;'>Aura Sanguinaria</h4><p style='color:#ff4b4b;'>Mítica</p><h3 style='color:#ffd700;'>🪙 5000</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.session_state.inv_aura:
            if st.session_state.skin_activa == 'aura': st.info(t('tie_equipada'))
            elif st.button(t('tie_equipar'), key="eq_aura", use_container_width=True): st.session_state.skin_activa = 'aura'; supabase.table("jugadores").update({"skin_activa": "aura"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else:
            if st.button(t('tie_comprar'), key="cp_aura", use_container_width=True):
                if st.session_state.monedas >= 5000: st.session_state.monedas -= 5000; st.session_state.inv_aura = True; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "inventario_aura": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                else: st.error("Ahorra.")
                
    carta_corona = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'corona')
    with t2:
        st.markdown(f"<div style='background:#121212; border:1px solid #ffd700; padding:15px; text-align:center; border-radius:8px;'>{carta_corona}<h4 style='margin-top:10px;'>Corona del Rey</h4><p style='color:#ffd700;'>Legendaria</p><h3 style='color:#ffd700;'>🪙 10000</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.session_state.inv_corona:
            if st.session_state.skin_activa == 'corona': st.info(t('tie_equipada'))
            elif st.button(t('tie_equipar'), key="eq_cor", use_container_width=True): st.session_state.skin_activa = 'corona'; supabase.table("jugadores").update({"skin_activa": "corona"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else:
            if st.button(t('tie_comprar'), key="cp_cor", use_container_width=True):
                if st.session_state.monedas >= 10000: st.session_state.monedas -= 10000; st.session_state.inv_corona = True; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "inventario_corona": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                else: st.error("Ahorra.")

    t3, t4 = st.columns(2)
    carta_sombra = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'sombra')
    with t3:
        st.markdown(f"<div style='background:#121212; border:1px solid #00aaff; padding:15px; text-align:center; border-radius:8px;'>{carta_sombra}<h4 style='margin-top:10px;'>Sombra Persistente</h4><p style='color:#00aaff;'>Rara</p><h3 style='color:#ffd700;'>🪙 1500</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.session_state.inv_sombra:
            if st.session_state.skin_activa == 'sombra': st.info(t('tie_equipada'))
            elif st.button(t('tie_equipar'), key="eq_som", use_container_width=True): st.session_state.skin_activa = 'sombra'; supabase.table("jugadores").update({"skin_activa": "sombra"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else:
            if st.button(t('tie_comprar'), key="cp_som", use_container_width=True):
                if st.session_state.monedas >= 1500: st.session_state.monedas -= 1500; st.session_state.inv_sombra = True; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "inv_sombra": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                else: st.error("Ahorra.")

    carta_fuego = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'fuego')
    with t4:
        st.markdown(f"<div style='background:#121212; border:1px solid #aa00ff; padding:15px; text-align:center; border-radius:8px;'>{carta_fuego}<h4 style='margin-top:10px;'>Fuego Fatuo</h4><p style='color:#aa00ff;'>Épica</p><h3 style='color:#ffd700;'>🪙 2500</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.session_state.inv_fuego:
            if st.session_state.skin_activa == 'fuego': st.info(t('tie_equipada'))
            elif st.button(t('tie_equipar'), key="eq_fue", use_container_width=True): st.session_state.skin_activa = 'fuego'; supabase.table("jugadores").update({"skin_activa": "fuego"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else:
            if st.button(t('tie_comprar'), key="cp_fue", use_container_width=True):
                if st.session_state.monedas >= 2500: st.session_state.monedas -= 2500; st.session_state.inv_fuego = True; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "inv_fuego": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                else: st.error("Ahorra.")

    if st.button(t('tie_quitar'), use_container_width=True):
        st.session_state.skin_activa = 'default'; supabase.table("jugadores").update({"skin_activa": "default"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()


   # --- EL MERCADO OCULTO (EASTER EGG) ---
    st.divider()
    st.markdown(f"<h3 style='text-align: center; color: #fff; margin-top: 30px; text-shadow: 0 0 15px #fff;'>{t('tie_oculto_tit')}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #888; font-size: 12px; margin-bottom: 20px;'>{t('tie_oculto_desc')}</p>", unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        codigo_secreto = st.text_input(t('tie_oculto_ph'), type="password", label_visibility="collapsed", placeholder=t('tie_oculto_ph'))
    with col_s2:
        if st.button(t('tie_oculto_btn'), use_container_width=True):
            if st.session_state.puntos_elo < 1000:
                st.error("Eres indigno. Vuelve cuando tengas 1000 ELO.")
            elif codigo_secreto.strip().upper() == "SUPREMO":
                supabase.table("jugadores").update({"skin_activa": "ascendido"}).eq("id", st.session_state.usuario_id).execute()
                st.session_state.skin_activa = "ascendido"
                st.balloons()
                st.success("HAS TRASCENDIDO. Skin 'Ascendido' equipada para siempre.")
                time.sleep(2)
                st.rerun()
            else:
                st.error("El código es incorrecto.")
                
    render_navbar("tienda")

# --- MISIONES SECUNDARIAS (GREMIO) ---
elif st.session_state.estado == "cuartel":
    idioma = st.session_state.get('idioma', 'es')
    c_txt = {
        "es": {
            "tit": "🛡️ CUARTEL GENERAL", "reg": "Registro de Guerra de", "emb_tit": "🤝 PROGRAMA DE EMBAJADORES", "emb_sub": "Tu Código de Reclutamiento:", "emb_desc": "Si un amigo usa tu nombre al registrarse, tú ganas 🪙 1000 y él 🪙 500.", "max": "RANGO MÁXIMO ALCANZADO", "sig": "ELO para el siguiente rango", "prog": "PROGRESO DE LIGA", "win": "Winrate", "tiem": "Tiempo Profundo", "tot": "Min. Totales", "rach": "Mejor Racha", "seg": "Seguidas", "herm": "👥 HERMANOS DE SANGRE", "ph": "Nombre exacto", "btn": "➕ AÑADIR", "err1": "No puedes añadirte a ti mismo.", "err2": "Guerrero no encontrado.", "ok": "¡Añadido a tus filas!", "solo": "Peleas solo. Añade a tus aliados."
        },
        "en": {
            "tit": "🛡️ HEADQUARTERS", "reg": "War Log of", "emb_tit": "🤝 AMBASSADOR PROGRAM", "emb_sub": "Your Referral Code:", "emb_desc": "If a friend uses your name to register, you earn 🪙 1000 and they earn 🪙 500.", "max": "MAXIMUM RANK REACHED", "sig": "ELO for next rank", "prog": "LEAGUE PROGRESS", "win": "Winrate", "tiem": "Deep Work Time", "tot": "Total Min.", "rach": "Best Streak", "seg": "In a row", "herm": "👥 BLOOD BROTHERS", "ph": "Exact name", "btn": "➕ ADD", "err1": "You can't add yourself.", "err2": "Warrior not found.", "ok": "Added to your ranks!", "solo": "You fight alone. Add your allies."
        }
    }
    c_t = c_txt.get(idioma, c_txt["es"])
    
    info_rango = get_rank_info(st.session_state.puntos_elo)
    rango_n, rango_s, rango_i, rango_c, elo_min, elo_max, rango_nivel = info_rango
    
    st.markdown(f"<h1 style='text-align: center; color: #fff; letter-spacing: 2px;'>{c_t['tit']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: {rango_c}; margin-bottom: 30px;'>{c_t['reg']} {st.session_state.nombre_guerra}</h4>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='background-color: #111; border: 1px dashed #ffd700; border-radius: 8px; padding: 20px; text-align: center; margin-bottom: 30px;'><h3 style='color: #ffd700; margin-top: 0;'>{c_t['emb_tit']}</h3><p style='color: #888; font-size: 14px;'>{c_t['emb_sub']}</p><h2 style='color: white; font-family: monospace; letter-spacing: 2px;'>{st.session_state.nombre_guerra}</h2><p style='color: #555; font-size: 12px; margin-bottom: 0;'>{c_t['emb_desc']}</p></div>".replace('\n', ''), unsafe_allow_html=True)

    if elo_min == elo_max: porcentaje_elo = 100; texto_progreso = f"{c_t['max']} ({st.session_state.puntos_elo} ELO)"
    else: puntos_conseguidos = st.session_state.puntos_elo - elo_min; puntos_rango = elo_max - elo_min; porcentaje_elo = int((puntos_conseguidos / puntos_rango) * 100); texto_progreso = f"{st.session_state.puntos_elo} / {elo_max} {c_t['sig']}"

    st.markdown(f"<div style='background-color: #111; border: 1px solid {rango_c}; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 30px;'><h3 style='color: white; margin-top: 0;'>{c_t['prog']}: {rango_i} {rango_n}</h3><div style='width: 100%; background-color: #333; border-radius: 10px; margin: 15px 0;'><div style='width: {porcentaje_elo}%; height: 20px; background: linear-gradient(90deg, #111, {rango_c}); border-radius: 10px; transition: width 0.5s ease;'></div></div><p style='color: #888; font-size: 14px; font-weight: bold; margin: 0;'>{texto_progreso} ({porcentaje_elo}%)</p></div>".replace('\n', ''), unsafe_allow_html=True)

    total_partidas = st.session_state.victorias + st.session_state.derrotas
    winrate = int((st.session_state.victorias / total_partidas) * 100) if total_partidas > 0 else 0
    horas_focus = round(st.session_state.minutos_focus / 60, 1)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div style='background-color: #161616; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center;'><p style='color: #888; font-size: 12px; margin: 0;'>{c_t['win']}</p><h2 style='color: #00ff00; margin: 5px 0;'>{winrate}%</h2><p style='color: #555; font-size: 10px; margin: 0;'>{st.session_state.victorias} V / {st.session_state.derrotas} D</p></div>".replace('\n', ''), unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='background-color: #161616; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center;'><p style='color: #888; font-size: 12px; margin: 0;'>{c_t['tiem']}</p><h2 style='color: #00aaff; margin: 5px 0;'>{horas_focus}h</h2><p style='color: #555; font-size: 10px; margin: 0;'>{st.session_state.minutos_focus} {c_t['tot']}</p></div>".replace('\n', ''), unsafe_allow_html=True)
    with c3: st.markdown(f"<div style='background-color: #161616; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center;'><p style='color: #888; font-size: 12px; margin: 0;'>{c_t['rach']}</p><h2 style='color: #ff4b4b; margin: 5px 0;'>🔥 {st.session_state.racha}</h2><p style='color: #555; font-size: 10px; margin: 0;'>{c_t['seg']}</p></div>".replace('\n', ''), unsafe_allow_html=True)

    st.markdown(f"<h3 style='text-align: center; color: #fff; margin-top: 40px;'>{c_t['herm']}</h3>", unsafe_allow_html=True)
    col_am_1, col_am_2 = st.columns([3, 1])
    with col_am_1: amigo_input = st.text_input("Añadir guerrero", placeholder=c_t['ph'], label_visibility="collapsed")
    with col_am_2:
        if st.button(c_t['btn'], use_container_width=True):
            if amigo_input.strip() == st.session_state.nombre_guerra: st.error(c_t['err1'])
            elif amigo_input:
                try:
                    comprobar = supabase.table("jugadores").select("id").eq("nombre", amigo_input.strip()).execute()
                    if len(comprobar.data) > 0:
                        supabase.table("amigos").insert({"jugador_id": st.session_state.usuario_id, "amigo_nombre": amigo_input.strip()}).execute()
                        st.success(c_t['ok']); time.sleep(1); st.rerun()
                    else: st.error(c_t['err2'])
                except Exception as e: st.error("Error base de datos.")
    
    try:
        mis_amigos = supabase.table("amigos").select("amigo_nombre").eq("jugador_id", st.session_state.usuario_id).execute()
        if len(mis_amigos.data) > 0:
            nombres_amigos = [a['amigo_nombre'] for a in mis_amigos.data]
            datos_amigos = supabase.table("jugadores").select("nombre, elo, skin_activa").in_("nombre", nombres_amigos).order("elo", desc=True).execute()
            if datos_amigos.data:
                cartas_amigos = "<div style='display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 15px;'>"
                for am in datos_amigos.data:
                    am_n, am_s, am_i, am_c = calcular_rango(am['elo'])
                    cartas_amigos += generar_carta_html(am['nombre'], am['elo'], am_i, am_c, "ALIADO", am.get('skin_activa', 'default'))
                cartas_amigos += "</div>"
                st.markdown(cartas_amigos.replace('\n', ''), unsafe_allow_html=True)
        else: st.markdown(f"<p style='text-align: center; color: #555; margin-top: 20px;'>{c_t['solo']}</p>", unsafe_allow_html=True)
    except Exception as e: st.markdown("<p style='text-align: center; color: #ff4b4b; margin-top: 20px;'>⚠️ Tabla de amigos no configurada aún.</p>", unsafe_allow_html=True)

    with st.expander(t("ajustes_titulo")):
        with st.form("form_ajustes"):
            nuevo_nombre = st.text_input(t("ajustes_nombre"), value=st.session_state.nombre_guerra)
            nueva_musica = st.selectbox(t("ajustes_musica"), list(CINTAS_AUDIO.keys()), index=list(CINTAS_AUDIO.keys()).index(st.session_state.get('musica_fondo', 'Lo-Fi (Concentración)')))
            nuevo_volumen = st.slider(t("ajustes_volumen"), min_value=0.0, max_value=1.0, value=float(st.session_state.get('volumen', 0.2)), step=0.1)
            
            idioma_actual = "English" if st.session_state.idioma == "en" else "Español"
            nuevo_idioma_key = st.selectbox(t("ajustes_idioma"), ["Español", "English"], index=["Español", "English"].index(idioma_actual))
            nuevo_idioma = "en" if nuevo_idioma_key == "English" else "es"
            
            if st.form_submit_button(t("ajustes_btn")):
                supabase.table("jugadores").update({
                    "nombre": nuevo_nombre,
                    "musica": nueva_musica,
                    "volumen": nuevo_volumen
                }).eq("id", st.session_state.usuario_id).execute()
                
                st.session_state.nombre_guerra = nuevo_nombre
                st.session_state.musica_fondo = nueva_musica
                st.session_state.volumen = nuevo_volumen
                st.session_state.idioma = nuevo_idioma
                
                st.success("✔ Base de datos actualizada / Database updated")
                time.sleep(1)
                st.rerun()
                
    render_navbar("cuartel")
elif st.session_state.estado == "cofre_animacion":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/foley/creaky_door_open.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#ffd700;'>FORZANDO LA CERRADURA...</h2>", unsafe_allow_html=True)
    st.markdown("<div class='chest-anim'>🧰</div>", unsafe_allow_html=True)
    if st.button("💥 REVELAR EL CONTENIDO 💥", type="primary", use_container_width=True):
        tirada = random.randint(1, 100); st.session_state.premio_duplicado = False
        if tirada <= 70: 
            st.session_state.premio_cofre = "sombra"
            if st.session_state.inv_sombra: st.session_state.premio_duplicado = True
            else: st.session_state.inv_sombra = True; supabase.table("jugadores").update({"inv_sombra": True}).eq("id", st.session_state.usuario_id).execute()
        elif tirada <= 90: 
            st.session_state.premio_cofre = "fuego"
            if st.session_state.inv_fuego: st.session_state.premio_duplicado = True
            else: st.session_state.inv_fuego = True; supabase.table("jugadores").update({"inv_fuego": True}).eq("id", st.session_state.usuario_id).execute()
        elif tirada <= 99: 
            st.session_state.premio_cofre = "aura"
            if st.session_state.inv_aura: st.session_state.premio_duplicado = True
            else: st.session_state.inv_aura = True; supabase.table("jugadores").update({"inventario_aura": True}).eq("id", st.session_state.usuario_id).execute()
        else: 
            st.session_state.premio_cofre = "corona"
            if st.session_state.inv_corona: st.session_state.premio_duplicado = True
            else: st.session_state.inv_corona = True; supabase.table("jugadores").update({"inventario_corona": True}).eq("id", st.session_state.usuario_id).execute()
        
        if st.session_state.premio_duplicado: st.session_state.monedas += 300; supabase.table("jugadores").update({"monedas": st.session_state.monedas}).eq("id", st.session_state.usuario_id).execute()
        st.session_state.estado = "cofre_resultado"; st.rerun()

elif st.session_state.estado == "cofre_resultado":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/foley/glass_shatter.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#fff;'>EL COFRE SE HA ABIERTO</h1>", unsafe_allow_html=True)
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    carta_premio = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "NUEVA SKIN", st.session_state.premio_cofre)
    if st.session_state.premio_cofre == "sombra": titulo_premio = "🟦 SOMBRA PERSISTENTE (RARO)"
    elif st.session_state.premio_cofre == "fuego": titulo_premio = "🟪 FUEGO FATUO (ÉPICO)"
    elif st.session_state.premio_cofre == "aura": titulo_premio = "🟥 AURA SANGUINARIA (MÍTICO)"
    else: titulo_premio = "🟨 CORONA DEL REY (LEGENDARIO) 🟨"

    st.markdown(f"<div style='text-align: center; margin: 30px 0;'>{carta_premio}<h2 style='margin-top: 20px;'>{titulo_premio}</h2></div>".replace('\n', ''), unsafe_allow_html=True)
    if st.session_state.premio_duplicado: st.warning("⚠️ Ya tenías esta skin. Recibes 300 Monedas a cambio.")
    else: st.success("¡Skin añadida a tu inventario!")
    if st.button("Volver a la Tienda", use_container_width=True): st.session_state.estado = "tienda"; st.rerun()

elif st.session_state.estado == "buscando" or st.session_state.estado == "buscando_privada":
    st.markdown("<audio autoplay loop src='https://actions.google.com/sounds/v1/alarms/beep_short.ogg'></audio>", unsafe_allow_html=True)
    tiempo_espera = time.time() - st.session_state.inicio_busqueda
    if st.session_state.estado == "buscando": st.markdown(f"<h2 style='text-align: center; color: #ff4b4b; animation: pulse 1.5s infinite;'>📡 Rastreando la red pública ({int(tiempo_espera)}s)...</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #ff4b4b;'>🤝 SALA DE SANGRE</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color: #111; border: 2px dashed #ff4b4b; padding: 20px; text-align: center; margin: 20px 0; border-radius: 10px;'><p style='color: #888; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px;'>Pásale este código a tu rival</p><h1 style='color: white; font-size: 60px; font-family: monospace; margin: 0; letter-spacing: 5px;'>{st.session_state.codigo_sala}</h1></div>".replace('\n', ''), unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #666;'>Esperando conexión... ({int(tiempo_espera)}s)</p>", unsafe_allow_html=True)
    
    if st.session_state.estado == "buscando" and tiempo_espera > 15:
        if st.session_state.partida_id: supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
        st.session_state.partida_id = None; st.session_state.rival_nombre = "EL GUARDIÁN"; st.session_state.rival_elo = st.session_state.puntos_elo + 15; st.session_state.rival_mision = "Quebrantar tu voluntad."; st.session_state.rival_skin = 'aura'; st.session_state.estado = "duelo"; st.rerun()
    
    texto_boton = "Cancelar Búsqueda" if st.session_state.estado == "buscando" else "Destruir Sala y Volver"
    if st.button(texto_boton, use_container_width=True):
        if st.session_state.partida_id: supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
        st.session_state.estado = "lobby"; st.rerun()

    if not st.session_state.partida_id:
        if st.session_state.estado == "buscando":
            rango_min = st.session_state.puntos_elo - 150; rango_max = st.session_state.puntos_elo + 150
            disponibles = supabase.table("partidas").select("*").eq("estado", "esperando").eq("tipo", "publica").eq("tiempo_batalla", st.session_state.tiempo_combate).neq("jugador1", st.session_state.usuario_id).gte("jugador1_elo", rango_min).lte("jugador1_elo", rango_max).execute()
        else: disponibles = supabase.table("partidas").select("*").eq("estado", "esperando").eq("tipo", "privada").eq("codigo_sala", st.session_state.codigo_sala).neq("jugador1", st.session_state.usuario_id).execute()
            
        if len(disponibles.data) > 0:
            sala = disponibles.data[0]; st.session_state.partida_id = sala['id']; ahora = datetime.now(timezone.utc).isoformat()
            supabase.table("partidas").update({"jugador2": st.session_state.usuario_id, "estado": "luchando", "ultima_actividad": ahora, "jugador2_mision": st.session_state.mision_actual}).eq("id", sala['id']).execute()
            rival_db = supabase.table("jugadores").select("nombre, elo, skin_activa").eq("id", sala['jugador1']).execute()
            if rival_db.data: st.session_state.rival_nombre = rival_db.data[0]['nombre']; st.session_state.rival_elo = rival_db.data[0]['elo']; st.session_state.rival_skin = rival_db.data[0].get('skin_activa', 'default')
            else: st.session_state.rival_nombre = "Anónimo"; st.session_state.rival_elo = 100; st.session_state.rival_skin = 'default'
            st.session_state.rival_mision = sala.get('jugador1_mision', "Sobrevivir"); st.session_state.estado = "duelo"; st.rerun()
        else:
            tipo_p = "publica" if st.session_state.estado == "buscando" else "privada"; cod_s = "" if st.session_state.estado == "buscando" else st.session_state.codigo_sala
            nueva = supabase.table("partidas").insert({"jugador1": st.session_state.usuario_id, "estado": "esperando", "tipo": tipo_p, "codigo_sala": cod_s, "jugador1_elo": st.session_state.puntos_elo, "tiempo_batalla": st.session_state.tiempo_combate, "jugador1_mision": st.session_state.mision_actual}).execute()
            st.session_state.partida_id = nueva.data[0]['id']; st.rerun()
    else:
        ahora = datetime.now(timezone.utc).isoformat(); supabase.table("partidas").update({"ultima_actividad": ahora}).eq("id", st.session_state.partida_id).execute()
        estado_sala = supabase.table("partidas").select("*").eq("id", st.session_state.partida_id).execute()
        if len(estado_sala.data) > 0 and estado_sala.data[0]['estado'] == 'luchando':
            sala = estado_sala.data[0]
            rival_db = supabase.table("jugadores").select("nombre, elo, skin_activa").eq("id", sala['jugador2']).execute()
            if rival_db.data: st.session_state.rival_nombre = rival_db.data[0]['nombre']; st.session_state.rival_elo = rival_db.data[0]['elo']; st.session_state.rival_skin = rival_db.data[0].get('skin_activa', 'default')
            else: st.session_state.rival_nombre = "Anónimo"; st.session_state.rival_elo = 100; st.session_state.rival_skin = 'default'
            st.session_state.rival_mision = sala.get('jugador2_mision', "Sobrevivir"); st.session_state.estado = "duelo"; st.rerun()
        else:
            with st.spinner("Rastreando..." if st.session_state.estado == "buscando" else "Vigilando la puerta..."): time.sleep(2); st.rerun()
elif st.session_state.estado == "duelo":
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; text-transform: uppercase; letter-spacing: 3px;'>🔥 DUELO A MUERTE 🔥</h1>", unsafe_allow_html=True)
    
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    _, _, riv_i, riv_c = calcular_rango(st.session_state.rival_elo)
    carta_tu = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "TÚ", st.session_state.skin_activa)
    carta_riv = generar_carta_html(st.session_state.rival_nombre, st.session_state.rival_elo, riv_i, riv_c, "ENEMIGO", st.session_state.get('rival_skin', 'default'))
    
    st.markdown(f"<div style='display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; margin-top: 20px;'>{carta_tu}<h1 style='color: #ff4b4b; font-size: 50px; font-style: italic;'>VS</h1>{carta_riv}</div>".replace('\n', ''), unsafe_allow_html=True)
    st.markdown(f"<div style='display: flex; justify-content: space-between; background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; margin-top: 15px;'><div style='text-align: left; width: 45%;'><p style='color: {tu_c}; margin: 0; font-weight: bold; font-size: 12px;'>TU OBJETIVO</p><p style='color: white; font-family: monospace; font-size: 14px; margin: 0;'>{st.session_state.mision_actual}</p></div><div style='border-left: 1px solid #333;'></div><div style='text-align: right; width: 45%;'><p style='color: {riv_c}; margin: 0; font-weight: bold; font-size: 12px;'>OBJETIVO ENEMIGO</p><p style='color: white; font-family: monospace; font-size: 14px; margin: 0;'>{st.session_state.rival_mision}</p></div></div>".replace('\n', ''), unsafe_allow_html=True)
    st.markdown("<div style='background-color: #0a0a0a; border: 2px solid #ff4b4b; border-radius: 15px; padding: 20px; margin: 30px 0; box-shadow: 0 0 30px rgba(255, 75, 75, 0.2);'><div id='reloj-container' style='text-align: center; font-size: 80px; font-family: monospace; font-weight: bold; color: white;'>--:--</div><div id='audio-container'></div></div>".replace('\n', ''), unsafe_allow_html=True)
    
    # MÓDULO DE RADIO PURO (Sin manipuladores de volumen)
    pista_actual = CINTAS_AUDIO.get(st.session_state.get('musica_fondo', 'Lo-Fi (Concentración)'), "")
    
    if pista_actual != "":
        st.markdown(f"""
            <div style='text-align: center; margin-bottom: 20px; padding: 10px; background-color: #111; border-radius: 8px; border: 1px solid #333;'>
                <p style='color: #00ff00; font-family: monospace; font-size: 12px; margin-bottom: 5px;'>📻 RADIO ACTIVADA: {st.session_state.musica_fondo}</p>
                <audio controls autoplay loop style='height: 40px; width: 100%; border-radius: 4px; outline: none;'>
                    <source src="{pista_actual}" type="audio/mpeg">
                </audio>
                <p style='color: #888; font-size: 10px; margin-top: 5px; margin-bottom: 0;'>* Si no suena al entrar, dale al botón de Play. Usa los botones de tu dispositivo para el volumen.</p>
            </div>
        """, unsafe_allow_html=True)

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
            "jugador_nombre": st.session_state.nombre_guerra,
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
            "jugador_nombre": st.session_state.nombre_guerra,
            "rival_nombre": st.session_state.rival_nombre, 
            "resultado": "victoria", 
            "puntos_cambio": st.session_state.elo_premio
        }).execute()
        
        if st.session_state.partida_id: 
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
            
        st.session_state.ultima_pildora = random.choice(pildoras)
        
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
            let wakeLock = null;

            // EL CENTINELA: Fuerza a la pantalla a quedarse encendida
            async function activarEscudoPantalla() {{
                try {{
                    wakeLock = await navigator.wakeLock.request('screen');
                }} catch (err) {{
                    console.log(`Escudo falló: ${{err.name}}, ${{err.message}}`);
                }}
            }}
            activarEscudoPantalla();
            
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
                    if(wakeLock !== null) wakeLock.release();
                    todosLosBotones.forEach(btn => {{ 
                        if(btn.innerText.includes('VICTORIA_SECRETA')) btn.click(); 
                    }}); 
                }}
            }}, 1000);
            
            // EL VERDUGO: Si cambian de app o bloquean el móvil manualmente, mueren.
            parentDoc.addEventListener('visibilitychange', function() {{ 
                if (parentDoc.visibilityState === 'hidden') {{ 
                    clearInterval(intervalo); 
                    if(wakeLock !== null) wakeLock.release();
                    todosLosBotones.forEach(btn => {{ 
                        if(btn.innerText.includes('ME RINDO')) btn.click(); 
                    }}); 
                }} else if (wakeLock !== null && parentDoc.visibilityState === 'visible') {{
                    activarEscudoPantalla();
                }}
            }});
        </script>
    """, height=0, width=0)
elif st.session_state.estado == "derrota":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #ff1a1a; font-size: 4em; text-transform: uppercase;'>💀 DERROTA</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #ff4b4b; font-size: 3em;'>-{st.session_state.elo_castigo} ELO</h2>", unsafe_allow_html=True)
    st.error(f"Tu escudo colapsó. Has fracasado en tu misión: *'{st.session_state.mision_actual}'*. **{st.session_state.rival_nombre}** se lleva la gloria.")
    st.write("")
    if st.button("Tragar el orgullo y volver", use_container_width=True): st.session_state.estado = "lobby"; st.rerun()

elif st.session_state.estado == "ascenso":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/crowds/crowd_cheering.ogg'></audio>", unsafe_allow_html=True)
    color = st.session_state.rango_alcanzado_color
    st.markdown(f"<div class='rank-up-box' style='background-color: #111; border: 4px solid {color}; border-radius: 20px; padding: 40px; text-align: center; margin: 40px 0; box-shadow: 0 0 50px {color};'><h1 style='color: white; font-size: 3em; margin: 0; text-transform: uppercase; letter-spacing: 2px;'>¡ASCENSO CONSEGUIDO!</h1><p style='color: #aaa; font-size: 1.2em; margin-top: 10px;'>Has roto tus límites y cruzado a la siguiente liga.</p><h1 style='color: {color}; font-size: 4em; margin: 20px 0; text-shadow: 0 0 20px {color};'>{st.session_state.rango_alcanzado_nombre}</h1></div>".replace('\n', ''), unsafe_allow_html=True)
    if st.button("ACEPTAR MI NUEVO PODER", type="primary", use_container_width=True): st.session_state.estado = "victoria"; st.rerun()
        
elif st.session_state.estado == "victoria":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/crowds/battle_crowd_cheer.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #00ff00; font-size: 4em; text-transform: uppercase; text-shadow: 0 0 20px rgba(0,255,0,0.4);'>🏆 VICTORIA</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #00ff00; font-size: 3em;'>+{st.session_state.elo_premio} ELO</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.4);'>🪙 +{st.session_state.monedas_ganadas_recientes} MONEDAS A LA BÓVEDA</h3>", unsafe_allow_html=True)
    st.success(f"Misión Cumplida: *'{st.session_state.mision_actual}'*. Tu disciplina ha destrozado a **{st.session_state.rival_nombre}**.")
    st.markdown(f"<div style='background-color: #1a1a1a; padding: 20px; border-left: 5px solid #00ff00; margin: 20px 0;'><p style='font-style: italic; font-size: 1.2em; color: #ddd;'>\"{st.session_state.ultima_pildora['texto']}\"</p><p style='text-align: right; color: #00ff00; font-weight: bold;'>— {st.session_state.ultima_pildora['autor']}</p></div>".replace('\n', ''), unsafe_allow_html=True)
    if st.button("Reclamar y Volver", use_container_width=True): st.session_state.estado = "lobby"; st.rerun()
