import streamlit as st
import time
import random
from datetime import datetime, timedelta, timezone
import streamlit.components.v1 as components
from supabase import create_client, Client

# --- IMPORTACIONES MODULARES (TU NUEVO EJÉRCITO) ---
from datos import pildoras, MISIONES_DESARROLLO
from motor import get_rank_info, calcular_rango, calcular_riesgo_recompensa, generar_codigo_sala, tiene_boost_activo
from idiomas import DIC
from interfaz import cargar_css, generar_carta_html, generar_html_mision, render_navbar, render_top_bar

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

# ==========================================================
# RUTAS DE LA APLICACIÓN
# ==========================================================

if st.session_state.estado == "login":
    st.write("") 
    c_hero, c_espacio, c_login = st.columns([1.2, 0.1, 1])
    
    with c_hero:
        st.markdown(f"<div style='text-align: left;'><img src='{LOGO_URL}' width='150' class='logo-breathe' style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 class='epic-title' style='text-align: left;'>LA ARENA</h1>", unsafe_allow_html=True)
        st.markdown("<div class='manifesto' style='text-align: left; margin-bottom: 25px;'>El mundo está lleno de gente que abandona cuando duele.<br><span class='highlight'>Nosotros venimos a romper al 99%.</span></div>".replace('\n', ''), unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: linear-gradient(90deg, #161616 0%, transparent 100%); border-left: 3px solid #ff4b4b; padding: 15px; margin-bottom: 15px; border-radius: 4px;'>
                <h4 style='color: white; margin: 0; font-size: 15px; text-transform: uppercase;'>⚔️ La Cárcel para tu Móvil</h4>
                <p style='color: #888; margin: 0; font-size: 13px;'>Abre la app en tu teléfono y déjalo en la mesa. Si sales de la pantalla para mirar redes sociales, tu escudo colapsa y pierdes ELO.</p>
            </div>
            <div style='background: linear-gradient(90deg, #161616 0%, transparent 100%); border-left: 3px solid #ffd700; padding: 15px; margin-bottom: 15px; border-radius: 4px;'>
                <h4 style='color: white; margin: 0; font-size: 15px; text-transform: uppercase;'>🪙 Mercado Negro de Skins</h4>
                <p style='color: #888; margin: 0; font-size: 13px;'>Sobrevive a tus sesiones de estudio para ganar monedas. Abre cofres y equipa auras y neones.</p>
            </div>
            <div style='background: linear-gradient(90deg, #161616 0%, transparent 100%); border-left: 3px solid #00ff00; padding: 15px; border-radius: 4px;'>
                <h4 style='color: white; margin: 0; font-size: 15px; text-transform: uppercase;'>🏆 Ranking Mundial y Temporadas</h4>
                <p style='color: #888; margin: 0; font-size: 13px;'>Sube desde Hierro III hasta Diamante. Solo los más disciplinados alcanzan el Salón de los Dioses.</p>
            </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    with c_login:
        st.write(""); st.write("")
        tab1, tab2 = st.tabs(["🚪 ENTRAR AL COLISEO", "📝 FORJAR UNA LEYENDA"])
        
        with tab1:
            email_log = st.text_input("Correo electrónico", key="log_email")
            pass_log = st.text_input("Contraseña", type="password", key="log_pass")
            if st.button("ACCEDER", type="primary", use_container_width=True):
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
            email_reg = st.text_input("Correo electrónico", key="reg_email")
            nombre_reg = st.text_input("Nombre de guerra (Tu Código)", key="reg_nombre")
            pass_reg = st.text_input("Contraseña", type="password", key="reg_pass")
            referido_reg = st.text_input("¿Quién te ha reclutado? (Opcional)", key="reg_ref")
            if st.button("JURAR LEALTAD", type="primary", use_container_width=True):
                if not nombre_reg: st.error("Necesitas un nombre de guerra.")
                else:
                    try:
                        monedas_iniciales = 0
                        if referido_reg:
                            reclutador_data = supabase.table("jugadores").select("id, monedas").eq("nombre", referido_reg.strip()).execute()
                            if len(reclutador_data.data) > 0:
                                r_id = reclutador_data.data[0]['id']; r_monedas = reclutador_data.data[0]['monedas']
                                supabase.table("jugadores").update({"monedas": r_monedas + 1000}).eq("id", r_id).execute(); monedas_iniciales = 500
                                st.success(f"¡Reclutado por {referido_reg}! Entras con 500 monedas extra.")
                            else: st.warning("Código de embajador no existe.")
                                
                        auth_resp = supabase.auth.sign_up({"email": email_reg, "password": pass_reg}); hoy_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
                        supabase.table("jugadores").insert({
                            "id": auth_resp.user.id, "elo": 100, "racha": 0, "monedas": monedas_iniciales, 
                            "nombre": nombre_reg, "ultima_fecha_misiones": hoy_str, "victorias": 0, "derrotas": 0,
                            "minutos_focus": 0, "bautismo_completado": False, "gremio_fecha": "", "referido_por": referido_reg if referido_reg else None
                        }).execute()
                        st.success("¡Registrado! Ve a 'Entrar al Coliseo'.")
                    except Exception as e: st.error(f"Fallo en el registro.")

elif st.session_state.estado == "bautismo":
    st.markdown("<audio autoplay src='https://actions.google.com/sounds/v1/alarms/spaceship_alarm.ogg'></audio>", unsafe_allow_html=True)
    st.markdown("<h1 class='glitch-text' style='font-size: 3em; color: #ff4b4b; margin-bottom: 0;'>⚠️ INICIANDO SECUENCIA ⚠️</h1>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='background-color: #0a0a0a; border: 2px solid #ff4b4b; padding: 40px; border-radius: 10px; margin-top: 30px; box-shadow: 0 0 30px rgba(255,0,0,0.3);'>
            <h2 style='color: white; text-align: center; text-transform: uppercase;'>Bienvenido a La Arena, <span style='color:#ff4b4b;'>{st.session_state.nombre_guerra}</span></h2>
            <p style='color: #aaa; text-align: center; font-size: 1.2em;'>Has entrado porque tu disciplina es débil y necesitas que el sistema te marque el límite.</p>
            <hr style='border: 1px solid #333; margin: 30px 0;'>
            <h3 style='color: #ff4b4b; text-align: center; margin-bottom: 20px;'>📜 EL PACTO DE SANGRE</h3>
            <ul style='color: #ddd; font-size: 1.1em; line-height: 2; list-style-type: none; padding-left: 0; text-align: center;'>
                <li><b>REGLA 1:</b> Abre esta app en tu <b>TELÉFONO MÓVIL</b>. Declara tu misión y el tiempo.</li>
                <li><b>REGLA 2:</b> Deja el móvil en la mesa. Ve a hacer tu misión (ordenador, libros, físico).</li>
                <li><b>REGLA 3:</b> Si coges el móvil y sales de esta pantalla para mirar otra cosa... <b style='color:#ff4b4b;'>tu escudo colapsa y quedas eliminado</b>.</li>
            </ul>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)
    st.write(""); st.write("")
    if st.button("🩸 ACEPTO LAS CONSECUENCIAS (ENTRAR AL LOBBY)", type="primary", use_container_width=True):
        supabase.table("jugadores").update({"bautismo_completado": True}).eq("id", st.session_state.usuario_id).execute()
        st.session_state.bautismo_visto = True; st.session_state.estado = "lobby"; st.rerun()

elif st.session_state.estado == "lobby":
    st.session_state.partida_id = None; st.session_state.rival_nombre = "Desconocido"
    rango_n, rango_s, rango_i, rango_c = calcular_rango(st.session_state.puntos_elo)
    st.markdown(f"<div style='text-align: center;'><img src='{LOGO_URL}' width='80' style='border-radius: 15px; box-shadow: 0 0 15px #ff4b4b; margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; letter-spacing: 2px; margin-top: 0;'>⚔️ MODO COMBATE</h1>", unsafe_allow_html=True)
    
    boosts_html = ""
    if tiene_boost_activo(st.session_state.boost_elo): boosts_html += "<span style='background:#ff4b4b; color:white; padding:2px 8px; border-radius:10px; font-size:12px; font-weight:bold; margin-right:5px;'>⚡ x2 ELO</span>"
    if tiene_boost_activo(st.session_state.boost_monedas): boosts_html += "<span style='background:#ffd700; color:black; padding:2px 8px; border-radius:10px; font-size:12px; font-weight:bold;'>💰 x2 MONEDAS</span>"
    st.markdown(f"<h3 style='text-align: center; color: white; text-transform: uppercase;'>Bienvenido, {st.session_state.nombre_guerra} <br><div style='margin-top:10px;'>{boosts_html}</div></h3>".replace('\n', ''), unsafe_allow_html=True)
    st.divider()
    
    carta_propia = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, rango_i, rango_c, "TU LEYENDA", st.session_state.skin_activa)
    st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'>{carta_propia}</div>".replace('\n', ''), unsafe_allow_html=True)
    st.markdown(f"<div style='display: flex; justify-content: space-around; text-align: center; background-color: #121212; padding: 25px; border-radius: 12px; border: 1px solid {rango_c}; box-shadow: 0 4px 20px {rango_c}40;'><div><p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase;'>Tu Rango</p><h2 style='margin: 0; color: {rango_c};'>{rango_i} {rango_n}</h2></div><div style='border-left: 1px solid #333; border-right: 1px solid #333; padding: 0 20px;'><p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase;'>ELO</p><h2 style='margin: 0; color: white;'>{st.session_state.puntos_elo} pts</h2></div><div><p style='margin: 0; color: #888; font-size: 14px; text-transform: uppercase;'>Bóveda</p><h2 style='margin: 0; color: #ffd700;'>🪙 {st.session_state.monedas}</h2></div></div>".replace('\n', ''), unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #00ff00; margin-top: 40px; text-shadow: 0 0 10px rgba(0,255,0,0.4);'>📜 CONTRATOS MERCENARIOS</h3>", unsafe_allow_html=True)
    
    pasos_totales = 4; pasos_actuales = min(st.session_state.progreso_m1, 1) + min(st.session_state.progreso_m2, 2) + min(st.session_state.progreso_m3, 1); porcentaje = int((pasos_actuales / pasos_totales) * 100)
    st.markdown(f"<div style='width: 100%; background-color: #333; border-radius: 10px; margin-bottom: 20px;'><div style='width: {porcentaje}%; height: 15px; background: linear-gradient(90deg, #008000, #00ff00); border-radius: 10px; box-shadow: 0 0 10px #00ff00; transition: width 0.5s ease;'></div></div><p style='text-align: center; color: #888; font-size: 12px; margin-top: -10px;'>Progreso Diario: {porcentaje}%</p>".replace('\n', ''), unsafe_allow_html=True)
    
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown(generar_html_mision("Primer Sangrado", "Gana 1 combate", 50, st.session_state.m1_reclamada), unsafe_allow_html=True)
        if st.session_state.m1_reclamada: st.button("✅ RECLAMADO", disabled=True, key="btn_m1_d", use_container_width=True)
        elif st.session_state.progreso_m1 >= 1:
            if st.button("🎁 RECLAMAR", type="primary", key="btn_m1_c", use_container_width=True):
                st.session_state.monedas += 50; st.session_state.m1_reclamada = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "m1_reclamada": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else: st.button("Falta 1", disabled=True, key="btn_m1_f", use_container_width=True)
    with c_m2:
        st.markdown(generar_html_mision("Asesino a Sueldo", "Gana 2 escaramuzas", 100, st.session_state.m2_reclamada), unsafe_allow_html=True)
        if st.session_state.m2_reclamada: st.button("✅ RECLAMADO", disabled=True, key="btn_m2_d", use_container_width=True)
        elif st.session_state.progreso_m2 >= 2:
            if st.button("🎁 RECLAMAR", type="primary", key="btn_m2_c", use_container_width=True):
                st.session_state.monedas += 100; st.session_state.m2_reclamada = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "m2_reclamada": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else: st.button(f"Faltan {2 - st.session_state.progreso_m2}", disabled=True, key="btn_m2_f", use_container_width=True)
    with c_m3:
        st.markdown(generar_html_mision("El Titán", "Sobrevive 1 asalto", 300, st.session_state.m3_reclamada), unsafe_allow_html=True)
        if st.session_state.m3_reclamada: st.button("✅ RECLAMADO", disabled=True, key="btn_m3_d", use_container_width=True)
        elif st.session_state.progreso_m3 >= 1:
            if st.button("🎁 RECLAMAR", type="primary", key="btn_m3_c", use_container_width=True):
                st.session_state.monedas += 300; st.session_state.m3_reclamada = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "m3_reclamada": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else: st.button("Falta 1", disabled=True, key="btn_m3_f", use_container_width=True)

    st.write(""); st.divider()
    st.markdown("""
        <div class="rules-box">
            <h3 style="text-align: center; color: #ff4b4b; text-transform: uppercase; margin-top: 0;">⚠️ Las Leyes de la Arena</h3>
            <ul style="list-style-type: none; padding-left: 0; color: #ccc; font-size: 15px; line-height: 1.8;">
                <li style="margin-bottom: 10px;">📱 <span class="neon-green">CÓMO SE JUEGA:</span> Abre esto en tu móvil, déjalo en la mesa y ve a trabajar en tu PC o en tus libros.</li>
                <li style="margin-bottom: 10px;">🔴 <span class="neon-red">CÓMO PIERDES:</span> Si coges el móvil y cambias de app, tu escudo colapsa y pierdes ELO.</li>
                <li>⚔️ <strong style="color: #ffd700;">EL PACTO:</strong> Convierte tu móvil en tu propio vigilante. No te engañes a ti mismo.</li>
            </ul>
        </div>
    """.replace('\n', ''), unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #ff4b4b;'>🔥 DECLARACIÓN DE INTENCIONES</h3>", unsafe_allow_html=True)
    c_texto, c_dado = st.columns([5, 1])
    with c_dado:
        st.write("")
        if st.button("🎲", help="Deja que el Oráculo decida tu destino.", use_container_width=True):
            st.session_state.input_mision_texto = random.choice(MISIONES_DESARROLLO); st.rerun()
    with c_texto:
        mision_input = st.text_input("", value=st.session_state.input_mision_texto, placeholder="Ej: Terminar el ensayo de Filosofía...", label_visibility="collapsed")
        st.session_state.input_mision_texto = mision_input 
    
    tiempo_opts = {"⚙️ Modo Test (10 Segundos)": 10}
    for m in range(15, 105, 5):
        if m == 25: tiempo_opts["⚔️ Escaramuza (25 Minutos)"] = m * 60
        elif m == 50: tiempo_opts["🔥 Asalto Profundo (50 Minutos)"] = m * 60
        elif m == 90: tiempo_opts["💀 Modo Titán (90 Minutos)"] = m * 60
        else: tiempo_opts[f"⏱️ {m} Minutos"] = m * 60

    tiempo_str = st.selectbox("Duración de la batalla:", list(tiempo_opts.keys()))
    
    c_pub, c_priv = st.columns(2)
    with c_pub:
        if st.button("🌍 BÚSQUEDA MUNDIAL", use_container_width=True, type="primary"):
            if not st.session_state.input_mision_texto: st.error("Un guerrero no entra sin propósito. Declara tu misión o usa el dado 🎲.")
            else:
                limite_fantasmas = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
                supabase.table("partidas").delete().eq("estado", "esperando").lt("ultima_actividad", limite_fantasmas).execute()
                st.session_state.mision_actual = st.session_state.input_mision_texto; st.session_state.tiempo_combate = tiempo_opts[tiempo_str]
                w_elo, l_elo, coins = calcular_riesgo_recompensa(st.session_state.tiempo_combate, st.session_state.puntos_elo, st.session_state.boost_elo, st.session_state.boost_monedas)
                st.session_state.elo_premio = w_elo; st.session_state.elo_castigo = l_elo; st.session_state.monedas_ganadas_recientes = coins
                st.session_state.tipo_partida = "publica"; st.session_state.codigo_sala = ""; st.session_state.inicio_busqueda = time.time(); st.session_state.estado = "buscando"; st.rerun()
    st.markdown("<h3 style='text-align: center; color: #888; margin-top: 30px;'>🤝 DUELO PRIVADO</h3>", unsafe_allow_html=True)
    c_p1, c_p2 = st.columns([2, 1])
    with c_p1: codigo_input = st.text_input("", placeholder="Pega código o vacío para crear", label_visibility="collapsed", key="input_cod_priv")
    with c_p2:
        if st.button("🚪 CREAR / UNIRSE", use_container_width=True):
            if not st.session_state.input_mision_texto: st.error("Declara tu misión primero.")
            else:
                st.session_state.mision_actual = st.session_state.input_mision_texto; st.session_state.tiempo_combate = tiempo_opts[tiempo_str]
                w_elo, l_elo, coins = calcular_riesgo_recompensa(st.session_state.tiempo_combate, st.session_state.puntos_elo, st.session_state.boost_elo, st.session_state.boost_monedas)
                st.session_state.elo_premio = w_elo; st.session_state.elo_castigo = l_elo; st.session_state.monedas_ganadas_recientes = coins
                st.session_state.tipo_partida = "privada"; st.session_state.codigo_sala = codigo_input.upper().strip() if codigo_input else generar_codigo_sala()
                st.session_state.inicio_busqueda = time.time(); st.session_state.estado = "buscando_privada"; st.rerun()
    render_navbar("lobby")

elif st.session_state.estado == "gremio":
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; letter-spacing: 2px;'>⚔️ EL GREMIO</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #888; margin-bottom: 30px;'>Conquista la realidad. Sistema de honor activado.</h4>", unsafe_allow_html=True)

    hoy_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    if st.session_state.gremio_fecha != hoy_str:
        supabase.table("jugadores").update({"gremio_fecha": hoy_str, "gremio_m1": False, "gremio_m2": False, "gremio_m3": False, "gremio_m4": False}).eq("id", st.session_state.usuario_id).execute()
        st.session_state.gremio_fecha = hoy_str; st.session_state.gremio_m1 = False; st.session_state.gremio_m2 = False; st.session_state.gremio_m3 = False; st.session_state.gremio_m4 = False

    st.markdown("<div style='background-color: #110000; border: 1px solid #ff4b4b; border-radius: 8px; padding: 15px; margin-bottom: 20px;'><p style='color: #ccc; margin: 0; font-size: 14px; text-align: center;'>⚠️ <b>ATENCIÓN:</b> El sistema no puede verificar si haces estas misiones. Si mientes pulsando el botón sin haber sudado, estarás corrompiendo tu propia mente.</p></div>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        st.markdown(generar_html_mision("BAÑO DE HIELO", "Ducha de agua fría total (Min 2 min)", 100, st.session_state.gremio_m1), unsafe_allow_html=True)
        if st.session_state.gremio_m1: st.button("✅ SUPERADO", disabled=True, key="g_m1_d", use_container_width=True)
        else:
            if st.button("🩸 LO HE HECHO", type="primary", key="g_m1_c", use_container_width=True):
                st.session_state.monedas += 100; st.session_state.gremio_m1 = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "gremio_m1": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                
        st.markdown(generar_html_mision("SANGRE EN LAS VENAS", "50 Flexiones (Puedes dividir en series)", 150, st.session_state.gremio_m2), unsafe_allow_html=True)
        if st.session_state.gremio_m2: st.button("✅ SUPERADO", disabled=True, key="g_m2_d", use_container_width=True)
        else:
            if st.button("🩸 LO HE HECHO", type="primary", key="g_m2_c", use_container_width=True):
                st.session_state.monedas += 150; st.session_state.gremio_m2 = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "gremio_m2": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()

    with g2:
        st.markdown(generar_html_mision("MENTE DESPEJADA", "Barrer, fregar y recoger tu cuarto al 100%", 100, st.session_state.gremio_m3), unsafe_allow_html=True)
        if st.session_state.gremio_m3: st.button("✅ SUPERADO", disabled=True, key="g_m3_d", use_container_width=True)
        else:
            if st.button("🩸 LO HE HECHO", type="primary", key="g_m3_c", use_container_width=True):
                st.session_state.monedas += 100; st.session_state.gremio_m3 = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "gremio_m3": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                
        st.markdown(generar_html_mision("CONOCIMIENTO", "Leer 15 páginas de un libro (No digital)", 150, st.session_state.gremio_m4), unsafe_allow_html=True)
        if st.session_state.gremio_m4: st.button("✅ SUPERADO", disabled=True, key="g_m4_d", use_container_width=True)
        else:
            if st.button("🩸 LO HE HECHO", type="primary", key="g_m4_c", use_container_width=True):
                st.session_state.monedas += 150; st.session_state.gremio_m4 = True
                supabase.table("jugadores").update({"monedas": st.session_state.monedas, "gremio_m4": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()

    render_navbar("gremio")

elif st.session_state.estado == "mundo":
    st.markdown("<h1 style='text-align: center; color: #fff; letter-spacing: 2px;'>🌍 LA PLAZA PÚBLICA</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray; margin-bottom: 30px;'>El mundo está observando.</h4>", unsafe_allow_html=True)
    c_feed, c_rank = st.columns([1.2, 1])
    with c_rank:
        st.markdown("<h3 style='color: #ffd700; text-align: center;'>🏆 TOP GLOBAL</h3>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: #111; border: 1px solid #333; border-radius: 12px; padding: 15px;'>", unsafe_allow_html=True)
        top_players = supabase.table("jugadores").select("nombre, elo, skin_activa").order("elo", desc=True).limit(10).execute()
        if top_players.data:
            for idx, p in enumerate(top_players.data):
                p_nombre = p['nombre']; p_elo = p['elo']; r_n, r_s, r_i, r_c = calcular_rango(p_elo)
                color_pos = "#ffd700" if idx == 0 else "#c0c0c0" if idx == 1 else "#cd7f32" if idx == 2 else "#888"
                st.markdown(f"<div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; padding: 10px 0;'><div style='display: flex; align-items: center; gap: 10px;'><strong style='color: {color_pos}; font-size: 18px;'>#{idx+1}</strong><span style='color: white; font-weight: bold;'>{p_nombre}</span></div><div style='text-align: right;'><span style='color: {r_c}; font-size: 12px;'>{r_i} {p_elo} pts</span></div></div>".replace('\n', ''), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c_feed:
        st.markdown("<h3 style='color: #00aaff; text-align: center;'>📡 MURO EN DIRECTO</h3>", unsafe_allow_html=True)
        st.markdown("<div class='feed-box' style='background-color: #0a0a0a; border: 1px solid #333; border-radius: 12px; padding: 15px; height: 450px; overflow-y: auto;'>", unsafe_allow_html=True)
        feed = supabase.table("historial").select("*").order("id", desc=True).limit(15).execute()
        if feed.data:
            for f in feed.data:
                res = f['resultado']; puntos = f['puntos_cambio']; j_nom = f.get('jugador_nombre', 'Un guerrero'); r_nom = f.get('rival_nombre', 'el Guardián')
                if res == "victoria": color = "#00ff00"; icono = "🟢"; texto = f"**{j_nom}** completó su misión y roba <span style='color:{color};'>+{puntos} ELO</span>."
                else: color = "#ff4b4b"; icono = "🔴"; texto = f"El escudo de **{j_nom}** colapsó. Pierde <span style='color:{color};'>{puntos} ELO</span>."
                st.markdown(f"<div style='background-color: #111; border-left: 3px solid {color}; padding: 10px; margin-bottom: 8px; border-radius: 4px;'><p style='color: #ccc; margin: 0; font-size: 13px;'>{icono} {texto}</p></div>".replace('\n', ''), unsafe_allow_html=True)
        else: st.markdown("<p style='text-align: center; color: #555;'>El silencio reina en la arena...</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<h3 style='text-align: center; color: #ffd700; margin-top: 20px;'>📜 LEYENDAS INMORTALES</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 14px;'>El Salón de los Dioses. Solo los ganadores de temporadas pasadas.</p>", unsafe_allow_html=True)
    leyendas = supabase.table("leyendas").select("*").order("temporada", desc=True).execute()
    if leyendas.data:
        for l in leyendas.data:
            st.markdown(f"<div style='background:#1a1a1a; border-left:4px solid {l['rango_color']}; padding:15px; margin-bottom:10px;'><h4 style='margin:0; color:white;'>Temporada {l['temporada']}: {l['nombre']}</h4><p style='margin:0; color:#888;'>{l['rango_icono']} {l['rango_nombre']} - {l['elo_final']} ELO</p></div>".replace('\n', ''), unsafe_allow_html=True)
    else: st.markdown("<div style='text-align:center; padding:30px; border:1px dashed #333;'><p style='color:#555; font-style:italic;'>El pedestal está vacío. Sé tú el primero.</p></div>".replace('\n', ''), unsafe_allow_html=True)
        
    render_navbar("mundo")

elif st.session_state.estado == "tienda":
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    st.markdown("<h1 style='text-align: center; color: #ffd700; letter-spacing: 2px;'>🛒 EL MERCADO NEGRO</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: #1a1a1a; border: 1px solid #ffd700; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 30px;'><p style='margin:0; color:#aaa; font-size:14px;'>Fondos Disponibles</p><h2 style='margin:0; color:#ffd700; font-size:36px;'>🪙 {st.session_state.monedas}</h2></div>".replace('\n', ''), unsafe_allow_html=True)
    
    st.markdown("### 🎲 EL COFRE DEL GLADIADOR")
    st.markdown(f"<div style='background:#121212; border:2px solid #ffd700; padding:20px; text-align:center; border-radius:8px;'><h1 style='font-size: 80px; margin:0;'>🧰</h1><h3 style='color: white; margin-top: 10px;'>Cofre Misterioso</h3><p style='color: #888; font-size: 12px;'>🟦 70% | 🟪 20% | 🟥 9% | 🟨 1%</p><h2 style='color:#ffd700; margin-bottom: 20px;'>🪙 1000</h2></div>".replace('\n', ''), unsafe_allow_html=True)
    if st.button("🎲 ABRIR COFRE (1000 Monedas)", type="primary", use_container_width=True):
        if st.session_state.monedas >= 1000:
            st.session_state.monedas -= 1000; supabase.table("jugadores").update({"monedas": st.session_state.monedas}).eq("id", st.session_state.usuario_id).execute()
            st.session_state.estado = "cofre_animacion"; st.rerun()
        else: st.error("No tienes fondos para el azar.")
    
    st.markdown("### 🧬 BOOSTS DIRECTOS (24H)")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("<div style='background:#121212; border:1px solid #333; padding:15px; text-align:center; border-radius:8px;'><h3>⚡ x2 ELO</h3><h3 style='color:#ffd700;'>🪙 150</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.button("COMPRAR ELO", key="b_elo", use_container_width=True):
            if st.session_state.monedas >= 150:
                st.session_state.monedas -= 150; fin = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
                st.session_state.boost_elo = fin; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "boost_elo_hasta": fin}).eq("id", st.session_state.usuario_id).execute(); st.success("¡Boost ELO!"); time.sleep(1); st.rerun()
            else: st.error("No tienes oro.")
    with b2:
        st.markdown("<div style='background:#121212; border:1px solid #333; padding:15px; text-align:center; border-radius:8px;'><h3>💰 x2 ORO</h3><h3 style='color:#ffd700;'>🪙 200</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.button("COMPRAR ORO", key="b_oro", use_container_width=True):
            if st.session_state.monedas >= 200:
                st.session_state.monedas -= 200; fin = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
                st.session_state.boost_monedas = fin; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "boost_monedas_hasta": fin}).eq("id", st.session_state.usuario_id).execute(); st.success("¡Boost ORO!"); time.sleep(1); st.rerun()
            else: st.error("No tienes oro.")

    st.markdown("### 🔥 COMPRA DIRECTA")
    t1, t2 = st.columns(2)
    carta_aura = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'aura')
    with t1:
        st.markdown(f"<div style='background:#121212; border:1px solid #ff4b4b; padding:15px; text-align:center; border-radius:8px;'>{carta_aura}<h4 style='margin-top:10px;'>Aura Sanguinaria</h4><p style='color:#ff4b4b;'>Mítica</p><h3 style='color:#ffd700;'>🪙 5000</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.session_state.inv_aura:
            if st.session_state.skin_activa == 'aura': st.info("EQUIPADA")
            elif st.button("EQUIPAR", key="eq_aura", use_container_width=True): st.session_state.skin_activa = 'aura'; supabase.table("jugadores").update({"skin_activa": "aura"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else:
            if st.button("COMPRAR", key="cp_aura", use_container_width=True):
                if st.session_state.monedas >= 5000: st.session_state.monedas -= 5000; st.session_state.inv_aura = True; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "inventario_aura": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                else: st.error("Ahorra.")
                
    carta_corona = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'corona')
    with t2:
        st.markdown(f"<div style='background:#121212; border:1px solid #ffd700; padding:15px; text-align:center; border-radius:8px;'>{carta_corona}<h4 style='margin-top:10px;'>Corona del Rey</h4><p style='color:#ffd700;'>Legendaria</p><h3 style='color:#ffd700;'>🪙 10000</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.session_state.inv_corona:
            if st.session_state.skin_activa == 'corona': st.info("EQUIPADA")
            elif st.button("EQUIPAR", key="eq_cor", use_container_width=True): st.session_state.skin_activa = 'corona'; supabase.table("jugadores").update({"skin_activa": "corona"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else:
            if st.button("COMPRAR", key="cp_cor", use_container_width=True):
                if st.session_state.monedas >= 10000: st.session_state.monedas -= 10000; st.session_state.inv_corona = True; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "inventario_corona": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                else: st.error("Ahorra.")

    t3, t4 = st.columns(2)
    carta_sombra = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'sombra')
    with t3:
        st.markdown(f"<div style='background:#121212; border:1px solid #00aaff; padding:15px; text-align:center; border-radius:8px;'>{carta_sombra}<h4 style='margin-top:10px;'>Sombra Persistente</h4><p style='color:#00aaff;'>Rara</p><h3 style='color:#ffd700;'>🪙 1500</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.session_state.inv_sombra:
            if st.session_state.skin_activa == 'sombra': st.info("EQUIPADA")
            elif st.button("EQUIPAR", key="eq_som", use_container_width=True): st.session_state.skin_activa = 'sombra'; supabase.table("jugadores").update({"skin_activa": "sombra"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else:
            if st.button("COMPRAR", key="cp_som", use_container_width=True):
                if st.session_state.monedas >= 1500: st.session_state.monedas -= 1500; st.session_state.inv_sombra = True; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "inv_sombra": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                else: st.error("Ahorra.")

    carta_fuego = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "PREVIA", 'fuego')
    with t4:
        st.markdown(f"<div style='background:#121212; border:1px solid #aa00ff; padding:15px; text-align:center; border-radius:8px;'>{carta_fuego}<h4 style='margin-top:10px;'>Fuego Fatuo</h4><p style='color:#aa00ff;'>Épica</p><h3 style='color:#ffd700;'>🪙 2500</h3></div>".replace('\n', ''), unsafe_allow_html=True)
        if st.session_state.inv_fuego:
            if st.session_state.skin_activa == 'fuego': st.info("EQUIPADA")
            elif st.button("EQUIPAR", key="eq_fue", use_container_width=True): st.session_state.skin_activa = 'fuego'; supabase.table("jugadores").update({"skin_activa": "fuego"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
        else:
            if st.button("COMPRAR", key="cp_fue", use_container_width=True):
                if st.session_state.monedas >= 2500: st.session_state.monedas -= 2500; st.session_state.inv_fuego = True; supabase.table("jugadores").update({"monedas": st.session_state.monedas, "inv_fuego": True}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
                else: st.error("Ahorra.")

    if st.button("✖ QUITAR SKIN ACTUAL", use_container_width=True):
        st.session_state.skin_activa = 'default'; supabase.table("jugadores").update({"skin_activa": "default"}).eq("id", st.session_state.usuario_id).execute(); st.rerun()
    render_navbar("tienda")

elif st.session_state.estado == "cuartel":
    info_rango = get_rank_info(st.session_state.puntos_elo)
    rango_n, rango_s, rango_i, rango_c, elo_min, elo_max, rango_nivel = info_rango
    st.markdown("<h1 style='text-align: center; color: #fff; letter-spacing: 2px;'>🛡️ CUARTEL GENERAL</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: {rango_c}; margin-bottom: 30px;'>Registro de Guerra de {st.session_state.nombre_guerra}</h4>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='background-color: #111; border: 1px dashed #ffd700; border-radius: 8px; padding: 20px; text-align: center; margin-bottom: 30px;'><h3 style='color: #ffd700; margin-top: 0;'>🤝 PROGRAMA DE EMBAJADORES</h3><p style='color: #888; font-size: 14px;'>Tu Código de Reclutamiento:</p><h2 style='color: white; font-family: monospace; letter-spacing: 2px;'>{st.session_state.nombre_guerra}</h2><p style='color: #555; font-size: 12px; margin-bottom: 0;'>Si un amigo usa tu nombre al registrarse, tú ganas 🪙 1000 y él 🪙 500.</p></div>".replace('\n', ''), unsafe_allow_html=True)

    if elo_min == elo_max: porcentaje_elo = 100; texto_progreso = f"RANGO MÁXIMO ALCANZADO ({st.session_state.puntos_elo} ELO)"
    else: puntos_conseguidos = st.session_state.puntos_elo - elo_min; puntos_rango = elo_max - elo_min; porcentaje_elo = int((puntos_conseguidos / puntos_rango) * 100); texto_progreso = f"{st.session_state.puntos_elo} / {elo_max} ELO para el siguiente rango"

    st.markdown(f"<div style='background-color: #111; border: 1px solid {rango_c}; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 30px;'><h3 style='color: white; margin-top: 0;'>PROGRESO DE LIGA: {rango_i} {rango_n}</h3><div style='width: 100%; background-color: #333; border-radius: 10px; margin: 15px 0;'><div style='width: {porcentaje_elo}%; height: 20px; background: linear-gradient(90deg, #111, {rango_c}); border-radius: 10px; transition: width 0.5s ease;'></div></div><p style='color: #888; font-size: 14px; font-weight: bold; margin: 0;'>{texto_progreso} ({porcentaje_elo}%)</p></div>".replace('\n', ''), unsafe_allow_html=True)

    total_partidas = st.session_state.victorias + st.session_state.derrotas
    winrate = int((st.session_state.victorias / total_partidas) * 100) if total_partidas > 0 else 0
    horas_focus = round(st.session_state.minutos_focus / 60, 1)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div style='background-color: #161616; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center;'><p style='color: #888; font-size: 12px; margin: 0;'>Winrate</p><h2 style='color: #00ff00; margin: 5px 0;'>{winrate}%</h2><p style='color: #555; font-size: 10px; margin: 0;'>{st.session_state.victorias} V / {st.session_state.derrotas} D</p></div>".replace('\n', ''), unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='background-color: #161616; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center;'><p style='color: #888; font-size: 12px; margin: 0;'>Tiempo Profundo</p><h2 style='color: #00aaff; margin: 5px 0;'>{horas_focus}h</h2><p style='color: #555; font-size: 10px; margin: 0;'>{st.session_state.minutos_focus} Min. Totales</p></div>".replace('\n', ''), unsafe_allow_html=True)
    with c3: st.markdown(f"<div style='background-color: #161616; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center;'><p style='color: #888; font-size: 12px; margin: 0;'>Mejor Racha</p><h2 style='color: #ff4b4b; margin: 5px 0;'>🔥 {st.session_state.racha}</h2><p style='color: #555; font-size: 10px; margin: 0;'>Seguidas</p></div>".replace('\n', ''), unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #fff; margin-top: 40px;'>👥 HERMANOS DE SANGRE</h3>", unsafe_allow_html=True)
    col_am_1, col_am_2 = st.columns([3, 1])
    with col_am_1: amigo_input = st.text_input("Añadir guerrero", placeholder="Nombre exacto", label_visibility="collapsed")
    with col_am_2:
        if st.button("➕ AÑADIR", use_container_width=True):
            if amigo_input.strip() == st.session_state.nombre_guerra: st.error("No puedes añadirte a ti mismo.")
            elif amigo_input:
                try:
                    comprobar = supabase.table("jugadores").select("id").eq("nombre", amigo_input.strip()).execute()
                    if len(comprobar.data) > 0:
                        supabase.table("amigos").insert({"jugador_id": st.session_state.usuario_id, "amigo_nombre": amigo_input.strip()}).execute()
                        st.success(f"¡{amigo_input} añadido a tus filas!"); time.sleep(1); st.rerun()
                    else: st.error("Guerrero no encontrado.")
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
        else: st.markdown("<p style='text-align: center; color: #555; margin-top: 20px;'>Peleas solo. Añade a tus aliados.</p>", unsafe_allow_html=True)
    except Exception as e: st.markdown("<p style='text-align: center; color: #ff4b4b; margin-top: 20px;'>⚠️ Tabla de amigos no configurada aún.</p>", unsafe_allow_html=True)

    with st.expander("⚙️ Ajustes de Perfil"):
        nuevo_nombre = st.text_input("Cambiar nombre (cambiará tu código)", value=st.session_state.nombre_guerra)
        if st.button("ACTUALIZAR NOMBRE"):
            supabase.table("jugadores").update({"nombre": nuevo_nombre}).eq("id", st.session_state.usuario_id).execute()
            st.session_state.nombre_guerra = nuevo_nombre; st.success("¡Actualizado!"); time.sleep(1); st.rerun()
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
    st.markdown("<audio autoplay loop src='https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3'></audio>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #ff4b4b; text-transform: uppercase; letter-spacing: 3px;'>🔥 DUELO A MUERTE 🔥</h1>", unsafe_allow_html=True)
    _, _, tu_i, tu_c = calcular_rango(st.session_state.puntos_elo)
    _, _, riv_i, riv_c = calcular_rango(st.session_state.rival_elo)
    carta_tu = generar_carta_html(st.session_state.nombre_guerra, st.session_state.puntos_elo, tu_i, tu_c, "TÚ", st.session_state.skin_activa)
    carta_riv = generar_carta_html(st.session_state.rival_nombre, st.session_state.rival_elo, riv_i, riv_c, "ENEMIGO", st.session_state.get('rival_skin', 'default'))
    st.markdown(f"<div style='display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; margin-top: 20px;'>{carta_tu}<h1 style='color: #ff4b4b; font-size: 50px; font-style: italic;'>VS</h1>{carta_riv}</div>".replace('\n', ''), unsafe_allow_html=True)
    st.markdown(f"<div style='display: flex; justify-content: space-between; background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; margin-top: 15px;'><div style='text-align: left; width: 45%;'><p style='color: {tu_c}; margin: 0; font-weight: bold; font-size: 12px;'>TU OBJETIVO</p><p style='color: white; font-family: monospace; font-size: 14px; margin: 0;'>{st.session_state.mision_actual}</p></div><div style='border-left: 1px solid #333;'></div><div style='text-align: right; width: 45%;'><p style='color: {riv_c}; margin: 0; font-weight: bold; font-size: 12px;'>OBJETIVO ENEMIGO</p><p style='color: white; font-family: monospace; font-size: 14px; margin: 0;'>{st.session_state.rival_mision}</p></div></div>".replace('\n', ''), unsafe_allow_html=True)
    st.markdown("<div style='background-color: #0a0a0a; border: 2px solid #ff4b4b; border-radius: 15px; padding: 20px; margin: 30px 0; box-shadow: 0 0 30px rgba(255, 75, 75, 0.2);'><div id='reloj-container' style='text-align: center; font-size: 80px; font-family: monospace; font-weight: bold; color: white;'>--:--</div><div id='audio-container'></div></div>".replace('\n', ''), unsafe_allow_html=True)
    
    if st.button("💀 ME RINDO (Tocar el móvil)", type="primary", use_container_width=True):
        st.session_state.puntos_elo = max(0, st.session_state.puntos_elo - st.session_state.elo_castigo); st.session_state.racha = 0; st.session_state.derrotas += 1; st.session_state.minutos_focus += int(st.session_state.tiempo_combate / 60)
        supabase.table("jugadores").update({"elo": st.session_state.puntos_elo, "racha": st.session_state.racha, "derrotas": st.session_state.derrotas, "minutos_focus": st.session_state.minutos_focus}).eq("id", st.session_state.usuario_id).execute()
        supabase.table("historial").insert({"jugador_id": st.session_state.usuario_id, "jugador_nombre": st.session_state.nombre_guerra, "rival_nombre": st.session_state.rival_nombre, "resultado": "derrota", "puntos_cambio": -st.session_state.elo_castigo}).execute()
        if st.session_state.partida_id: supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
        st.session_state.estado = "derrota"; st.rerun()
            
    if st.button("VICTORIA_SECRETA", key="btn_victoria"):
        viejo_rango_idx = get_rank_info(st.session_state.puntos_elo)[6]
        st.session_state.puntos_elo += st.session_state.elo_premio; st.session_state.racha += 1; st.session_state.monedas += st.session_state.monedas_ganadas_recientes; st.session_state.victorias += 1; st.session_state.minutos_focus += int(st.session_state.tiempo_combate / 60)
        st.session_state.progreso_m1 += 1  
        if st.session_state.tiempo_combate == 1500: st.session_state.progreso_m2 += 1
        elif st.session_state.tiempo_combate == 5400: st.session_state.progreso_m3 += 1
            
        supabase.table("jugadores").update({"elo": st.session_state.puntos_elo, "racha": st.session_state.racha, "monedas": st.session_state.monedas, "progreso_m1": st.session_state.progreso_m1, "progreso_m2": st.session_state.progreso_m2, "progreso_m3": st.session_state.progreso_m3, "victorias": st.session_state.victorias, "minutos_focus": st.session_state.minutos_focus}).eq("id", st.session_state.usuario_id).execute()
        supabase.table("historial").insert({"jugador_id": st.session_state.usuario_id, "jugador_nombre": st.session_state.nombre_guerra, "rival_nombre": st.session_state.rival_nombre, "resultado": "victoria", "puntos_cambio": st.session_state.elo_premio}).execute()
        if st.session_state.partida_id: supabase.table("partidas").delete().eq("id", st.session_state.partida_id).execute()
        st.session_state.ultima_pildora = random.choice(pildoras); nuevo_rango = get_rank_info(st.session_state.puntos_elo)
        if nuevo_rango[6] > viejo_rango_idx: st.session_state.rango_alcanzado_nombre = f"{nuevo_rango[2]} {nuevo_rango[0]} - {nuevo_rango[1]}"; st.session_state.rango_alcanzado_color = nuevo_rango[3]; st.session_state.estado = "ascenso"
        else: st.session_state.estado = "victoria"
        st.rerun()

    components.html(f"""
        <script>
            const parentDoc = window.parent.document;
            const todosLosBotones = parentDoc.querySelectorAll('button');
            todosLosBotones.forEach(btn => {{ if(btn.innerText.includes('VICTORIA_SECRETA')) btn.closest('div[data-testid="stButton"]').style.display = 'none'; }});
            let tiempoRestante = {st.session_state.tiempo_combate}; let latidoReproducido = false;
            function actualizarReloj() {{
                let m = Math.floor(tiempoRestante / 60); let s = tiempoRestante % 60; let fmt = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
                parentDoc.getElementById('reloj-container').innerText = fmt;
                if (tiempoRestante <= 10 && tiempoRestante > 0) {{ let audioTick = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg'); audioTick.play(); }}
            }}
            actualizarReloj();
            const intervalo = setInterval(function() {{
                tiempoRestante--; actualizarReloj();
                if (tiempoRestante <= 0) {{ clearInterval(intervalo); todosLosBotones.forEach(btn => {{ if(btn.innerText.includes('VICTORIA_SECRETA')) btn.click(); }}); }}
            }}, 1000);
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
