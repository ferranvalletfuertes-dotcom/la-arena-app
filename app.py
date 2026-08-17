import streamlit as st
import time
import random
from datetime import datetime, timedelta, timezone
import streamlit.components.v1 as components
from supabase import create_client, Client

st.set_page_config(page_title="Modo Combate | La Arena", layout="centered")

# --- INYECCIÓN DE CSS (ARMADURA VISUAL Y ÉPICA) ---
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
    
    .fut-card:hover {
        transform: translateY(-5px);
        filter: brightness(1.2);
    }
    
    .stTextInput > div > div > input {
        background-color: #111 !important;
        color: #00ff00 !important;
        border: 1px solid #333 !important;
        font-family: monospace;
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

# --- MEMORIA DEL JUGADOR ---
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

pildoras = [
    {"autor": "Marco Aurelio", "texto": "Tienes poder sobre tu mente, no sobre los acontecimientos externos. Date cuenta de esto."},
    {"autor": "Naval Ravikant", "texto": "Si no puedes ver el lado positivo, estás mirando con los ojos del ego."},
    {"autor": "David Goggins", "texto": "El sufrimiento es la única forma de crecer. Domina tu mente."},
    {"autor": "Séneca", "texto": "No es que tengamos poco tiempo, sino que perdemos mucho."}
]

def calcular_rango(elo):
    if elo < 200: return "Hierro III", "Esclavo", "🪨", "#7a7a7a"
    elif elo < 300: return "Hierro II", "Distraído", "⛓️", "#8f8f8f"
    elif elo < 400: return "Hierro I", "Despertando", "⚙️", "#a3a3a3"
    elif elo < 600: return "Bronce", "Guerrero", "🥉", "#cd7f32"
    elif elo < 800: return "Plata", "Dueño del Tiempo", "🥈", "#c0c0c0"
    elif elo < 1000: return "Oro", "Élite", "🥇", "#ffd700"
    else: return "Diamante", "Intocable", "💎", "#00ffff"

def calcular_monedas_base(elo):
    if elo < 200: return 10
    elif elo < 300: return 15
    elif elo < 400: return 20
    elif elo < 600: return 35
    elif elo < 800: return 50
    elif elo < 1000: return 75
    else: return 120

def calcular_riesgo_recompensa(segundos, elo_actual):
    base_monedas = calcular_monedas_base(elo_actual)
    if segundos == 10: return 5, 5, 1 
    elif segundos == 1500: return 25, 20, base_monedas * 1 
    elif segundos == 3000: return 55, 40, int(base_monedas * 2.5) 
    elif segundos == 5400: return 100, 80, base_monedas * 5 
    return 25, 25, base_monedas

def generar_carta_html(nombre, elo, rango_i, rango_c, subtitulo):
    return f"""<div class="fut-card" style="background: linear-gradient(135deg, #161616 0%, #050505 100%); border: 2px solid {rango_c}; border-radius: 12px; width: 140px; margin: 10px; padding: 15px 10px; position: relative; box-shadow: 0 0 20px {rango_c}30; display: inline-block; text-align: center; transition: all 0.3s ease;">
<div style="position: absolute; top: 8px; left: 12px; color: {rango_c}; font-weight: 900; font-size: 20px; font-family: monospace; text-shadow: 0 0 5px {rango_c};">{elo}</div>
<div style="position: absolute; top: 8px; right: 12px; font-size: 20px; filter: drop-shadow(0 0 5px {rango_c});">{rango_i}</div>
<div style="margin-top: 35px; margin-bottom: 10px;">
<svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="{rango_c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.9; filter: drop-shadow(0 0 8px {rango_c});"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
</div>
<h4 style="color: white; margin: 0; font-size: 14px; text-transform: uppercase; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: 1px;">{nombre}</h4>
<div style="color: #666; font-size: 11px; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px; font-weight: bold;">{subtitulo}</div>
</div>"""

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
                    st.session_state.puntos_elo = datos.data[0]['elo']
                    st.session_state.racha = datos.data[0]['racha']
                    st.session_state.monedas = datos.data[0].get('monedas') or 0
                    st.session_state.nombre_guerra = datos.data[0].get('nombre') or "Guerrero"
                else:
                    supabase.table("jugadores").insert({"id": user_id, "elo": 100, "racha": 0, "monedas": 0, "nombre": "Guerrero"}).execute()
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
                    supabase.table("jugadores").insert({"id": auth_resp.user.id, "elo": 100, "racha": 0, "monedas": 0, "nombre": nombre_reg}).execute()
                    st.success("¡Tu nombre está grabado en la piedra! Pasa a la pestaña de 'Entrar'.")
                except Exception as e:
                    st.error(f"Fallo en el registro: {str(e)}")

# --- EL LOBBY ---
elif st.session_state.estado == "lobby":
    st.session_state.partida_id = None 
    st.session_state.rival_nombre = "Desconocido"
    rango_n, rango_s, rango_i, rango_c = calcular_rango(st.session_state.puntos_elo)
    
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; letter-spacing: 2px;'>⚔️ MODO COMBATE</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: white; text-transform: uppercase;'>Bienvenido, {st.session_state.nombre_guerra}</h3>", unsafe_allow_html=True)
    
    with st.expander("⚙️ Ajustes de Perfil"):
        nuevo_nombre = st.text_input("Cambiar nombre de guerra", value=st.session_state.nombre_guerra)
        if st.button("ACTUALIZAR NOMBRE"):
            supabase.table("jugadores").update({"nombre": nuevo_nombre}).eq("id", st.session_state.usuario_id).execute()
            st.session_state.nombre_guerra = nuevo_nombre
            st.success("¡Nombre actualizado!")
            time.sleep(1); st.rerun()

    st.divider()
    
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
    
    with st.expander("🌍 Salón de la Élite (Top 5)", expanded=True):
        ranking = supabase.table("jugadores").select("elo, nombre").order("elo", desc=True).limit(5).execute()
        if ranking.data:
            cartas_html = "<div style='display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; padding: 10px 0;'>"
            for i, jugador in enumerate(ranking.data):
                _, _, i_rank, c_rank = calcular_rango(jugador['elo'])
                cartas_html += generar_carta_html(jugador['nombre'], jugador['elo'], i_rank, c_rank, f"TOP {i+1}")
            cartas_html += "</div>"
            st.markdown(cartas_html, unsafe_allow_html=True)

    with st.expander("📜 Historial de Guerra"):
        historial = supabase.table("historial").select("*").eq("jugador_id", st.session_state.usuario_id).order("fecha", desc=True).limit(5).execute()
        if historial.data:
            for batalla in historial.data:
                color = "🟢" if batalla['resultado'] == "victoria" else "🔴"
                signo = "+" if batalla['resultado'] == "victoria" else ""
                st.markdown(f"{color} vs **{batalla['rival_nombre']}** ({signo}{batalla['puntos_cambio']} ELO)")
        else:
            st.write("Aún no has derramado sangre en la Arena.")
            
    st.divider()

    st.markdown("""
        <div class="rules-box">
            <h3 style="text-align: center; color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; margin-top: 0; text-shadow: 0 0 10px rgba(255, 75, 75, 0.5);">⚠️ Las Leyes de la Arena</h3>
            <ul style="list-style-type: none; padding-left: 0; color: #ccc; font-size: 15px; line-height: 1.8;">
                <li style="margin-bottom: 10px;">🟢 <span class="neon-green">CÓMO GANAR:</span> Escribe tu misión. Sobrevive hasta que el reloj llegue a cero sin salir de la aplicación.</li>
                <li style="margin-bottom: 10px;">🔴 <span class="neon-red">CÓMO PERDER:</span> Si cambias de pestaña, minimizas el navegador o pulsas "Me Rindo", tu C4 explota. Pierdes tu ELO.</li>
                <li>⚔️ <strong style="color: #ffd700;">EL PACTO:</strong> Cumple la misión declarada. Si no trabajas, estarás engañando al sistema, pero nunca a ti mismo.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #ff4b4b;'>🔥 DECLARACIÓN DE INTENCIONES</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 14px;'>Tu rival sabrá por qué estás luchando. No le decepciones.</p>", unsafe_allow_html=True)
    
    mision_input = st.text_input("", placeholder="Ej: Terminar el ensayo de Filosofía...", label_visibility="collapsed")
    
    tiempo_opts = {
        "⚙️ Modo Test (10 Segundos | Riesgo: 5 ELO)": 10,
        "⚔️ Escaramuza (25 Minutos | Riesgo: 20 ELO)": 1500,
        "🔥 Asalto Profundo (50 Minutos | Riesgo: 40 ELO)": 3000,
        "💀 Modo Titán (90 Minutos | Riesgo: 80 ELO)": 5400
    }
    tiempo_str = st.selectbox("Duración de la batalla:", list(tiempo_opts.keys()))
    
    if st.button("🔥 BUSCAR RIVAL", use_container_width=True, type="primary"):
        if not mision_input:
            st.error("Un guerrero no entra a la Arena sin un propósito. Declara tu misión.")
        else:
            limite_fantasmas = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
            supabase.table("partidas").delete().eq("estado", "esperando").lt("ultima_actividad", limite_fantasmas).execute()
            
            st.session_state.mision_actual = mision_input
            st.session_state.tiempo_combate = tiempo_opts[tiempo_str]
            win_elo, lose_elo, coins = calcular_riesgo_recompensa(st.session_state.tiempo_combate, st.session_state.puntos_elo)
            st.session_state.elo_premio = win_elo
            st.session_state.elo_castigo = lose_elo
            st.session_state.monedas_ganadas_recientes = coins
            
            st.session_state.inicio_busqueda = time.time()
            st.session_state.estado = "buscando"
            st.rerun()

    st.markdown("<hr style='border: 1px solid #333; margin-top: 30px;'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 0.1, 1])
    with c1:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🏠 LOBBY", use_container_width=True): pass 
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🛒 TIENDA", use_container_width=True): 
            st.session_state.estado = "tienda"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# --- LA TIENDA ---
elif st.session_state.estado == "tienda":
    st.markdown("<h1 style='text-align: center; color: #ffd700; letter-spacing: 2px;'>🛒 EL MERCADO NEGRO</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Viste tu leyenda. Intimida al enemigo.</h4>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background-color: #1a1a1a; border: 1px solid #ffd700; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 30px;'>
            <p style='margin:0; color:#aaa; font-size:14px; text-transform:uppercase;'>Fondos Disponibles</p>
            <h2 style='margin:0; color:#ffd700; font-size:36px; text-shadow: 0 0 15px rgba(255,215,0,0.4);'>🪙 {st.session_state.monedas}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔥 SKINS DE ARENA (Próximamente)")
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("""
        <div style='background-color: #121212; border: 1px solid #333; padding: 20px; text-align: center; border-radius: 8px;'>
            <h1 style='margin:0;'>🩸</h1>
            <h4 style='color: white;'>Aura Sanguinaria</h4>
            <h3 style='color: #ffd700;'>🪙 500</h3>
            <button disabled style='width:100%; padding:10px; background:#333; color:#777; border:none; border-radius:5px;'>BLOQUEADO</button>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div style='background-color: #121212; border: 1px solid #333; padding: 20px; text-align: center; border-radius: 8px;'>
            <h1 style='margin:0;'>👑</h1>
            <h4 style='color: white;'>Corona del Rey</h4>
            <h3 style='color: #ffd700;'>🪙 1500</h3>
            <button disabled style='width:100%; padding:10px; background:#333; color:#777; border:none; border-radius:5px;'>BLOQUEADO</button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid #333; margin-top: 40px;'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 0.1, 1])
    with c1:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🏠 LOBBY", use_container_width=True): 
            st.session_state.estado = "lobby"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
        if st.button("🛒 TIENDA", use_container_width=True): pass
        st.markdown("</div>", unsafe_allow_html=True)


# --- EMPAREJAMIENTO MULTIJUGADOR ---
elif st.session_state.estado == "buscando":
    tiempo_espera = time.time() - st.session_state.inicio_busqueda
    st.markdown(f"<h2 style='text-align: center; color: #ff4b4b; animation: pulse 1.5s infinite;'>📡 Rastreando la red ({int(tiempo_espera)}s)...</h2>", unsafe_allow_html=True)
    
    # EL GUARDIÁN DESPIERTA A LOS 15 SEGUNDOS
    if tiempo_espera > 15:
        if st.session_state.partida_id:
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
            st.session_state.partida_id = None
            
        st.session_state.rival_nombre = "EL GUARDIÁN"
        st.session_state.rival_elo = st.session_state.puntos_elo + 15
        st.session_state.rival_mision = "Quebrantar tu voluntad."
        
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
        
        disponibles = supabase.table("partidas").select("*").eq("estado", "esperando").eq("tiempo_batalla", st.session_state.tiempo_combate).neq("jugador1", st.session_state.usuario_id).gte("jugador1_elo", rango_min).lte("jugador1_elo", rango_max).execute()
        
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
            
            rival_db = supabase.table("jugadores").select("nombre, elo").eq("id", sala['jugador1']).execute()
            if rival_db.data:
                st.session_state.rival_nombre = rival_db.data[0]['nombre']
                st.session_state.rival_elo = rival_db.data[0]['elo']
            else:
                st.session_state.rival_nombre = "Anónimo"
                st.session_state.rival_elo = 100
                
            st.session_state.rival_mision = sala.get('jugador1_mision', "Sobrevivir")
            st.session_state.estado = "duelo"
            st.rerun()
        else:
            nueva = supabase.table("partidas").insert({
                "jugador1": st.session_state.usuario_id, 
                "estado": "esperando",
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
            rival_db = supabase.table("jugadores").select("nombre, elo").eq("id", sala['jugador2']).execute()
            if rival_db.data:
                st.session_state.rival_nombre = rival_db.data[0]['nombre']
                st.session_state.rival_elo = rival_db.data[0]['elo']
            else:
                st.session_state.rival_nombre = "Anónimo"
                st.session_state.rival_elo = 100
                
            st.session_state.rival_mision = sala.get('jugador2_mision', "Sobrevivir")
            st.session_state.estado = "duelo"
            st.rerun()
        else:
            with st.spinner(f"Buscando guerreros..."):
                time.sleep(2)
                st.rerun()

# --- LA ARENA DE DUELO ---
elif st.session_state.estado == "duelo":
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; text-transform: uppercase; letter-spacing: 3px;'>🔥 DUELO A MUERTE 🔥</h1>", unsafe_allow_html=True)
    
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    _, _, riv_i, riv_c = calcular_rango(st.session_state.rival_elo)
    
    carta_tu = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "TÚ")
    carta_riv = generar_carta_html(st.session_state.rival_nombre, st.session_state.rival_elo, riv_i, riv_c, "ENEMIGO")
    
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
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("💀 ME RINDO (Tocar el móvil)", type="primary", use_container_width=True):
        st.session_state.puntos_elo = max(0, st.session_state.puntos_elo - st.session_state.elo_castigo)
        st.session_state.racha = 0
        supabase.table("jugadores").update({"elo": st.session_state.puntos_elo, "racha": st.session_state.racha}).eq("id", st.session_state.usuario_id).execute()
        supabase.table("historial").insert({"jugador_id": st.session_state.usuario_id, "rival_nombre": st.session_state.rival_nombre, "resultado": "derrota", "puntos_cambio": -st.session_state.elo_castigo}).execute()
        
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
        
        supabase.table("historial").insert({"jugador_id": st.session_state.usuario_id, "rival_nombre": st.session_state.rival_nombre, "resultado": "victoria", "puntos_cambio": st.session_state.elo_premio}).execute()
        
        if st.session_state.partida_id:
            supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
            
        st.session_state.ultima_pildora = random.choice(pildoras)
        st.session_state.estado = "victoria"
        st.rerun()

    components.html(f"""
        <script>
            const parentDoc = window.parent.document;
            const todosLosBotones = parentDoc.querySelectorAll('button');
            todosLosBotones.forEach(btn => {{ if(btn.innerText.includes('VICTORIA_SECRETA')) btn.closest('div[data-testid="stButton"]').style.display = 'none'; }});
            
            let tiempoRestante = {st.session_state.tiempo_combate}; 
            
            function actualizarReloj() {{
                let m = Math.floor(tiempoRestante / 60);
                let s = tiempoRestante % 60;
                let fmt = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
                parentDoc.getElementById('reloj-container').innerText = fmt;
            }}
            
            actualizarReloj();
            
            const intervalo = setInterval(function() {{
                tiempoRestante--;
                actualizarReloj();
                if (tiempoRestante <= 0) {{ 
                    clearInterval(intervalo); 
                    todosLosBotones.forEach(btn => {{ if(btn.innerText.includes('VICTORIA_SECRETA')) btn.click(); }}); 
                }}
            }}, 1000);
            
            parentDoc.addEventListener('visibilitychange', function() {{ 
                if (parentDoc.visibilityState === 'hidden') {{ 
                    clearInterval(intervalo); 
                    todosLosBotones.forEach(btn => {{ if(btn.innerText.includes('ME RINDO')) btn.click(); }}); 
                }} 
            }});
        </script>
    """, height=0, width=0)

# --- PANTALLAS FINALES ---
elif st.session_state.estado == "derrota":
    st.markdown("<h1 style='text-align: center; color: #ff1a1a; font-size: 4em; text-transform: uppercase;'>💀 DERROTA</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #ff4b4b; font-size: 3em;'>-{st.session_state.elo_castigo} ELO</h2>", unsafe_allow_html=True)
    st.error(f"Abandonaste tu misión: *'{st.session_state.mision_actual}'*. **{st.session_state.rival_nombre}** se ha llevado la gloria por tu debilidad.")
    st.write("")
    if st.button("Tragar el orgullo y volver", use_container_width=True): 
        st.session_state.estado = "lobby"; st.rerun()
        
elif st.session_state.estado == "victoria":
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
        st.session_state.estado = "lobby"; st.rerun()
