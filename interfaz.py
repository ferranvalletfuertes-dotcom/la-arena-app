from idiomas import DIC
import streamlit as st

def cargar_css():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .stButton > button[data-baseweb="button"] {
            background-color: #ff4b4b; color: white; border-radius: 8px; border: none;
            padding: 10px 24px; font-weight: 900; letter-spacing: 1px; text-transform: uppercase;
            transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(255, 75, 75, 0.2);
        }
        .stButton > button[data-baseweb="button"]:hover {
            background-color: #ff1a1a; box-shadow: 0 0 20px rgba(255, 75, 75, 0.6); transform: scale(1.02);
        }
        .nav-btn > button[data-baseweb="button"] {
            background-color: #1a1a1a !important; border: 1px solid #333 !important;
            color: #888 !important; box-shadow: none !important; padding: 5px !important;
        }
        .nav-btn > button[data-baseweb="button"]:hover {
            color: #fff !important; border-color: #ff4b4b !important; 
            background-color: #222 !important; transform: none !important;
        }
        div[data-testid="stExpander"] { background-color: #161616; border: 1px solid #333; border-radius: 8px; }
        
        .epic-title { color: #ff4b4b; font-size: 3.5em; text-transform: uppercase; letter-spacing: 4px; text-shadow: 0 0 25px rgba(255,75,75,0.7); margin-bottom: 0px; }
        .manifesto { color: #a3a3a3; font-size: 1.1em; font-style: italic; margin-top: 10px; line-height: 1.6; }
        .highlight { color: #ffffff; font-weight: bold; text-shadow: 0 0 5px rgba(255,255,255,0.3); }
        .stTextInput > div > div > input { background-color: #111 !important; color: #00ff00 !important; border: 1px solid #333 !important; font-family: monospace; text-align: center; font-weight: bold; }
        .neon-red { color: #ff4b4b; text-shadow: 0 0 10px rgba(255, 75, 75, 0.8); font-weight: 900; }
        .neon-green { color: #00ff00; text-shadow: 0 0 10px rgba(0, 255, 0, 0.8); font-weight: 900; }
        .rules-box { border: 1px solid #ff4b4b; background-color: #110000; padding: 20px; border-radius: 8px; box-shadow: 0 0 20px rgba(255, 75, 75, 0.3); margin-top: 25px; margin-bottom: 25px; }

        @keyframes float-card { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
        @keyframes rank-up-pop { 0% { transform: scale(0.5); opacity: 0; } 70% { transform: scale(1.05); opacity: 1; } 100% { transform: scale(1); opacity: 1; } }
        @keyframes breathe-logo { 0% { transform: translateY(0px) scale(1); box-shadow: 0 0 15px #ff4b4b; } 50% { transform: translateY(-8px) scale(1.02); box-shadow: 0 0 35px #ff0000; } 100% { transform: translateY(0px) scale(1); box-shadow: 0 0 15px #ff4b4b; } }
        .logo-breathe { border-radius: 15px; animation: breathe-logo 3.5s ease-in-out infinite; }
        
        @keyframes glitch { 0% { text-shadow: 2px 0 0 #ff4b4b, -2px 0 0 #00ffff; } 5% { text-shadow: -2px 0 0 #ff4b4b, 2px 0 0 #00ffff; } 10% { text-shadow: 2px 0 0 #ff4b4b, -2px 0 0 #00ffff; } 15% { text-shadow: -2px 0 0 #ff4b4b, 2px 0 0 #00ffff; } 20% { text-shadow: none; } 100% { text-shadow: none; } }
        .glitch-text { animation: glitch 2.5s infinite; color: white; font-family: monospace; text-align: center; letter-spacing: 2px; }

        .fut-card { transition: filter 0.3s ease; }
        .fut-card:hover { filter: brightness(1.2); cursor: pointer; }
        .anim-float { animation: float-card 3.5s ease-in-out infinite; }
        .anim-aura { animation: float-card 3.5s ease-in-out infinite; border: 2px solid #ff0000 !important; box-shadow: 0 0 15px #ff0000, 0 0 5px #ff0000 inset !important; }
        .anim-fuego { animation: float-card 3.5s ease-in-out infinite; border: 2px solid #aa00ff !important; box-shadow: 0 0 15px #aa00ff, 0 0 5px #aa00ff inset !important; }
        .anim-sombra { animation: float-card 3.5s ease-in-out infinite; border: 2px solid #00aaff !important; box-shadow: 0 0 15px #00aaff, 0 0 5px #00aaff inset !important; }

        @keyframes chest-shake { 0% { transform: translate(1px, 1px) rotate(0deg); } 10% { transform: translate(-1px, -2px) rotate(-1deg); } 20% { transform: translate(-3px, 0px) rotate(1deg); } 30% { transform: translate(3px, 2px) rotate(0deg); } 40% { transform: translate(1px, -1px) rotate(1deg); } 50% { transform: translate(-1px, 2px) rotate(-1deg); } 60% { transform: translate(-3px, 1px) rotate(0deg); } 70% { transform: translate(3px, 1px) rotate(-1deg); } 80% { transform: translate(-1px, -1px) rotate(1deg); } 90% { transform: translate(1px, 2px) rotate(0deg); } 100% { transform: translate(1px, -2px) rotate(-1deg); } }
        .chest-anim { font-size: 100px; animation: chest-shake 0.5s infinite; text-align: center; margin: 20px 0; text-shadow: 0 0 30px #ffd700; }
        
        .feed-box::-webkit-scrollbar { display: none; }
        .feed-box { -ms-overflow-style: none; scrollbar-width: none; }
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
        
