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
    </style>
""", unsafe_allow_html=True)

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

# --- MEMORIA ABSOLUTA ---
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
if 'boost_elo' not in st.session_state: st.session_state.boost_elo = None
if 'boost_monedas' not in st.session_state: st.session_state.boost_monedas = None
if 'rival_skin' not in st.session_state: st.session_state.rival_skin = 'default'

# NUEVA MEMORIA PARA SALAS PRIVADAS
if 'tipo_partida' not in st.session_state: st.session_state.tipo_partida = "publica"
if 'codigo_sala' not in st.session_state: st.session_state.codigo_sala = ""

pildoras = [
    {"autor": "Marco Aurelio", "texto": "Tienes poder sobre tu mente, no sobre los acontecimientos externos. Date cuenta de esto."},
    {"autor": "Naval Ravikant", "texto": "Si no puedes ver el lado positivo, estás mirando con los ojos del ego."},
    {"autor": "David Goggins", "texto": "El sufrimiento es la única forma de crecer. Domina tu mente."},
    {"autor": "Séneca", "texto": "No es que tengamos poco tiempo, sino que perdemos mucho."}
]

# --- MOTORES DE LÓGICA ---
def calcular_rango(elo):
    if elo < 200: return "Hierro III", "Esclavo", "🪨", "#7a7a7a"
    elif elo < 300: return "Hierro II", "Distraído", "⛓️", "#8f8f8f"
    elif elo < 400: return "Hierro I", "Despertando", "⚙️", "#a3a3a3"
    elif elo < 600: return "Bronce", "Guerrero", "🥉", "#cd7f32"
    elif elo < 800: return "Plata", "Dueño del Tiempo", "🥈", "#c0c0c0"
    elif elo < 1000: return "Oro", "Élite", "🥇", "#ffd700"
    else: return "Diamante", "Intocable", "💎", "#00ffff"

def tiene_boost_activo(fecha_str):
    if not fecha_str: return False
    try:
        fecha_fin = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
        return datetime.now(timezone.utc) < fecha_fin
    except: 
        return False

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
    
    if segundos == 10: 
        p_elo, c_elo, coins = 5, 5, 1 
    elif segundos == 1500: 
        p_elo, c_elo, coins = 25, 20, base_monedas * 1 
    elif segundos == 3000: 
        p_elo, c_elo, coins = 55, 40, int(base_monedas * 2.5) 
    elif segundos == 5400: 
        p_elo, c_elo, coins = 100, 80, base_monedas * 5 
    else: 
        p_elo, c_elo, coins = 25, 25, base_monedas

    if tiene_boost_activo(boost_elo_str): p_elo *= 2
    if tiene_boost_activo(boost_monedas_str): coins *= 2
        
    return p_elo, c_elo, coins

def generar_carta_html(nombre, elo, rango_i, rango_c, subtitulo, skin='default'):
    display_name = f"👑 {nombre}" if skin == 'corona' else nombre
    color_borde = "#ff0000" if skin == 'aura' else rango_c
    clase_animacion = "anim-aura" if skin == 'aura' else "anim-float"
    efecto_sombra = "" if skin == 'aura' else f"box-shadow: 0 0 20px {color_borde}30;"

    return f"""
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

def render_navbar(origen):
    st.markdown("<hr style='border: 1px solid #333; margin-top: 40px;'>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([1, 0.05, 1, 0.05, 1])
    
    with c1:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🏠 LOBBY", use_container_width=True, key=f"nav_lobby_{origen}"): 
            st.session_state.estado = "lobby"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c2: 
        st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>", unsafe_allow_html=True)
        
    with c3:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🛒 TIENDA", use_container_width=True, key=f"nav_tienda_{origen}"): 
            st.session_state.estado = "tienda"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c4: 
        st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>", unsafe_allow_html=True)
        
    with c5:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🏛️ LEYENDAS", use_container_width=True, key=f"nav_salon_{origen}"): 
            st.session_state.estado = "salon"
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
    """, unsafe_allow_html=True)
    
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
                    st.session_state.boost_elo = d.get('boost_elo_hasta')
                    st.session_state.boost_monedas = d.get('boost_monedas_hasta')
                else:
                    supabase.table("jugadores").insert({
                        "id": user_id, 
                        "elo": 100, 
                        "racha": 0, 
                        "monedas": 0, 
                        "nombre": "Guerrero"
                    }).execute()
                    st.session_state.puntos_elo = 100
                    st.session_state.racha = 0
                    st.session_state.monedas = 0
                    st.session_state.nombre_guerra = "Guerrero"
                
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
                    supabase.table("jugadores").insert({
                        "id": auth_resp.user.id, 
                        "elo": 100, 
                        "racha": 0, 
                        "monedas": 0, 
                        "nombre": nombre_reg
                    }).execute()
                    st.success("¡Tu nombre está grabado en la piedra! Pasa a la pestaña de 'Entrar'.")
                except Exception as e:
                    st.error(f"Fallo en el registro: {str(e)}")

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
        
    st.markdown(f"<h3 style='text-align: center; color: white; text-transform: uppercase;'>Bienvenido, {st.session_state.nombre_guerra} <br><div style='margin-top:10px;'>{boosts_html}</div></h3>", unsafe_allow_html=True)
    
    with st.expander("⚙️ Ajustes de Perfil"):
        nuevo_nombre = st.text_input("Cambiar nombre de guerra", value=st.session_state.nombre_guerra)
        if st.button("ACTUALIZAR NOMBRE"):
            supabase.table("jugadores").update({"nombre": nuevo_nombre}).eq("id", st.session_state.usuario_id).execute()
            st.session_state.nombre_guerra = nuevo_nombre
            st.success("¡Nombre actualizado!")
            time.sleep(1)
            st.rerun()

    st.divider()
    
    carta_propia = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, rango_i, rango_c, "TU LEYENDA", st.session_state.skin_activa)
    st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'>{carta_propia}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around; text-align: center; background-color: #121212; padding: 25px; border-radius: 12px; border: 1px solid {rango_c}; box-shadow: 0 4px 20px {rango_c}40;'>
            <div>
                <p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;'>Tu Rango</p>
                <h2 style='margin: 0; color: {rango_c}; text-shadow: 0 0 10px {rango_c}80;'>{rango_i} {rango_n}</h2>
            </div>
            <div style='border-left: 1px solid #333; border-right: 1px solid #333; padding: 0 20px;'>
                <p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;'>ELO</p>
                <h2 style='margin: 0; color: white;'>{st.session_state.puntos_elo} pts</h2>
            </div>
            <div>
                <p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;'>Bóveda</p>
                <h2 style='margin: 0; color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.3);'>🪙 {st.session_state.monedas}</h2>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") 
    
    with st.expander("🌍 Ranking Mundial (Top 5)", expanded=True):
        ranking = supabase.table("jugadores").select("elo, nombre, skin_activa").order("elo", desc=True).limit(5).execute()
        if ranking.data:
            cartas_html = "<div style='display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; padding: 10px 0;'>"
            for i, jugador in enumerate(ranking.data):
                _, _, i_rank, c_rank = calcular_rango(jugador['elo'])
                cartas_html += generar_carta_html(jugador['nombre'], jugador['elo'], i_rank, c_rank, f"TOP {i+1}", jugador.get('skin_activa', 'default'))
            cartas_html += "</div>"
            st.markdown(cartas_html, unsafe_allow_html=True)

    with st.expander("📜 Historial de Guerra"):
        historial = supabase.table("historial").select("*").eq("jugador_id", st.session_state.usuario_id).order("fecha", desc=True).limit(5).execute()
        if historial.data:
            for batalla in historial.data:
                if batalla['resultado'] == "victoria":
                    color = "🟢"
                    signo = "+"
                else:
                    color = "🔴"
                    signo = ""
                st.markdown(f"{color} vs **{batalla['rival_nombre']}** ({signo}{batalla['puntos_cambio']} ELO)")
        else:
            st.write("Aún no has derramado sangre en la Arena.")
            
    st.divider()
    
    st.markdown("""
        <div class="rules-box">
            <h3 style="text-align: center; color: #ff4b4b; text-transform: uppercase; margin-top: 0; text-shadow: 0 0 10px rgba(255, 75, 75, 0.5);">⚠️ Las Leyes de la Arena</h3>
            <ul style="list-style-type: none; padding-left: 0; color: #ccc; font-size: 15px; line-height: 1.8;">
                <li style="margin-bottom: 10px;">🟢 <span class="neon-green">CÓMO GANAR:</span> Escribe tu misión y sobrevive hasta que el reloj llegue a cero sin salir de la aplicación.</li>
                <li style="margin-bottom: 10px;">🔴 <span class="neon-red">CÓMO PERDER:</span> Si cambias de pestaña o pulsas "Me Rindo", tu C4 explota. Pierdes tu ELO.</li>
                <li>⚔️ <strong style="color: #ffd700;">EL PACTO:</strong> Cumple la misión declarada. Si no trabajas, estarás engañando al sistema.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #ff4b4b;'>🔥 DECLARACIÓN DE INTENCIONES</h3>", unsafe_allow_html=True)
    mision_input = st.text_input("", placeholder="Ej: Terminar el ensayo de Filosofía...", label_visibility="collapsed")
    
    tiempo_opts = {
        "⚙️ Modo Test (10 Segundos | Riesgo: 5 ELO)": 10,
        "⚔️ Escaramuza (25 Minutos | Riesgo: 20 ELO)": 1500,
        "🔥 Asalto Profundo (50 Minutos | Riesgo: 40 ELO)": 3000,
        "💀 Modo Titán (90 Minutos | Riesgo: 80 ELO)": 5400
    }
    tiempo_str = st.selectbox("Duración de la batalla:", list(tiempo_opts.keys()))
    
    # --- SISTEMA DE EMPAREJAMIENTO (PÚBLICO Y PRIVADO) ---
    c_pub, c_priv = st.columns(2)
    
    with c_pub:
        if st.button("🌍 BÚSQUEDA MUNDIAL", use_container_width=True, type="primary"):
            if not mision_input:
                st.error("Un guerrero no entra sin propósito. Declara tu misión.")
            else:
                limite_fantasmas = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
                supabase.table("partidas").delete().eq("estado", "esperando").lt("ultima_actividad", limite_fantasmas).execute()
                
                st.session_state.mision_actual = mision_input
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
        codigo_input = st.text_input("", placeholder="Pega el código de un amigo o déjalo vacío para crear", label_visibility="collapsed", key="input_cod_priv")
    with c_p2:
        if st.button("🚪 CREAR / UNIRSE", use_container_width=True):
            if not mision_input:
                st.error("Declara tu misión primero.")
            else:
                st.session_state.mision_actual = mision_input
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

# --- LA TIENDA ---
elif st.session_state.estado == "tienda":
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    
    st.markdown("<h1 style='text-align: center; color: #ffd700; letter-spacing: 2px;'>🛒 EL MERCADO NEGRO</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Viste tu leyenda. Intimida al enemigo.</h4>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background-color: #1a1a1a; border: 1px solid #ffd700; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 30px;'>
            <p style='margin:0; color:#aaa; font-size:14px; text-transform:uppercase;'>Fondos Disponibles</p>
            <h2 style='margin:0; color:#ffd700; font-size:36px; text-shadow: 0 0 15px rgba(255,215,0,0.4);'>🪙 {st.session_state.monedas}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧬 BOOSTS DE RENDIMIENTO (24 Horas)")
    
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("""
            <div style='background:#121212; border:1px solid #333; padding:15px; text-align:center; border-radius:8px;'>
                <h3>⚡ x2 ELO</h3>
                <p style='color:#888; font-size:12px;'>Multiplica tus ganancias de rango.</p>
                <h3 style='color:#ffd700;'>🪙 150</h3>
            </div>
        """, unsafe_allow_html=True)
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
        """, unsafe_allow_html=True)
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

    st.markdown("### 🔥 SKINS DE ARENA")
    
    t1, t2 = st.columns(2)
    
    carta_aura = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'aura')
    with t1:
        st.markdown(f"""
            <div style='background:#121212; border:1px solid #ff4b4b; padding:15px; text-align:center; border-radius:8px;'>
                {carta_aura}
                <h4 style='margin-top:10px;'>Aura Sanguinaria</h4>
                <p style='color:#888; font-size:12px;'>Tu carta arderá en rojo perpetuo.</p>
                <h3 style='color:#ffd700;'>🪙 500</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.inv_aura:
            if st.session_state.skin_activa == 'aura':
                st.info("EQUIPADA")
            elif st.button("EQUIPAR AURA", use_container_width=True): 
                st.session_state.skin_activa = 'aura'
                supabase.table("jugadores").update({"skin_activa": "aura"}).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else:
            if st.button("COMPRAR AURA", use_container_width=True):
                if st.session_state.monedas >= 500:
                    st.session_state.monedas -= 500
                    st.session_state.inv_aura = True
                    supabase.table("jugadores").update({
                        "monedas": st.session_state.monedas, 
                        "inventario_aura": True
                    }).eq("id", st.session_state.usuario_id).execute()
                    st.success("Desbloqueada")
                    st.rerun()
                else:
                    st.error("Necesitas más oro y victorias.")
                
    carta_corona = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'corona')
    with t2:
        st.markdown(f"""
            <div style='background:#121212; border:1px solid #ffd700; padding:15px; text-align:center; border-radius:8px;'>
                {carta_corona}
                <h4 style='margin-top:10px;'>Corona del Rey</h4>
                <p style='color:#888; font-size:12px;'>Icono permanente en tu nombre.</p>
                <h3 style='color:#ffd700;'>🪙 1500</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.inv_corona:
            if st.session_state.skin_activa == 'corona':
                st.info("EQUIPADA")
            elif st.button("EQUIPAR CORONA", use_container_width=True): 
                st.session_state.skin_activa = 'corona'
                supabase.table("jugadores").update({"skin_activa": "corona"}).eq("id", st.session_state.usuario_id).execute()
                st.rerun()
        else:
            if st.button("COMPRAR CORONA", use_container_width=True):
                if st.session_state.monedas >= 1500:
                    st.session_state.monedas -= 1500
                    st.session_state.inv_corona = True
                    supabase.table("jugadores").update({
                        "monedas": st.session_state.monedas, 
                        "inventario_corona": True
                    }).eq("id", st.session_state.usuario_id).execute()
                    st.success("El Rey ha sido coronado.")
                    st.rerun()
                else:
                    st.error("No eres digno aún.")
                
    if st.button("✖ QUITAR SKIN ACTUAL", use_container_width=True):
        st.session_state.skin_activa = 'default'
        supabase.table("jugadores").update({"skin_activa": "default"}).eq("id", st.session_state.usuario_id).execute()
        st.rerun()
    
    render_navbar("tienda")

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
            <p style='color: #888; font-size: 14px;'>Al llegar a cero, el ELO de todos los guerreros se reseteará. Solo los 3 mejores serán grabados en la piedra eterna.</p>
            <h1 style='color: white; font-family: monospace; font-size: 45px; margin: 10px 0; text-shadow: 0 0 10px rgba(255,255,255,0.3);'>
                {dias}D : {horas}H
            </h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #fff;'>🏆 ASPIRANTES A LEYENDA (TOP 3 ACTUAL)</h3>", unsafe_allow_html=True)
    
    ranking = supabase.table("jugadores").select("elo, nombre, skin_activa").order("elo", desc=True).limit(3).execute()
    if ranking.data:
        cartas_html = "<div style='display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; padding: 10px 0;'>"
        for i, jugador in enumerate(ranking.data):
            _, _, i_rank, c_rank = calcular_rango(jugador['elo'])
            cartas_html += generar_carta_html(jugador['nombre'], jugador['elo'], i_rank, c_rank, f"ASPIRANTE #{i+1}", jugador.get('skin_activa', 'default'))
        cartas_html += "</div>"
        st.markdown(cartas_html, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #ffd700; margin-top: 40px;'>📜 LEYENDAS INMORTALES</h3>", unsafe_allow_html=True)
    
    leyendas = supabase.table("leyendas").select("*").order("temporada", desc=True).execute()
    if leyendas.data:
        for l in leyendas.data:
            st.markdown(f"""
                <div style='background:#1a1a1a; border-left:4px solid {l['rango_color']}; padding:15px; margin-bottom:10px;'>
                    <h4 style='margin:0; color:white;'>Temporada {l['temporada']}: {l['nombre']}</h4>
                    <p style='margin:0; color:#888;'>{l['rango_icono']} {l['rango_nombre']} - {l['elo_final']} ELO Final</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='text-align:center; padding:30px; border:1px dashed #333;'>
                <p style='color:#555; font-style:italic;'>Aún no ha terminado ninguna temporada. El pedestal está vacío.</p>
            </div>
        """, unsafe_allow_html=True)

    render_navbar("salon")

# --- EMPAREJAMIENTO MULTIJUGADOR (PÚBLICO) ---
elif st.session_state.estado == "buscando":
    
    st.markdown("<audio autoplay loop src='https://actions.google.com/sounds/v1/alarms/beep_short.ogg'></audio>", unsafe_allow_html=True)
    
    tiempo_espera = time.time() - st.session_state.inicio_busqueda
    st.markdown(f"<h2 style='text-align: center; color: #ff4b4b; animation: pulse 1.5s infinite;'>📡 Rastreando la red pública ({int(tiempo_espera)}s)...</h2>", unsafe_allow_html=True)
    
    if tiempo_espera > 15:
        if st.session_state.partida_id:
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
            st.session_state.partida_id = None
            
        st.session_state.rival_nombre = "EL GUARDIÁN"
        st.session_state.rival_elo = st.session_state.puntos_elo + 15
        st.session_state.rival_mision = "Quebrantar tu voluntad."
        st.session_state.rival_skin = 'aura' 
        
        st.session_state.estado = "duelo"
        st.rerun()
    
    if st.button("Cancelar Búsqueda", use_container_width=True):
        if st.session_state.partida_id:
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
        st.session_state.estado = "lobby"
        st.rerun()

    if not st.session_state.partida_id:
        rango_min = st.session_state.puntos_elo - 150
        rango_max = st.session_state.puntos_elo + 150
        
        disponibles = supabase.table("partidas").select("*").eq("estado", "esperando").eq("tipo", "publica").eq("tiempo_batalla", st.session_state.tiempo_combate).neq("jugador1", st.session_state.usuario_id).gte("jugador1_elo", rango_min).lte("jugador1_elo", rango_max).execute()
        
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
            nueva = supabase.table("partidas").insert({
                "jugador1": st.session_state.usuario_id, 
                "estado": "esperando",
                "tipo": "publica",
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
            with st.spinner("Rastreando..."):
                time.sleep(2)
                st.rerun()

# --- EMPAREJAMIENTO MULTIJUGADOR (PRIVADO) ---
elif st.session_state.estado == "buscando_privada":
    st.markdown("<audio autoplay loop src='https://actions.google.com/sounds/v1/alarms/beep_short.ogg'></audio>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #ff4b4b;'>🤝 SALA DE SANGRE</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background-color: #111; border: 2px dashed #ff4b4b; padding: 20px; text-align: center; margin: 20px 0; border-radius: 10px;'>
            <p style='color: #888; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px;'>Pásale este código a tu rival</p>
            <h1 style='color: white; font-size: 60px; font-family: monospace; margin: 0; letter-spacing: 5px; text-shadow: 0 0 15px rgba(255,255,255,0.4);'>{st.session_state.codigo_sala}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    tiempo_espera = time.time() - st.session_state.inicio_busqueda
    st.markdown(f"<p style='text-align: center; color: #666;'>Esperando conexión... ({int(tiempo_espera)}s)</p>", unsafe_allow_html=True)
    
    if st.button("Destruir Sala y Volver", use_container_width=True):
        if st.session_state.partida_id:
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
        st.session_state.estado = "lobby"
        st.rerun()

    if not st.session_state.partida_id:
        sala_existente = supabase.table("partidas").select("*").eq("estado", "esperando").eq("tipo", "privada").eq("codigo_sala", st.session_state.codigo_sala).neq("jugador1", st.session_state.usuario_id).execute()
        
        if len(sala_existente.data) > 0:
            sala = sala_existente.data[0]
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
                
            st.session_state.rival_mision = sala.get('jugador1_mision', "Sobrevivir")
            st.session_state.estado = "duelo"
            st.rerun()
        else:
            nueva = supabase.table("partidas").insert({
                "jugador1": st.session_state.usuario_id, 
                "estado": "esperando",
                "tipo": "privada",
                "codigo_sala": st.session_state.codigo_sala,
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
                
            st.session_state.rival_mision = sala.get('jugador2_mision', "Sobrevivir")
            st.session_state.estado = "duelo"
            st.rerun()
        else:
            with st.spinner("Vigilando la puerta..."):
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
    """, unsafe_allow_html=True)
    
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
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #0a0a0a; border: 2px solid #ff4b4b; border-radius: 15px; padding: 20px; margin: 30px 0; box-shadow: 0 0 30px rgba(255, 75, 75, 0.2);'>
            <div id='reloj-container' style='text-align: center; font-size: 80px; font-family: monospace; font-weight: bold; color: white;'>--:--</div>
            <div id='audio-container'></div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("💀 ME RINDO (Tocar el móvil)", type="primary", use_container_width=True):
        st.session_state.puntos_elo = max(0, st.session_state.puntos_elo - st.session_state.elo_castigo)
        st.session_state.racha = 0
        
        supabase.table("jugadores").update({
            "elo": st.session_state.puntos_elo, 
            "racha": st.session_state.racha
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
        st.session_state.puntos_elo += st.session_state.elo_premio
        st.session_state.racha += 1
        st.session_state.monedas += st.session_state.monedas_ganadas_recientes
        
        supabase.table("jugadores").update({
            "elo": st.session_state.puntos_elo, 
            "racha": st.session_state.racha,
            "monedas": st.session_state.monedas
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
    """, unsafe_allow_html=True)
    
    if st.button("Reclamar y Volver", use_container_width=True): 
        st.session_state.estado = "lobby"
        st.rerun()
