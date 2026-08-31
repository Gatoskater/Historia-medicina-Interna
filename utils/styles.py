"""
Sistema visual v2 — identidad "consultora médica refinada".
Paleta navy + oro sobre fondo marfil, tipografía Playfair Display (serif,
títulos) + Inter (sans, UI). Sidebar clara (deliberadamente distinta de la
v1, que era oscura). Selectores verificados contra el bundle real de esta
versión de Streamlit (data-testid) para evitar reglas CSS que no aplican.
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --navy: #101a34;
    --navy-2: #17223f;
    --gold: #b0894f;
    --gold-deep: #8f6d3a;
    --gold-tint: #f6efe0;
    --ink: #171a21;
    --ink-soft: #5b5f6b;
    --ink-faint: #8b8f99;
    --bg: #faf8f4;
    --surface: #ffffff;
    --line: #e8e3d6;
    --radius: 14px;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3, .serif { font-family: 'Playfair Display', serif !important; }

.stApp { background-color: var(--bg); }
[data-testid="stMainBlockContainer"] { padding-top: 1.2rem; max-width: 1100px; }

/* ============ SIDEBAR — clara, refinada, distinta de la v1 ============ */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--line);
    box-shadow: 2px 0 14px rgba(16,26,52,0.03);
}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding-top: 0.4rem; }
section[data-testid="stSidebar"] * { color: var(--ink); }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color: var(--navy) !important;
}

/* Botones de navegación (secondary = ítem de menú en reposo) */
section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background-color: transparent;
    border: 1px solid transparent;
    color: var(--ink-soft);
    text-align: left;
    justify-content: flex-start;
    border-radius: 9px;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.5rem 0.7rem;
    transition: background-color 0.15s ease, color 0.15s ease, transform 0.1s ease;
}
section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
    background-color: var(--gold-tint);
    color: var(--navy);
    transform: translateX(2px);
}
/* Ítem activo (primary) — pastilla dorada tenue, texto navy en negrita */
section[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
    background-color: var(--gold-tint) !important;
    border: 1px solid var(--gold) !important;
    color: var(--navy) !important;
    text-align: left;
    justify-content: flex-start;
    border-radius: 9px;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 0.5rem 0.7rem;
    box-shadow: inset 3px 0 0 var(--gold);
}
section[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p { color: var(--navy) !important; }

.sidebar-brand {
    padding: 0.3rem 0 1rem 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: 0.9rem;
}
.sidebar-brand .mark { font-family:'Playfair Display', serif; font-weight:700; font-size:1.32rem; color: var(--navy); line-height:1.2; }
.sidebar-brand .sub { font-family:'Playfair Display', serif; font-style: italic; font-size:0.95rem; color: var(--gold-deep); }

.sidebar-footer {
    margin-top: 1.4rem; padding-top: 0.9rem; border-top: 1px solid var(--line);
    font-size: 0.72rem; color: var(--ink-faint); text-align: center; font-style: italic;
    font-family: 'Playfair Display', serif;
}
.sidebar-footer b { color: var(--gold-deep); font-style: normal; }

/* ============ MASTHEAD — banda navy decorativa arriba del contenido ============ */
.masthead {
    background: linear-gradient(120deg, var(--navy) 0%, var(--navy-2) 100%);
    border-radius: var(--radius);
    padding: 1.35rem 1.7rem;
    margin-bottom: 1.1rem;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 10px 28px rgba(16,26,52,0.16);
}
.masthead .mh-title { font-family:'Playfair Display', serif; font-weight:700; font-size:1.5rem; color:#fdfaf4; letter-spacing:0.01em; }
.masthead .mh-sub { font-family:'Playfair Display', serif; font-style:italic; font-size:0.95rem; color: #d8c8a8; margin-top:0.1rem; }
.masthead .mh-credit {
    font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.12em;
    color: var(--navy); background: var(--gold); padding: 0.32rem 0.7rem;
    border-radius: 999px; font-weight: 700; white-space: nowrap;
}

/* Cápsula de progreso general */
.progress-capsule-track { background: var(--line); border-radius: 999px; height: 8px; overflow: hidden; margin: 0 0 1.3rem 0; }
.progress-capsule-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--navy) 0%, var(--gold) 100%); transition: width 0.4s ease; }

/* ============ Encabezado de sección ============ */
.hc-header { padding: 0.2rem 0 1rem 0; margin-bottom: 0.6rem; }
.hc-header .kicker { text-transform: uppercase; letter-spacing: 0.16em; font-size: 0.68rem; font-weight: 700; color: var(--gold-deep); }
.hc-header h1 { margin: 0.15rem 0 0.15rem 0; font-size: 1.7rem; color: var(--navy); font-weight: 700; }
.hc-header p { color: var(--ink-soft); font-size: 0.9rem; margin: 0; }

.section-title {
    font-family: 'Playfair Display', serif; font-weight: 600; font-size: 1.18rem;
    color: var(--navy); border-bottom: 2px solid var(--gold); padding-bottom: 0.35rem;
    margin: 1.1rem 0 0.9rem 0; display: inline-block;
}

/* ============ Tarjetas / contenedores con borde ============ */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: var(--radius) !important;
    border-color: var(--line) !important;
    background: var(--surface);
    transition: box-shadow 0.2s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover { box-shadow: 0 6px 18px rgba(16,26,52,0.06); }

/* ============ Expanders ============ */
[data-testid="stExpander"] {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius) !important;
    background: var(--surface);
    overflow: hidden;
}
[data-testid="stExpander"] summary { font-weight: 600; color: var(--navy); }
[data-testid="stExpander"] summary:hover { color: var(--gold-deep); }

/* ============ Popover (guías "¿Qué preguntar aquí?") ============ */
[data-testid="stPopoverButton"] {
    border-radius: 999px !important;
    font-size: 0.78rem !important;
    border-color: var(--gold) !important;
    color: var(--gold-deep) !important;
}
[data-testid="stPopoverBody"] {
    border-radius: var(--radius) !important;
    border-color: var(--line) !important;
    font-size: 0.86rem;
}

/* ============ Inputs ============ */
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
    border-radius: 9px !important;
    border-color: var(--line) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(176,137,79,0.18) !important;
}
[data-testid="stWidgetLabel"] p { font-weight: 500; color: var(--ink); font-size: 0.88rem; }

/* ============ Botones fuera del sidebar ============ */
[data-testid="stBaseButton-primary"] {
    background-color: var(--navy) !important;
    border: 1px solid var(--navy) !important;
    color: var(--gold-tint) !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    transition: transform 0.12s ease, box-shadow 0.12s ease;
}
[data-testid="stBaseButton-primary"] p { color: var(--gold-tint) !important; }
[data-testid="stBaseButton-primary"]:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(16,26,52,0.22); }

[data-testid="stBaseButton-secondary"] {
    border-radius: 9px !important;
    border-color: var(--line) !important;
    color: var(--navy) !important;
    font-weight: 500 !important;
    transition: border-color 0.12s ease, transform 0.12s ease;
}
[data-testid="stBaseButton-secondary"]:hover { border-color: var(--gold) !important; transform: translateY(-1px); }

[data-testid="stDownloadButton"] [data-testid="stBaseButton-primary"] { background-color: var(--gold-deep) !important; border-color: var(--gold-deep) !important; }

/* ============ Pills / Segmented control — el color activo lo pone el theme (primaryColor = oro) ============ */
[data-testid="stButtonGroup"] { gap: 0.35rem; }

/* ============ Badges de progreso caseros ============ */
.progress-pill { display: inline-block; padding: 0.15rem 0.6rem; border-radius: 999px; font-size: 0.66rem; font-weight: 700; letter-spacing: 0.02em; }
.pill-completo { background-color: var(--navy); color: var(--gold-tint); }
.pill-parcial { background-color: var(--gold-tint); color: var(--gold-deep); border: 1px solid var(--gold); }
.pill-vacio { background-color: var(--line); color: var(--ink-faint); }

/* ============ Métricas nativas ============ */
[data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 0.7rem 0.9rem; }
[data-testid="stMetricLabel"] { color: var(--ink-soft) !important; }
[data-testid="stMetricValue"] { color: var(--navy) !important; font-family: 'Playfair Display', serif; }

/* ============ Guía discreta (texto de apoyo, no intrusivo) ============ */
.mini-guia { font-size: 0.78rem; color: var(--ink-faint); font-style: italic; margin: -0.4rem 0 0.7rem 0; }

footer, #MainMenu, [data-testid="stToolbar"] { visibility: hidden; height: 0; }
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)


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
