from idiomas import DIC
import streamlit as st

def cargar_css():
    st.markdown("""
        <style>
        /* Importar fuente letal */
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
        
        * {
            font-family: 'Oswald', sans-serif !important;
        }

        /* Animaciones de respiración y latido */
        @keyframes pulse-red {
            0% { box-shadow: 0 0 10px #ff4b4b, inset 0 0 5px #ff4b4b; }
            50% { box-shadow: 0 0 25px #ff4b4b, inset 0 0 10px #ff4b4b; }
            100% { box-shadow: 0 0 10px #ff4b4b, inset 0 0 5px #ff4b4b; }
        }
        @keyframes levitate {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        @keyframes neon-flicker {
            0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ff4b4b, 0 0 40px #ff4b4b; }
            20%, 24%, 55% { text-shadow: none; }
        }

        /* Títulos Épicos */
        .epic-title {
            text-align: center;
            color: #ffffff;
            font-size: 3.5rem;
            text-transform: uppercase;
            letter-spacing: 5px;
            margin-bottom: 0.5rem;
            animation: neon-flicker 4s infinite;
        }

        /* Cartas de Jugador con Efecto de Levitación Continua */
        .player-card {
            background: linear-gradient(145deg, #161616, #0a0a0a);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            width: 160px;
            transition: all 0.3s ease;
            /* AQUÍ ESTÁ LA MAGIA QUE QUERÍAS: Levitación automática y constante */
            animation: levitate 3s ease-in-out infinite; 
        }
        .player-card:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 30px rgba(255, 75, 75, 0.2);
            cursor: crosshair;
        }

        /* Botón de Peligro (Rendirse) */
        .btn-peligro button {
            background-color: transparent !important;
            border: 2px solid #ff4b4b !important;
            color: #ff4b4b !important;
            transition: all 0.3s ease !important;
        }
        .btn-peligro button:hover {
            background-color: #ff4b4b !important;
            color: white !important;
            animation: pulse-red 1s infinite !important;
        }

        /* Modificación de Inputs y Formularios para que parezcan terminales */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: #0a0a0a !important;
            border: 1px solid #333 !important;
            color: #00ff00 !important;
            font-family: monospace !important;
            border-radius: 4px !important;
        }
        .stTextInput input:focus {
            border-color: #ff4b4b !important;
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.3) !important;
        }

        /* Esconder la barra superior de Streamlit y el footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def generar_carta_html(nombre, elo, rango_i, rango_c, subtitulo, skin='default'):
    display_name = f"👑 {nombre}" if skin == 'corona' else nombre
    if skin == 'aura': color_borde = "#ff0000"; clase_animacion = "anim-aura"; efecto_sombra = ""
    elif skin == 'fuego': color_borde = "#aa00ff"; clase_animacion = "anim-fuego"; efecto_sombra = ""
    elif skin == 'sombra': color_borde = "#00aaff"; clase_animacion = "anim-sombra"; efecto_sombra = ""
    else: color_borde = rango_c; clase_animacion = "anim-float"; efecto_sombra = f"box-shadow: 0 0 20px {color_borde}30;"

    html_bruto = f"""
    <div class="fut-card {clase_animacion}" style="background: linear-gradient(135deg, #161616 0%, #050505 100%); border: 2px solid {color_borde}; border-radius: 12px; width: 140px; margin: 10px; padding: 15px 10px; position: relative; {efecto_sombra} display: inline-block; text-align: center; transition: all 0.3s ease;">
        <div style="position: absolute; top: 8px; left: 12px; color: {color_borde}; font-weight: 900; font-size: 20px; font-family: monospace; text-shadow: 0 0 5px {color_borde};">{elo}</div>
        <div style="position: absolute; top: 8px; right: 12px; font-size: 20px; filter: drop-shadow(0 0 5px {color_borde});">{rango_i}</div>
        <div style="margin-top: 35px; margin-bottom: 10px;">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="{color_borde}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.9; filter: drop-shadow(0 0 8px {color_borde});"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        </div>
        <h4 style="color: white; margin: 0; font-size: 14px; text-transform: uppercase; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: 1px;">{display_name}</h4>
        <div style="color: #666; font-size: 11px; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px; font-weight: bold;">{subtitulo}</div>
    </div>
    """
    return html_bruto.replace("\n", "")

def generar_html_mision(titulo, desc, oro, completada):
    color_borde = "#00ff00" if completada else "#333"
    opacidad = "0.5" if completada else "1"
    html_mision = f"""
    <div style="background-color: #121212; border: 1px solid {color_borde}; border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 10px; opacity: {opacidad}; transition: all 0.3s ease; box-shadow: 0 0 10px {color_borde}40;">
        <h4 style="color: white; margin: 0 0 5px 0; font-size: 14px; text-transform: uppercase;">{titulo}</h4>
        <p style="color: #888; font-size: 11px; margin: 0 0 10px 0;">{desc}</p>
        <h3 style="color: #ffd700; margin: 0; text-shadow: 0 0 5px rgba(255,215,0,0.5);">🪙 {oro}</h3>
    </div>
    """
    return html_mision.replace("\n", "")

from idiomas import DIC

# (Mantén tus funciones cargar_css, generar_carta_html, etc. intactas arriba)

def render_top_bar():
    # Botón flotante superior derecho para cambiar idioma instantáneamente
    lang = st.session_state.get('idioma', 'es')
    c1, c2 = st.columns([8, 1.5])
    with c2:
        if st.button(DIC[lang]["lang_btn"], use_container_width=True):
            st.session_state.idioma = 'en' if lang == 'es' else 'es'
            st.rerun()

def render_navbar(origen):
    lang = st.session_state.get('idioma', 'es')
    st.markdown("<hr style='border: 1px solid #333; margin-top: 40px;'>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns([1, 0.02, 1, 0.02, 1, 0.02, 1, 0.02, 1])
    
    with c1:
        st.markdown("<div class='nav-btn'>".replace('\n', ''), unsafe_allow_html=True)
        if st.button(DIC[lang]["nav_lobby"], use_container_width=True, key=f"nav_lobby_{origen}"): st.session_state.estado = "lobby"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c2: st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>".replace('\n', ''), unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='nav-btn'>".replace('\n', ''), unsafe_allow_html=True)
        if st.button(DIC[lang]["nav_gremio"], use_container_width=True, key=f"nav_gremio_{origen}"): st.session_state.estado = "gremio"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c4: st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>".replace('\n', ''), unsafe_allow_html=True)
    with c5:
        st.markdown("<div class='nav-btn'>".replace('\n', ''), unsafe_allow_html=True)
        if st.button(DIC[lang]["nav_mundo"], use_container_width=True, key=f"nav_mundo_{origen}"): st.session_state.estado = "mundo"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c6: st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>".replace('\n', ''), unsafe_allow_html=True)
    with c7:
        st.markdown("<div class='nav-btn'>".replace('\n', ''), unsafe_allow_html=True)
        if st.button(DIC[lang]["nav_tienda"], use_container_width=True, key=f"nav_tienda_{origen}"): st.session_state.estado = "tienda"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c8: st.markdown("<div style='border-left: 2px solid #333; height: 100%; margin: auto;'></div>".replace('\n', ''), unsafe_allow_html=True)
    with c9:
        st.markdown("<div class='nav-btn'>".replace('\n', ''), unsafe_allow_html=True)
        if st.button(DIC[lang]["nav_cuartel"], use_container_width=True, key=f"nav_cuartel_{origen}"): st.session_state.estado = "cuartel"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
