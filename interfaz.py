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
            /* Aquí está la vida: 3 segundos, infinito, suave */
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
    # Aplicamos los bordes y auras según el mercado negro
    borde_skin = f"border: 2px solid {color};"
    if skin == "fuego": borde_skin = f"border: 2px solid {color}; box-shadow: 0 0 15px #ff4b4b, inset 0 0 10px #ff4b4b;"
    elif skin == "sombra": borde_skin = f"border: 2px solid {color}; box-shadow: 0 0 15px #8a2be2, inset 0 0 10px #8a2be2;"
    elif skin == "aura": borde_skin = f"border: 2px solid {color}; box-shadow: 0 0 20px #00aaff, inset 0 0 15px #00aaff;"
    elif skin == "corona": borde_skin = f"border: 2px solid #ffd700; box-shadow: 0 0 25px #ffd700, inset 0 0 15px #ffd700;"

    html = f"""
    <div class="carta-viva" style="{borde_skin}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span style="color: {color}; font-weight: bold; font-size: 14px;">{elo}</span>
            <span style="color: {color}; font-size: 18px;">{icono}</span>
        </div>
        <div style="font-size: 40px; margin-bottom: 10px; color: #fff;">👤</div>
        <h4 style="color: white; margin: 0; font-size: 16px; letter-spacing: 1px; text-transform: uppercase;">{nombre}</h4>
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
        
