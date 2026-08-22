from idiomas import DIC
import streamlit as st

def cargar_css():
    st.markdown("""
        <style>
        /* Importar fuente letal */
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
        
        * { font-family: 'Oswald', sans-serif !important; }

        /* EL MOTOR DE LEVITACIÓN */
        @keyframes flotar {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-12px); }
            100% { transform: translateY(0px); }
        }

        .carta-viva {
            background: linear-gradient(145deg, #161616, #0a0a0a);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            width: 160px;
            margin: 0 auto !important; /* ESTO CENTRA LA CARTA EN CUALQUIER PANTALLA O COLUMNA */
            animation: flotar 3s ease-in-out infinite;
            transition: box-shadow 0.3s ease;
        }
        
        .carta-viva:hover {
            box-shadow: 0 15px 30px rgba(255, 75, 75, 0.4);
            cursor: crosshair;
        }

        /* Títulos */
        .epic-title {
            text-align: center; color: #ffffff; font-size: 3.5rem;
            text-transform: uppercase; letter-spacing: 5px; margin-bottom: 0.5rem;
        }

        /* Ocultar basura de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)


def generar_carta_html(nombre, elo, icono, color, etiqueta, skin="default"):
    # Parámetros por defecto (Rango normal)
    color_borde = color
    color_texto = color
    sombra = "box-shadow: none;"
    fondo = "background: linear-gradient(145deg, #161616, #0a0a0a);"
    nombre_display = nombre

    # INYECCIÓN DE SKINS PREMIUM (Invaden toda la carta)
    if skin == "fuego": 
        color_borde = "#ff4b4b"
        color_texto = "#ff4b4b"
        sombra = "box-shadow: 0 0 25px rgba(255, 75, 75, 0.5), inset 0 0 20px rgba(255, 75, 75, 0.3);"
        fondo = "background: linear-gradient(145deg, #3a0808, #0a0a0a);" # Degradado rojo sangre
    elif skin == "sombra": 
        color_borde = "#8a2be2"
        color_texto = "#8a2be2"
        sombra = "box-shadow: 0 0 25px rgba(138, 43, 226, 0.5), inset 0 0 20px rgba(138, 43, 226, 0.3);"
        fondo = "background: linear-gradient(145deg, #1a083a, #0a0a0a);" # Degradado morado oscuro
    elif skin == "aura": 
        color_borde = "#00aaff"
        color_texto = "#00aaff"
        sombra = "box-shadow: 0 0 25px rgba(0, 170, 255, 0.5), inset 0 0 20px rgba(0, 170, 255, 0.3);"
        fondo = "background: linear-gradient(145deg, #08253a, #0a0a0a);" # Degradado azul eléctrico
    elif skin == "corona":
        # La corona respeta tu rango original, pero te da estatus de Rey
        sombra = "box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);" 
        nombre_display = f"👑 {nombre}"

    # Construcción del Estilo Final
    estilo_carta = f"border: 2px solid {color_borde}; {sombra} {fondo}"

    # El Avatar Elegante teñido del color de la skin
    svg_icono = f'''<svg width="45" height="45" viewBox="0 0 24 24" fill="none" stroke="{color_texto}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'''

    html = f"""
    <div class="carta-viva" style="{estilo_carta}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span style="color: {color_texto}; font-weight: bold; font-size: 14px;">{elo}</span>
            <span style="color: {color_texto}; font-size: 18px;">{icono}</span>
        </div>
        <div style="margin-bottom: 10px;">
            {svg_icono}
        </div>
        <h4 style="color: white; margin: 0; font-size: 15px; letter-spacing: 1px; text-transform: uppercase;">{nombre_display}</h4>
        <p style="color: #888; font-size: 10px; margin-top: 5px; letter-spacing: 1px;">{etiqueta}</p>
    </div>
    """
    return html.replace('\n', '')

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
        
