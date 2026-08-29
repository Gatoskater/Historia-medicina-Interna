"""
Inyección de CSS para lograr un diseño elegante, minimalista, tipo firma
médica refinada: sidebar oscuro (slate/navy) + acentos teal + tipografía
Lora (serif, títulos) / Montserrat (sans, cuerpo).
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Montserrat:wght@400;500;600;700;800&display=swap');

:root {
    --accent: #0d9488;
    --accent-dark: #0f766e;
    --accent-light: #f0fdfa;
    --ink: #0f172a;
    --ink-soft: #334155;
    --paper: #f7f8fa;
}

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
}

h1, h2, h3, .serif {
    font-family: 'Lora', serif !important;
}

.stApp {
    background-color: var(--paper);
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #0b1120 100%);
    border-right: 1px solid #1e293b;
}
section[data-testid="stSidebar"] * {
    color: #cbd5e1;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}
section[data-testid="stSidebar"] .stButton button {
    background-color: transparent;
    border: 1px solid #1e293b;
    color: #cbd5e1;
    text-align: left;
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.86rem;
    transition: all 0.15s ease-in-out;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background-color: #1e293b;
    border-color: var(--accent);
    color: #ffffff;
}
section[data-testid="stSidebar"] .stProgress > div > div {
    background-color: var(--accent);
}

/* Botón de sección activa (marcado vía clase personalizada con markdown) */
.nav-activo button {
    background-color: #1e293b !important;
    border-left: 3px solid var(--accent) !important;
    color: #ffffff !important;
}

/* ---------- Encabezado principal ---------- */
.hc-header {
    padding: 1.6rem 0 1rem 0;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1.6rem;
}
.hc-header .kicker {
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--accent-dark);
}
.hc-header h1 {
    margin: 0.2rem 0 0.1rem 0;
    font-size: 1.9rem;
    color: var(--ink);
}
.hc-header p {
    color: var(--ink-soft);
    font-size: 0.92rem;
    margin: 0;
}

/* ---------- Tarjetas / contenedores ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px !important;
}

.guide-box {
    background-color: var(--accent-light);
    border-left: 4px solid var(--accent);
    padding: 0.9rem 1.1rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.85rem;
    color: var(--accent-dark);
    margin-bottom: 1.1rem;
    line-height: 1.5;
}

.section-title {
    font-family: 'Lora', serif;
    font-size: 1.35rem;
    color: var(--ink);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 0.4rem;
    margin-bottom: 1.1rem;
    display: inline-block;
}

/* ---------- Inputs ---------- */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"],
.stDateInput input, .stNumberInput input {
    border-radius: 8px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(13,148,136,0.15) !important;
}

/* Botones primarios */
.stButton button[kind="primary"], .stDownloadButton button {
    background-color: var(--accent);
    border: none;
    border-radius: 8px;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.stButton button[kind="primary"]:hover, .stDownloadButton button:hover {
    background-color: var(--accent-dark);
}

/* Métricas de progreso */
.progress-pill {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
}
.pill-completo { background-color: var(--accent); color: white; }
.pill-parcial { background-color: #facc15; color: #422006; }
.pill-vacio { background-color: #334155; color: #cbd5e1; }

footer, #MainMenu {visibility: hidden;}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)
