import streamlit as st
from datetime import date

from utils.styles import inject_css
from utils.state import init_state, reset_state, SECCIONES, progreso_seccion, progreso_global
from utils.pdf_export import generar_pdf
from data.campos import (
    ENF_INFANCIA, ENF_CRONICAS_ADULTO, ETS, PARENTESCOS_FAMILIARES,
    ENF_FAMILIARES_FRECUENTES, FRCV_MODIFICABLES, FRCV_NO_MODIFICABLES,
    REVISION_SISTEMAS, EXAMEN_FISICO_SISTEMAS, DIAGNOSTICOS_SINDROMATICOS_SUGERIDOS,
)

st.set_page_config(
    page_title="Historia Clínica | Medicina Interna",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_state()
hc = st.session_state["hc"]


# ============================================================
# SIDEBAR — navegación
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 0.4rem 0 1rem 0; border-bottom:1px solid #1e293b;">
            <div style="font-family:'Lora',serif; font-size:1.4rem; color:#fff; line-height:1.25;">
                Historia Clínica<br><span style="font-size:1.05rem; color:#2dd4bf; font-style:italic;">Medicina Interna</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pct = progreso_global()
    st.markdown(f"<div style='font-size:0.7rem; letter-spacing:0.08em; text-transform:uppercase; color:#94a3b8; margin-top:0.9rem;'>Progreso general — {pct}%</div>", unsafe_allow_html=True)
    st.progress(pct / 100)
    st.write("")

    for key, label, icono in SECCIONES:
        if key == "vista_previa":
            continue
        llenos, total = progreso_seccion(key)
        badge = "✓" if llenos == total and total > 0 else (f"{llenos}/{total}" if llenos else "")
        activo = st.session_state["seccion_actual"] == key
        etiqueta_btn = f"{icono}  {label}   {badge}".rstrip()
        if st.button(etiqueta_btn, key=f"nav_{key}", use_container_width=True,
                     type="primary" if activo else "secondary"):
            st.session_state["seccion_actual"] = key
            st.rerun()

    st.markdown("<div style='border-top:1px solid #1e293b; margin: 0.8rem 0;'></div>", unsafe_allow_html=True)
    if st.button("📄  Vista Previa y PDF", key="nav_preview", use_container_width=True,
                 type="primary" if st.session_state["seccion_actual"] == "vista_previa" else "secondary"):
        st.session_state["seccion_actual"] = "vista_previa"
        st.rerun()

    st.write("")
    with st.expander("⚙️ Datos del médico / institución"):
        hc["medico"]["nombre"] = st.text_input("Nombre del estudiante/médico", value=hc["medico"]["nombre"])
        hc["medico"]["hospital"] = st.text_input("Institución / Hospital", value=hc["medico"]["hospital"])
        hc["medico"]["servicio"] = st.text_input("Servicio", value=hc["medico"]["servicio"])

    if st.button("🗑️ Nueva historia (borrar todo)", use_container_width=True):
        st.session_state["confirmar_reset"] = True

    if st.session_state.get("confirmar_reset"):
        st.warning("¿Seguro? Esta acción borra todos los datos.")
        c1, c2 = st.columns(2)
        if c1.button("Sí, borrar", use_container_width=True):
            reset_state()
            st.session_state["confirmar_reset"] = False
            st.rerun()
        if c2.button("Cancelar", use_container_width=True):
            st.session_state["confirmar_reset"] = False
            st.rerun()


def header(kicker, titulo, subtitulo):
    st.markdown(
        f"""
        <div class="hc-header">
            <div class="kicker">{kicker}</div>
            <h1>{titulo}</h1>
            <p>{subtitulo}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def guia(texto):
    st.markdown(f"<div class='guide-box'>💡 {texto}</div>", unsafe_allow_html=True)


seccion = st.session_state["seccion_actual"]

# ============================================================
# 1. DATOS DE FILIACIÓN
# ============================================================
if seccion == "filiacion":
    header("Sección 1", "Datos de Filiación", "Identificación del paciente y contacto de emergencia.")
    fil = hc["filiacion"]

    c1, c2, c3 = st.columns(3)
    fil["nombres"] = c1.text_input("Nombres", value=fil["nombres"])
    fil["apellidos"] = c2.text_input("Apellidos", value=fil["apellidos"])
    fil["ci"] = c3.text_input("Cédula de Identidad", value=fil["ci"])

    c1, c2, c3 = st.columns(3)
    fil["edad"] = c1.text_input("Edad", value=fil["edad"])
    fil["fecha_nacimiento"] = c2.date_input("Fecha de nacimiento", value=fil["fecha_nacimiento"],
                                             min_value=date(1900, 1, 1), max_value=date.today())
    fil["sexo"] = c3.selectbox("Sexo", ["", "Masculino", "Femenino"],
                                index=["", "Masculino", "Femenino"].index(fil["sexo"]) if fil["sexo"] in ["", "Masculino", "Femenino"] else 0)

    c1, c2, c3 = st.columns(3)
    fil["estado_civil"] = c1.selectbox("Estado civil", ["", "Soltero(a)", "Casado(a)", "Divorciado(a)", "Viudo(a)", "Unión estable"],
                                        index=0 if fil["estado_civil"] == "" else ["", "Soltero(a)", "Casado(a)", "Divorciado(a)", "Viudo(a)", "Unión estable"].index(fil["estado_civil"]))
    fil["religion"] = c2.text_input("Religión", value=fil["religion"])
    fil["raza"] = c3.text_input("Raza / autoidentificación étnica", value=fil["raza"])

    c1, c2, c3 = st.columns(3)
    fil["dominancia"] = c1.selectbox("Dominancia", ["", "Diestro(a)", "Zurdo(a)", "Ambidiestro(a)"],
                                      index=0 if fil["dominancia"] == "" else ["", "Diestro(a)", "Zurdo(a)", "Ambidiestro(a)"].index(fil["dominancia"]))
    fil["lugar_nacimiento"] = c2.text_input("Lugar de nacimiento", value=fil["lugar_nacimiento"])
    fil["lugar_procedencia"] = c3.text_input("Lugar de procedencia", value=fil["lugar_procedencia"])

    c1, c2, c3 = st.columns(3)
    fil["ocupacion"] = c1.text_input("Ocupación", value=fil["ocupacion"])
    fil["telefono"] = c2.text_input("Teléfono", value=fil["telefono"])
    fil["sala_cama"] = c3.text_input("Sala / Cama", value=fil["sala_cama"])

    fil["fecha_ingreso"] = st.date_input("Fecha de ingreso", value=fil["fecha_ingreso"],
                                          min_value=date(1900, 1, 1), max_value=date.today())

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Contacto de emergencia</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    fil["contacto_nombre"] = c1.text_input("Nombre completo", value=fil["contacto_nombre"])
    fil["contacto_telefono"] = c2.text_input("Teléfono", value=fil["contacto_telefono"], key="contacto_tel")
    c1, c2 = st.columns(2)
    fil["contacto_parentesco"] = c1.text_input("Parentesco", value=fil["contacto_parentesco"])
    fil["contacto_direccion"] = c2.text_input("Dirección", value=fil["contacto_direccion"])

# ============================================================
# 2. MOTIVO Y ENFERMEDAD ACTUAL
# ============================================================
elif seccion == "consulta":
    header("Sección 2", "Motivo de Consulta y Enfermedad Actual", "El relato debe ser conciso, cronológico y completo.")
    con = hc["consulta"]
    guia("Registra el motivo tal cual lo expresa el paciente, entre comillas. Para la enfermedad actual: inicio, características del síntoma principal, evolución, síntomas asociados, y qué lo llevó a consultar.")
    con["motivo"] = st.text_input('Motivo de consulta (entre comillas, en palabras del paciente)', value=con["motivo"])
    con["enfermedad_actual"] = st.text_area("Enfermedad actual", value=con["enfermedad_actual"], height=280,
                                             placeholder="Paciente masculino/femenino de X años, natural y procedente de..., conocido/no conocido por..., que refiere inicio de enfermedad actual...")

# ============================================================
# 3. ANTECEDENTES PERSONALES
# ============================================================
elif seccion == "antecedentes":
    header("Sección 3", "Antecedentes Personales", "Recorre cada bloque; marca lo positivo y detalla en el campo de texto.")
    ant = hc["antecedentes"]

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Médicos — Infancia</div>", unsafe_allow_html=True)
    ant["enf_infancia_sel"] = st.multiselect("Enfermedades de la infancia", ENF_INFANCIA, default=ant["enf_infancia_sel"])
    ant["enf_infancia_otros"] = st.text_input("Otros detalles (infancia)", value=ant["enf_infancia_otros"])

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Médicos — Adultez</div>", unsafe_allow_html=True)
    ant["enf_cronicas_sel"] = st.multiselect("Enfermedades crónicas conocidas", ENF_CRONICAS_ADULTO, default=ant["enf_cronicas_sel"])
    ant["enf_cronicas_otros"] = st.text_area("Detalle (diagnóstico, año, tratamiento)", value=ant["enf_cronicas_otros"], height=90)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title' style='font-size:1.05rem;'>Quirúrgicos</div>", unsafe_allow_html=True)
        ant["quirurgicos"] = st.text_area("Cirugías previas (tipo, año, complicaciones)", value=ant["quirurgicos"], height=110, label_visibility="collapsed")
    with c2:
        st.markdown("<div class='section-title' style='font-size:1.05rem;'>Traumatológicos</div>", unsafe_allow_html=True)
        ant["traumatologicos"] = st.text_area("Fracturas, caídas, lesiones", value=ant["traumatologicos"], height=110, label_visibility="collapsed")

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Alérgicos</div>", unsafe_allow_html=True)
    ant["alergicos"] = st.text_area("Medicamentos, alimentos, otros alérgenos y tipo de reacción", value=ant["alergicos"], height=90, label_visibility="collapsed")

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Enfermedades de transmisión sexual</div>", unsafe_allow_html=True)
    ant["ets_sel"] = st.multiselect("ETS", ETS, default=ant["ets_sel"], label_visibility="collapsed")
    ant["ets_otros"] = st.text_input("Detalles ETS", value=ant["ets_otros"])

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Transfusionales</div>", unsafe_allow_html=True)
    ant["transfusionales"] = st.text_area("Número de transfusiones, motivo, reacciones", value=ant["transfusionales"], height=80, label_visibility="collapsed")

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Ginecoobstétricos (si aplica)</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    ant["gineco_menarquia"] = c1.text_input("Menarquia", value=ant["gineco_menarquia"])
    ant["gineco_formula"] = c2.text_input("Fórmula obstétrica (G_P_A_C_)", value=ant["gineco_formula"])
    c1, c2 = st.columns(2)
    ant["gineco_fur"] = c1.text_input("Fecha de última regla (FUR)", value=ant["gineco_fur"])
    ant["gineco_mac"] = c2.text_input("Método anticonceptivo", value=ant["gineco_mac"])
    ant["gineco_otros"] = st.text_area("Otros datos ginecoobstétricos", value=ant["gineco_otros"], height=70)

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Inmunológicos</div>", unsafe_allow_html=True)
    ant["inmunologicos"] = st.text_area("Esquema de vacunación", value=ant["inmunologicos"], height=80, label_visibility="collapsed")

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Medicamentos actuales</div>", unsafe_allow_html=True)
    ant["medicamentos"] = st.text_area("Fármaco, dosis, frecuencia", value=ant["medicamentos"], height=90, label_visibility="collapsed")

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Epidemiológicos</div>", unsafe_allow_html=True)
    ant["epidemiologicos"] = st.text_area("Vivienda, servicios básicos, convivientes, mascotas, saneamiento", value=ant["epidemiologicos"], height=90, label_visibility="collapsed")

# ============================================================
# 4. ANTECEDENTES FAMILIARES
# ============================================================
elif seccion == "familiares":
    header("Sección 4", "Antecedentes Familiares", "Agrega una fila por familiar directo relevante.")
    fam = hc["familiares"]

    with st.form("form_familiar", clear_on_submit=True):
        c1, c2, c3 = st.columns([2, 1.4, 1])
        parentesco = c1.selectbox("Parentesco", PARENTESCOS_FAMILIARES)
        estado = c2.selectbox("Estado", ["Vivo(a)", "Fallecido(a)"])
        edad = c3.text_input("Edad")
        enfermedades = st.multiselect("Enfermedades / causa de muerte", ENF_FAMILIARES_FRECUENTES)
        enfermedades_otro = st.text_input("Otras enfermedades no listadas")
        if st.form_submit_button("➕ Agregar familiar", use_container_width=True):
            texto_enf = ", ".join(enfermedades + ([enfermedades_otro] if enfermedades_otro else [])) or "Aparentemente sano(a)"
            fam["filas"].append({"parentesco": parentesco, "estado": estado, "edad": edad, "enfermedades": texto_enf})
            st.rerun()

    if fam["filas"]:
        st.write("")
        for i, f in enumerate(fam["filas"]):
            with st.container(border=True):
                c1, c2 = st.columns([6, 1])
                c1.markdown(f"**{f['parentesco']}** — {f['estado']}, {f['edad']} años · {f['enfermedades']}")
                if c2.button("Eliminar", key=f"del_fam_{i}"):
                    fam["filas"].pop(i)
                    st.rerun()
    else:
        st.info("Aún no has agregado familiares.")

    fam["observaciones"] = st.text_area("Observaciones adicionales", value=fam["observaciones"], height=80)

# ============================================================
# 5. HÁBITOS PSICOBIOLÓGICOS
# ============================================================
elif seccion == "habitos":
    header("Sección 5", "Hábitos Psicobiológicos", "Interroga cada hábito de forma sistemática.")
    hab = hc["habitos"]
    campos = [
        ("tabaquico", "Tabáquicos", "Cigarrillos/día, años de consumo, índice paquetes-año"),
        ("oh", "Alcohólicos", "Tipo de bebida, frecuencia, cantidad"),
        ("cafeico", "Cafeicos", "Tazas al día, con o sin azúcar"),
        ("alimentario", "Alimentarios", "Número de comidas, tipo de dieta, predominio"),
        ("drogas", "Drogas ilícitas", "Tipo, frecuencia, vía"),
        ("actividad_fisica", "Actividad física", "Tipo, frecuencia, duración"),
        ("sueno", "Sueño", "Horas, calidad, dificultad para conciliar"),
        ("sexuales", "Sexuales", "Vida sexual activa, número de parejas, protección"),
        ("estres", "Situación personal y estrés", "Fuentes de estrés, manejo"),
    ]
    for key, label, placeholder in campos:
        hab[key] = st.text_area(label, value=hab[key], height=70, placeholder=placeholder)

# ============================================================
# 6. FACTORES DE RIESGO CARDIOVASCULAR
# ============================================================
elif seccion == "frcv":
    header("Sección 6", "Factores de Riesgo Cardiovascular", "Clasifica los factores presentes en el paciente.")
    frcv = hc["frcv"]
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title' style='font-size:1.05rem;'>Modificables</div>", unsafe_allow_html=True)
        frcv["modificables_sel"] = st.multiselect("Modificables", FRCV_MODIFICABLES, default=frcv["modificables_sel"], label_visibility="collapsed")
    with c2:
        st.markdown("<div class='section-title' style='font-size:1.05rem;'>No modificables</div>", unsafe_allow_html=True)
        frcv["no_modificables_sel"] = st.multiselect("No modificables", FRCV_NO_MODIFICABLES, default=frcv["no_modificables_sel"], label_visibility="collapsed")
    frcv["otros"] = st.text_area("Notas adicionales", value=frcv["otros"], height=80)

# ============================================================
# 7. REVISIÓN POR SISTEMAS
# ============================================================
elif seccion == "ros":
    header("Sección 7", "Revisión por Sistemas", "Interrogatorio funcional completo, aparato por aparato.")
    guia("Selecciona los síntomas que el paciente refiere activamente en cada aparato. Lo no seleccionado se asumirá como negado en la historia final.")
    ros = hc["ros"]
    for sec in REVISION_SISTEMAS:
        with st.expander(f"{sec['icono']}  {sec['label']}", expanded=False):
            data = ros[sec["key"]]
            data["sintomas"] = st.multiselect("Síntomas que refiere", sec["sintomas"], default=data["sintomas"], key=f"ros_sint_{sec['key']}", label_visibility="collapsed")
            data["detalles"] = st.text_area("Detalles / características del síntoma", value=data["detalles"], key=f"ros_det_{sec['key']}", height=70, placeholder="Tiempo de evolución, intensidad, factores agravantes/atenuantes...")

# ============================================================
# 8. EXAMEN FÍSICO
# ============================================================
elif seccion == "examen":
    header("Sección 8", "Examen Físico", "Signos vitales y exploración por sistemas.")
    ex = hc["examen"]

    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Signos vitales</div>", unsafe_allow_html=True)
    sv = ex["signos_vitales"]
    c1, c2, c3, c4 = st.columns(4)
    sv["temperatura"] = c1.text_input("Temperatura (°C)", value=sv["temperatura"])
    sv["pulso"] = c2.text_input("Pulso (lpm)", value=sv["pulso"])
    sv["fr"] = c3.text_input("Frec. respiratoria (rpm)", value=sv["fr"])
    sv["spo2"] = c4.text_input("SpO2 (%)", value=sv["spo2"])
    c1, c2, c3, c4 = st.columns(4)
    sv["ta_sistolica"] = c1.text_input("T.A. sistólica", value=sv["ta_sistolica"])
    sv["ta_diastolica"] = c2.text_input("T.A. diastólica", value=sv["ta_diastolica"])
    sv["peso"] = c3.text_input("Peso (kg)", value=sv["peso"])
    sv["talla"] = c4.text_input("Talla (cm)", value=sv["talla"])
    sv["llenado_capilar"] = st.text_input("Llenado capilar", value=sv["llenado_capilar"])

    st.write("")
    st.markdown("<div class='section-title' style='font-size:1.05rem;'>Exploración por sistemas</div>", unsafe_allow_html=True)
    guia("Marca 'Normal' para usar automáticamente la plantilla estándar (editable), o 'Anormal' para elegir hallazgos y describirlos.")

    sistemas = ex["sistemas"]
    for sec in EXAMEN_FISICO_SISTEMAS:
        data = sistemas[sec["key"]]
        with st.expander(f"{sec['icono']}  {sec['label']}", expanded=False):
            data["estado"] = st.radio("Estado", ["No explorado", "Normal", "Anormal"],
                                       index=["No explorado", "Normal", "Anormal"].index(data["estado"]),
                                       key=f"ef_estado_{sec['key']}", horizontal=True, label_visibility="collapsed")
            if data["estado"] == "Normal":
                data["texto"] = st.text_area("Descripción", value=data["texto"] or sec["normal"], key=f"ef_texto_{sec['key']}", height=90)
            elif data["estado"] == "Anormal":
                data["anormales"] = st.multiselect("Hallazgos anormales", sec["anormales"], default=data["anormales"], key=f"ef_anorm_{sec['key']}")
                data["texto"] = st.text_area("Descripción detallada", value=data["texto"], key=f"ef_texto2_{sec['key']}", height=90,
                                              placeholder="Localización, características, severidad...")

# ============================================================
# 9. SÍNTESIS DIAGNÓSTICA
# ============================================================
elif seccion == "sintesis":
    header("Sección 9", "Síntesis Diagnóstica", "Cierra la historia con el razonamiento clínico.")
    sin = hc["sintesis"]
    sin["datos_positivos"] = st.text_area("Resumen de datos positivos (ordenados por importancia)", value=sin["datos_positivos"], height=140)

    guia("Sugerencias de síndromes frecuentes en medicina interna — puedes usarlas como punto de partida.")
    sugeridos = st.multiselect("Síndromes sugeridos", DIAGNOSTICOS_SINDROMATICOS_SUGERIDOS)
    sin["diagnosticos_sindromaticos"] = st.text_area("Impresiones diagnósticas / diagnóstico sindromático (en orden de importancia)",
                                                       value=sin["diagnosticos_sindromaticos"] or "\n".join(f"- {s}" for s in sugeridos), height=140)
    sin["observaciones"] = st.text_area("Observaciones", value=sin["observaciones"], height=100)
    sin["diagnostico_definitivo"] = st.text_area("Diagnóstico definitivo (al cerrar el caso)", value=sin["diagnostico_definitivo"], height=100)
    sin["plan"] = st.text_area("Plan / Tratamiento", value=sin["plan"], height=120)

# ============================================================
# 10. VISTA PREVIA Y DESCARGA
# ============================================================
elif seccion == "vista_previa":
    header("Vista previa", "Historia Clínica Completa", "Revisa el documento antes de descargarlo en PDF.")

    fil = hc["filiacion"]
    nombre = f"{fil['nombres']} {fil['apellidos']}".strip() or "Paciente sin nombre"

    with st.container(border=True):
        st.markdown(f"### {nombre}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Edad", fil["edad"] or "—")
        c2.metric("Sexo", fil["sexo"] or "—")
        c3.metric("Progreso general", f"{progreso_global()}%")

    st.write("")
    pdf_bytes = generar_pdf(hc)
    nombre_archivo = f"historia_clinica_{(fil['apellidos'] or 'paciente').strip().replace(' ', '_').lower()}.pdf"

    st.download_button(
        "⬇️  Descargar Historia Clínica en PDF",
        data=pdf_bytes,
        file_name=nombre_archivo,
        mime="application/pdf",
        use_container_width=True,
        type="primary",
    )

    st.write("")
    with st.expander("Ver resumen por secciones", expanded=True):
        for key, label, icono in SECCIONES:
            if key == "vista_previa":
                continue
            llenos, total = progreso_seccion(key)
            estado = "✅ Completo" if llenos == total and total > 0 else ("🟡 Parcial" if llenos else "⚪ Vacío")
            st.markdown(f"**{icono} {label}** — {estado} ({llenos}/{total})")
