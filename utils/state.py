"""
Inicialización y utilidades del estado de sesión (st.session_state).
Toda la historia clínica vive en st.session_state["hc"], un diccionario anidado.
"""

import streamlit as st
from data.campos import REVISION_SISTEMAS, EXAMEN_FISICO_SISTEMAS

SECCIONES = [
    ("filiacion", "Datos de Filiación", "🪪"),
    ("consulta", "Motivo y Enfermedad Actual", "📝"),
    ("antecedentes", "Antecedentes Personales", "📚"),
    ("familiares", "Antecedentes Familiares", "👪"),
    ("habitos", "Hábitos Psicobiológicos", "🚬"),
    ("frcv", "Factores de Riesgo CV", "❤️‍🩹"),
    ("ros", "Revisión por Sistemas", "🔎"),
    ("examen", "Examen Físico", "🩺"),
    ("sintesis", "Síntesis Diagnóstica", "🧾"),
    ("vista_previa", "Vista Previa y PDF", "📄"),
]


def _estructura_inicial():
    return {
        "filiacion": {
            "nombres": "", "apellidos": "", "ci": "", "edad": "",
            "fecha_nacimiento": None, "sexo": "", "estado_civil": "",
            "religion": "", "raza": "", "dominancia": "",
            "lugar_nacimiento": "", "lugar_procedencia": "",
            "ocupacion": "", "telefono": "", "fecha_ingreso": None,
            "sala_cama": "",
            "contacto_nombre": "", "contacto_telefono": "",
            "contacto_parentesco": "", "contacto_direccion": "",
        },
        "consulta": {
            "motivo": "",
            "enfermedad_actual": "",
        },
        "antecedentes": {
            "enf_infancia_sel": [],
            "enf_infancia_otros": "",
            "enf_cronicas_sel": [],
            "enf_cronicas_otros": "",
            "quirurgicos": "",
            "traumatologicos": "",
            "alergicos": "",
            "ets_sel": [],
            "ets_otros": "",
            "transfusionales": "",
            "gineco_menarquia": "", "gineco_formula": "",
            "gineco_fur": "", "gineco_mac": "", "gineco_otros": "",
            "inmunologicos": "",
            "medicamentos": "",
            "epidemiologicos": "",
        },
        "familiares": {
            "filas": [],  # lista de dicts: parentesco, estado, edad, enfermedades
            "observaciones": "",
        },
        "habitos": {
            "tabaquico": "", "oh": "", "cafeico": "", "alimentario": "",
            "drogas": "", "actividad_fisica": "", "sueno": "",
            "sexuales": "", "estres": "",
        },
        "frcv": {
            "modificables_sel": [],
            "no_modificables_sel": [],
            "otros": "",
        },
        "ros": {s["key"]: {"sintomas": [], "detalles": ""} for s in REVISION_SISTEMAS},
        "examen": {
            "signos_vitales": {
                "temperatura": "", "pulso": "", "fr": "", "ta_sistolica": "",
                "ta_diastolica": "", "peso": "", "talla": "", "spo2": "",
                "llenado_capilar": "",
            },
            "sistemas": {
                s["key"]: {"estado": "No explorado", "anormales": [], "texto": ""}
                for s in EXAMEN_FISICO_SISTEMAS
            },
        },
        "sintesis": {
            "datos_positivos": "",
            "diagnosticos_sindromaticos": "",
            "observaciones": "",
            "diagnostico_definitivo": "",
            "plan": "",
        },
        "medico": {"nombre": "", "hospital": "", "servicio": ""},
    }


def init_state():
    if "hc" not in st.session_state:
        st.session_state["hc"] = _estructura_inicial()
    if "seccion_actual" not in st.session_state:
        st.session_state["seccion_actual"] = SECCIONES[0][0]


def reset_state():
    st.session_state["hc"] = _estructura_inicial()
    st.session_state["seccion_actual"] = SECCIONES[0][0]


def _lleno(v):
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, tuple, dict)):
        return len(v) > 0
    return bool(v)


def progreso_seccion(key):
    """Devuelve (llenos, total, porcentaje) heurístico por sección."""
    hc = st.session_state["hc"]
    if key == "filiacion":
        campos = ["nombres", "apellidos", "ci", "edad", "sexo", "fecha_ingreso"]
        llenos = sum(_lleno(hc["filiacion"].get(c)) for c in campos)
        return llenos, len(campos)
    if key == "consulta":
        campos = ["motivo", "enfermedad_actual"]
        llenos = sum(_lleno(hc["consulta"].get(c)) for c in campos)
        return llenos, len(campos)
    if key == "antecedentes":
        campos = ["quirurgicos", "traumatologicos", "alergicos",
                   "inmunologicos", "medicamentos", "epidemiologicos"]
        llenos = sum(_lleno(hc["antecedentes"].get(c)) for c in campos)
        llenos += 1 if (hc["antecedentes"]["enf_infancia_sel"] or hc["antecedentes"]["enf_cronicas_sel"]) else 0
        return llenos, len(campos) + 1
    if key == "familiares":
        return (1 if hc["familiares"]["filas"] else 0), 1
    if key == "habitos":
        campos = list(hc["habitos"].keys())
        llenos = sum(_lleno(hc["habitos"].get(c)) for c in campos)
        return llenos, len(campos)
    if key == "frcv":
        llenos = 1 if (hc["frcv"]["modificables_sel"] or hc["frcv"]["no_modificables_sel"]) else 0
        return llenos, 1
    if key == "ros":
        total = len(hc["ros"])
        llenos = sum(1 for v in hc["ros"].values() if _lleno(v["sintomas"]) or _lleno(v["detalles"]))
        return llenos, total
    if key == "examen":
        total = len(hc["examen"]["sistemas"])
        llenos = sum(1 for v in hc["examen"]["sistemas"].values() if v["estado"] != "No explorado")
        return llenos, total
    if key == "sintesis":
        campos = ["datos_positivos", "diagnosticos_sindromaticos", "diagnostico_definitivo"]
        llenos = sum(_lleno(hc["sintesis"].get(c)) for c in campos)
        return llenos, len(campos)
    return 0, 1


def progreso_global():
    total_pct = 0
    n = 0
    for key, _, _ in SECCIONES:
        if key == "vista_previa":
            continue
        llenos, total = progreso_seccion(key)
        total_pct += (llenos / total) if total else 0
        n += 1
    return round((total_pct / n) * 100) if n else 0
