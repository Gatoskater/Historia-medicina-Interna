"""
Sistema visual v3 — temas seleccionables (Claro / Sepia / Oscuro), con el
dorado como acento constante en los tres (así siempre "combina"), más
ajustes para que la app se sienta bien en un teléfono, que es donde se
usará la mayoría del tiempo.

Nota técnica: el color "activo" de pills/segmented_control/toggle lo pone
Streamlit a partir de `primaryColor` en .streamlit/config.toml, y eso NO
se puede cambiar en tiempo real por sesión (solo al reiniciar el server).
Por eso primaryColor está fijado en dorado — coincide exactamente con "los
detalles dorados me encantan" y hace que ese acento sea consistente pase lo
que pase con el tema de fondo elegido aquí.
"""

import streamlit as st

TEMAS = {
    "claro": {
        "bg": "#faf8f4", "surface": "#ffffff", "surface_2": "#f7f4ee",
        "text": "#171a21", "text_soft": "#5b5f6b", "text_faint": "#9a9ea8",
        "heading": "#101a34", "line": "#e8e3d6",
        "sidebar_bg": "#fffdf9", "sidebar_line": "#ece6d8",
    },
    "sepia": {
        "bg": "#f1e6d3", "surface": "#faf3e4", "surface_2": "#ecdfc4",
        "text": "#3b2f1e", "text_soft": "#6b5a3f", "text_faint": "#9c8865",
        "heading": "#4a3520", "line": "#e0d0ab",
        "sidebar_bg": "#f6ecd9", "sidebar_line": "#dfcda3",
    },
    "oscuro": {
        "bg": "#11151f", "surface": "#1a2030", "surface_2": "#212840",
        "text": "#e8e3d6", "text_soft": "#a9a89e", "text_faint": "#787a86",
        "heading": "#f4e7c9", "line": "#2a3040",
        "sidebar_bg": "#161b28", "sidebar_line": "#262d40",
    },
}

GOLD = "#b0894f"
GOLD_DEEP = "#8f6d3a"
GOLD_TINT_CLARO = "#f6efe0"
NAVY = "#101a34"
NAVY_2 = "#17223f"


def _gold_tint(tema_key):
    # En oscuro, el "tinte dorado" de fondo debe ser sutil sobre superficie oscura.
    return "rgba(176,137,79,0.16)" if tema_key == "oscuro" else GOLD_TINT_CLARO


def css_para_tema(tema_key: str) -> str:
    t = TEMAS.get(tema_key, TEMAS["claro"])
    gold_tint = _gold_tint(tema_key)
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --navy: {NAVY};
    --navy-2: {NAVY_2};
    --gold: {GOLD};
    --gold-deep: {GOLD_DEEP};
    --gold-tint: {gold_tint};
    --ink: {t["text"]};
    --ink-soft: {t["text_soft"]};
    --ink-faint: {t["text_faint"]};
    --bg: {t["bg"]};
    --surface: {t["surface"]};
    --surface-2: {t["surface_2"]};
    --line: {t["line"]};
    --heading: {t["heading"]};
    --radius: 14px;
}}

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
h1, h2, h3, .serif {{ font-family: 'Playfair Display', serif !important; }}

.stApp {{ background-color: var(--bg); }}
[data-testid="stMainBlockContainer"] {{ padding-top: 1.1rem; max-width: 1100px; }}
[data-testid="stAppViewContainer"] * {{ color: var(--ink); }}

/* ============ SIDEBAR — combina con el tema elegido ============ */
section[data-testid="stSidebar"] {{
    background: {t["sidebar_bg"]};
    border-right: 1px solid {t["sidebar_line"]};
}}
section[data-testid="stSidebar"] * {{ color: var(--ink) !important; }}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
    color: var(--heading) !important;
}}

section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {{
    background-color: transparent;
    border: 1px solid transparent;
    color: var(--ink-soft) !important;
    text-align: left; justify-content: flex-start;
    border-radius: 9px; font-weight: 500; font-size: 0.85rem;
    padding: 0.55rem 0.7rem; min-height: 2.6rem;
    transition: background-color 0.15s ease, transform 0.1s ease;
}}
section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {{
    background-color: var(--gold-tint); transform: translateX(2px);
}}
section[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {{
    background-color: var(--gold-tint) !important;
    border: 1px solid var(--gold) !important;
    color: var(--heading) !important;
    text-align: left; justify-content: flex-start;
    border-radius: 9px; font-weight: 700; font-size: 0.85rem;
    padding: 0.55rem 0.7rem; min-height: 2.6rem;
    box-shadow: inset 3px 0 0 var(--gold);
}}
section[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p {{ color: var(--heading) !important; }}

.sidebar-brand {{ padding: 0.3rem 0 1rem 0; border-bottom: 1px solid var(--line); margin-bottom: 0.9rem; }}
.sidebar-brand .mark {{ font-family:'Playfair Display', serif; font-weight:700; font-size:1.28rem; color: var(--heading); line-height:1.2; }}
.sidebar-brand .sub {{ font-family:'Playfair Display', serif; font-style: italic; font-size:0.92rem; color: var(--gold-deep); }}

.sidebar-footer {{
    margin-top: 1.2rem; padding-top: 0.8rem; border-top: 1px solid var(--line);
    font-size: 0.7rem; color: var(--ink-faint); text-align: center; font-style: italic;
    font-family: 'Playfair Display', serif;
}}
.sidebar-footer b {{ color: var(--gold-deep); font-style: normal; }}

/* ============ MASTHEAD ============ */
.masthead {{
    background: linear-gradient(120deg, var(--navy) 0%, var(--navy-2) 100%);
    border-radius: var(--radius); padding: 1.1rem 1.4rem; margin-bottom: 1rem;
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;
    box-shadow: 0 10px 28px rgba(16,26,52,0.18);
}}
.masthead .mh-title {{ font-family:'Playfair Display', serif; font-weight:700; font-size:1.35rem; color:#fdfaf4; }}
.masthead .mh-sub {{ font-family:'Playfair Display', serif; font-style:italic; font-size:0.88rem; color: #d8c8a8; margin-top:0.05rem; }}
.masthead .mh-credit {{
    font-size: 0.64rem; text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--navy); background: var(--gold); padding: 0.3rem 0.65rem;
    border-radius: 999px; font-weight: 700; white-space: nowrap;
}}

.progress-capsule-track {{ background: var(--line); border-radius: 999px; height: 8px; overflow: hidden; margin: 0 0 1.2rem 0; }}
.progress-capsule-fill {{ height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--navy) 0%, var(--gold) 100%); transition: width 0.4s ease; }}

/* ============ Encabezado de sección ============ */
.hc-header {{ padding: 0.15rem 0 0.9rem 0; margin-bottom: 0.5rem; }}
.hc-header .kicker {{ text-transform: uppercase; letter-spacing: 0.15em; font-size: 0.66rem; font-weight: 700; color: var(--gold-deep); }}
.hc-header h1 {{ margin: 0.15rem 0 0.15rem 0; font-size: 1.55rem; color: var(--heading); font-weight: 700; }}
.hc-header p {{ color: var(--ink-soft); font-size: 0.88rem; margin: 0; }}

.section-title {{
    font-family: 'Playfair Display', serif; font-weight: 600; font-size: 1.12rem;
    color: var(--heading); border-bottom: 2px solid var(--gold); padding-bottom: 0.32rem;
    margin: 1rem 0 0.85rem 0; display: inline-block;
}}

/* ============ Tarjetas / contenedores ============ */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius: var(--radius) !important; border-color: var(--line) !important;
    background: var(--surface); transition: box-shadow 0.2s ease;
}}

[data-testid="stExpander"] {{
    border: 1px solid var(--line) !important; border-radius: var(--radius) !important;
    background: var(--surface); overflow: hidden;
}}
[data-testid="stExpander"] summary {{ font-weight: 600; color: var(--heading); min-height: 2.8rem; }}
[data-testid="stExpander"] summary:hover {{ color: var(--gold-deep); }}

[data-testid="stPopoverButton"] {{
    border-radius: 999px !important; font-size: 0.78rem !important;
    border-color: var(--gold) !important; color: var(--gold-deep) !important;
    min-height: 2.4rem;
}}
[data-testid="stPopoverBody"] {{ border-radius: var(--radius) !important; border-color: var(--line) !important; font-size: 0.86rem; background: var(--surface); }}

/* ============ Inputs — 16px min para evitar zoom automático en iOS ============ */
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {{
    border-radius: 9px !important; border-color: var(--line) !important;
    background: var(--surface) !important; color: var(--ink) !important;
    font-size: 16px !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {{
    border-color: var(--gold) !important; box-shadow: 0 0 0 2px var(--gold-tint) !important;
}}
[data-testid="stWidgetLabel"] p {{ font-weight: 500; color: var(--ink); font-size: 0.88rem; }}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{ background: var(--surface) !important; border-color: var(--line) !important; min-height: 2.6rem; }}

/* ============ Botones — tamaño cómodo para dedo (min 44px) ============ */
[data-testid="stBaseButton-primary"] {{
    background-color: var(--navy) !important; border: 1px solid var(--navy) !important;
    color: var(--gold-tint) !important; border-radius: 9px !important; font-weight: 600 !important;
    min-height: 2.75rem; transition: transform 0.12s ease;
}}
[data-testid="stBaseButton-primary"] p {{ color: #fdfaf4 !important; }}
[data-testid="stBaseButton-primary"]:active {{ transform: scale(0.98); }}

[data-testid="stBaseButton-secondary"] {{
    border-radius: 9px !important; border-color: var(--line) !important; color: var(--ink) !important;
    font-weight: 500 !important; min-height: 2.75rem; background: var(--surface) !important;
}}
[data-testid="stBaseButton-secondary"]:hover {{ border-color: var(--gold) !important; }}
[data-testid="stBaseButton-secondary"]:active {{ transform: scale(0.98); }}

[data-testid="stDownloadButton"] [data-testid="stBaseButton-primary"] {{ background-color: var(--gold-deep) !important; border-color: var(--gold-deep) !important; }}

[data-testid="stButtonGroup"] {{ gap: 0.35rem; }}
[data-testid="stButtonGroup"] label {{ min-height: 2.4rem; }}

.progress-pill {{ display: inline-block; padding: 0.15rem 0.6rem; border-radius: 999px; font-size: 0.66rem; font-weight: 700; }}
.pill-completo {{ background-color: var(--navy); color: var(--gold-tint); }}
.pill-parcial {{ background-color: var(--gold-tint); color: var(--gold-deep); border: 1px solid var(--gold); }}
.pill-vacio {{ background-color: var(--line); color: var(--ink-faint); }}

[data-testid="stMetric"] {{ background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 0.65rem 0.85rem; }}
[data-testid="stMetricLabel"] {{ color: var(--ink-soft) !important; }}
[data-testid="stMetricValue"] {{ color: var(--heading) !important; font-family: 'Playfair Display', serif; }}

.mini-guia {{ font-size: 0.78rem; color: var(--ink-faint); font-style: italic; margin: -0.3rem 0 0.7rem 0; }}

footer, #MainMenu, [data-testid="stToolbar"] {{ visibility: hidden; height: 0; }}

/* ============ MÓVIL ============ */
@media (max-width: 640px) {{
    [data-testid="stMainBlockContainer"] {{ padding-left: 0.9rem !important; padding-right: 0.9rem !important; padding-top: 0.6rem !important; }}
    .masthead {{ padding: 0.85rem 1rem; border-radius: 10px; }}
    .masthead .mh-title {{ font-size: 1.12rem; }}
    .masthead .mh-sub {{ font-size: 0.78rem; }}
    .masthead .mh-credit {{ font-size: 0.58rem; padding: 0.25rem 0.55rem; }}
    .hc-header h1 {{ font-size: 1.28rem; }}
    .hc-header p {{ font-size: 0.82rem; }}
    .section-title {{ font-size: 1rem; }}
    [data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"] {{ width: 100%; }}
    [data-testid="stExpander"] summary {{ font-size: 0.92rem; }}
    div[data-testid="stHorizontalBlock"] {{ gap: 0.5rem; }}
}}
</style>
"""


def inject_css():
    tema = st.session_state.get("tema", "claro")
    st.markdown(css_para_tema(tema), unsafe_allow_html=True)


def selector_tema():
    opciones = {"claro": "☀️ Claro", "sepia": "📜 Sepia", "oscuro": "🌙 Oscuro"}
    actual = st.session_state.get("tema", "claro")
    seleccion = st.segmented_control(
        "Tema", list(opciones.values()),
        default=opciones[actual], key="selector_tema_widget", label_visibility="collapsed",
    )
    inv = {v: k for k, v in opciones.items()}
    nuevo = inv.get(seleccion, "claro")
    if nuevo != actual:
        st.session_state["tema"] = nuevo
        st.rerun()


def masthead_html(credit_name: str, subtitle: str = "Medicina Interna"):
    return f"""
    <div class="masthead">
        <div>
            <div class="mh-title">Historia Clínica</div>
            <div class="mh-sub">{subtitle}</div>
        </div>
        <div class="mh-credit">Por {credit_name}</div>
    </div>
    """


def progress_capsule_html(pct: int):
    return f"""
    <div class="progress-capsule-track">
        <div class="progress-capsule-fill" style="width:{pct}%;"></div>
    </div>
    """
