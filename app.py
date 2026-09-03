import streamlit as st
from datetime import date

from utils.styles import inject_css, masthead_html, progress_capsule_html, selector_tema
from utils.state import (
    init_state, reset_state, SECCIONES, progreso_seccion, progreso_global,
    APP_AUTHOR, indice_paquete_anio, clasificar_ipa,
)
from utils.pdf_export import generar_pdf
from utils.narrativa import componer_narrativa
from utils import supa
from utils.legal import requerir_aceptacion_terminos, version_footer, APP_VERSION
from data.campos import (
    ENF_INFANCIA, ENF_CRONICAS_ADULTO, ETS, CAMPOS_ANTECEDENTES_LIBRES,
    PARENTESCOS_FAMILIARES, ENF_FAMILIARES_FRECUENTES,
    FRCV_MODIFICABLES, FRCV_NO_MODIFICABLES,
    MOTIVOS_CONSULTA, REVISION_SISTEMAS, EXAMEN_FISICO_SISTEMAS,
    FITZPATRICK_OPCIONES, WEBER_OPCIONES, RINNE_OPCIONES,
    ABDOMEN_MANIOBRAS, ESTADO_MANIOBRA, REFLEJOS_OSTEOTENDINOSOS,
    GRADOS_REFLEJO, SIGNOS_MENINGEOS, PARES_CRANEALES_TXT,
    DIAGNOSTICOS_SINDROMATICOS_SUGERIDOS,
)

st.set_page_config(
    page_title="QuickChart | Historia Clínica",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ---- 1. Login (si Supabase está configurado) ----
if not supa.requerir_login():
    st.stop()

# ---- 2. Términos de uso (una vez por cuenta) ----
if not requerir_aceptacion_terminos():
    st.stop()

init_state()
hc = st.session_state["hc"]
V = st.session_state["form_version"]  # sufijo de todas las keys explícitas — ver nota en utils/state.py

# ---- 3. Cargar borrador guardado (solo la primera vez que carga la sesión) ----
if supa.supabase_configurado() and not st.session_state.get("_borrador_cargado"):
    _borrador = supa.cargar_borrador()
    if _borrador:
        st.session_state["hc"] = _borrador
        hc = st.session_state["hc"]
    st.session_state["_borrador_cargado"] = True


def _autosave():
    if supa.supabase_configurado():
        supa.guardar_borrador(hc)


def _idx(options, value, default=0):
    try:
        return options.index(value)
    except (ValueError, TypeError):
        return default


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="mark">QuickChart</div>
            <div class="sub">Historia Clínica · Medicina Interna</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "auth_user" in st.session_state:
        st.caption(f"👤 {st.session_state['auth_user']['email']}")
        if st.button("Cerrar sesión", use_container_width=True):
            _autosave()
            supa.cerrar_sesion()

    st.write("")
    pct = progreso_global()
    st.caption(f"Progreso general — **{pct}%**")
    st.progress(pct / 100)
    st.write("")

    for key, label, icono in SECCIONES:
        if key == "vista_previa":
            continue
        llenos, total = progreso_seccion(key)
        badge = "✓" if llenos == total and total > 0 else (f"{llenos}/{total}" if llenos else "")
        activo = st.session_state["seccion_actual"] == key
        etiqueta_btn = f"{icono}  {label}" + (f"   {badge}" if badge else "")
        if st.button(etiqueta_btn, key=f"nav_{key}", use_container_width=True,
                     type="primary" if activo else "secondary"):
            _autosave()
            st.session_state["seccion_actual"] = key
            st.rerun()

    st.markdown("<div style='border-top:1px solid var(--line); margin:0.8rem 0;'></div>", unsafe_allow_html=True)
    if st.button("📄  Vista Previa y PDF", key="nav_preview", use_container_width=True,
                 type="primary" if st.session_state["seccion_actual"] == "vista_previa" else "secondary"):
        _autosave()
        st.session_state["seccion_actual"] = "vista_previa"
        st.rerun()

    st.write("")
    with st.expander("⚙️ Configuración"):
        st.caption("Tema")
        selector_tema()
        st.write("")
        st.caption("Médico / institución")
        hc["medico"]["nombre"] = st.text_input("Tu nombre", value=hc["medico"]["nombre"], placeholder="Ej. Jade Díaz")
        hc["medico"]["hospital"] = st.text_input("Institución / Hospital", value=hc["medico"]["hospital"], placeholder="Ej. Hospital Vargas de Caracas")
        hc["medico"]["servicio"] = st.text_input("Servicio", value=hc["medico"]["servicio"], placeholder="Ej. Medicina Interna")

    if st.button("🗑️ Nueva historia (borrar todo)", use_container_width=True):
        st.session_state["confirmar_reset"] = True

    if st.session_state.get("confirmar_reset"):
        st.warning("¿Seguro? Esta acción borra todos los datos.")
        c1, c2 = st.columns(2)
        if c1.button("Sí, borrar", use_container_width=True):
            reset_state()
            _autosave()
            st.session_state["confirmar_reset"] = False
            st.rerun()
        if c2.button("Cancelar", use_container_width=True):
            st.session_state["confirmar_reset"] = False
            st.rerun()

    st.markdown(
        f"""<div class="sidebar-footer">Diseñada y desarrollada por<br><b>{APP_AUTHOR}</b></div>""",
        unsafe_allow_html=True,
    )


# ============================================================
# Helpers de encabezado
# ============================================================
def header(kicker, titulo, subtitulo):
    st.markdown(
        f"""<div class="hc-header"><div class="kicker">{kicker}</div><h1>{titulo}</h1><p>{subtitulo}</p></div>""",
        unsafe_allow_html=True,
    )


def section_title(texto):
    st.markdown(f"<div class='section-title'>{texto}</div>", unsafe_allow_html=True)


def guia_popover(texto, label="¿Qué preguntar / explorar aquí?"):
    if not texto:
        return
    with st.popover(label, icon="💡"):
        st.write(texto)


st.markdown(masthead_html(APP_AUTHOR), unsafe_allow_html=True)
st.markdown(progress_capsule_html(progreso_global()), unsafe_allow_html=True)

seccion = st.session_state["seccion_actual"]

# ============================================================
# 1. DATOS DE FILIACIÓN
# ============================================================
if seccion == "filiacion":
    header("Sección 1 de 9", "Datos de Filiación", "Identificación del paciente y contacto de emergencia.")
    fil = hc["filiacion"]

    c1, c2, c3 = st.columns(3)
    fil["nombres"] = c1.text_input("Nombres", value=fil["nombres"], placeholder="Ej. María José")
    fil["apellidos"] = c2.text_input("Apellidos", value=fil["apellidos"], placeholder="Ej. Rodríguez Pérez")
    fil["ci"] = c3.text_input("Cédula de Identidad", value=fil["ci"], placeholder="Ej. 28.469.571")

    c1, c2, c3 = st.columns(3)
    fil["edad"] = c1.text_input("Edad", value=fil["edad"], placeholder="Ej. 45 años")
    fil["fecha_nacimiento"] = c2.date_input("Fecha de nacimiento", value=fil["fecha_nacimiento"],
                                             min_value=date(1900, 1, 1), max_value=date.today())
    opciones_sexo = ["", "Masculino", "Femenino"]
    fil["sexo"] = c3.selectbox("Sexo", opciones_sexo, index=_idx(opciones_sexo, fil["sexo"]))

    c1, c2, c3 = st.columns(3)
    opciones_ec = ["", "Soltero(a)", "Casado(a)", "Divorciado(a)", "Viudo(a)", "Unión estable"]
    fil["estado_civil"] = c1.selectbox("Estado civil", opciones_ec, index=_idx(opciones_ec, fil["estado_civil"]))
    fil["religion"] = c2.text_input("Religión", value=fil["religion"], placeholder="Ej. Católica")
    fil["raza"] = c3.text_input("Raza / autoidentificación étnica", value=fil["raza"], placeholder="Ej. Mestiza")

    c1, c2, c3 = st.columns(3)
    opciones_dom = ["", "Diestro(a)", "Zurdo(a)", "Ambidiestro(a)"]
    fil["dominancia"] = c1.selectbox("Dominancia", opciones_dom, index=_idx(opciones_dom, fil["dominancia"]))
    fil["lugar_nacimiento"] = c2.text_input("Lugar de nacimiento", value=fil["lugar_nacimiento"], placeholder="Ej. Caracas, Distrito Capital")
    fil["lugar_procedencia"] = c3.text_input("Lugar de procedencia", value=fil["lugar_procedencia"], placeholder="Ej. Caracas, Distrito Capital")

    c1, c2, c3 = st.columns(3)
    fil["ocupacion"] = c1.text_input("Ocupación", value=fil["ocupacion"], placeholder="Ej. Estudiante de Medicina")
    fil["telefono"] = c2.text_input("Teléfono", value=fil["telefono"], placeholder="Ej. 0414-1234567")
    fil["sala_cama"] = c3.text_input("Sala / Cama", value=fil["sala_cama"], placeholder="Ej. 14 / 21")

    fil["fecha_ingreso"] = st.date_input("Fecha de ingreso", value=fil["fecha_ingreso"],
                                          min_value=date(1900, 1, 1), max_value=date.today())

    section_title("Contacto de emergencia")
    c1, c2 = st.columns(2)
    fil["contacto_nombre"] = c1.text_input("Nombre completo", value=fil["contacto_nombre"], placeholder="Ej. Liliana Sojo")
    fil["contacto_telefono"] = c2.text_input("Teléfono", value=fil["contacto_telefono"], placeholder="Ej. 0426-6139428")
    c1, c2 = st.columns(2)
    fil["contacto_parentesco"] = c1.text_input("Parentesco", value=fil["contacto_parentesco"], placeholder="Ej. Madre")
    fil["contacto_direccion"] = c2.text_input("Dirección", value=fil["contacto_direccion"], placeholder="Ej. Distrito Capital")

# ============================================================
# 2. MOTIVO Y ENFERMEDAD ACTUAL — asistente dinámico
# ============================================================
elif seccion == "consulta":
    header("Sección 2 de 9", "Motivo de Consulta y Enfermedad Actual",
           "Elige los síntomas guía y te muestro exactamente qué interrogar de cada uno.")
    con = hc["consulta"]
    con["motivo"] = st.text_input('Motivo de consulta (entre comillas, en palabras del paciente)',
                                   value=con["motivo"], placeholder='Ej. "Dolor abdominal y vómitos"')

    section_title("Asistente de síntomas guiados")
    label_to_motivo = {f"{m['icono']} {m['label']}": m for m in MOTIVOS_CONSULTA}
    labels = list(label_to_motivo.keys())
    key_to_label = {m["key"]: lbl for lbl, m in label_to_motivo.items()}
    default_labels = [key_to_label[k] for k in con["motivos_sel"] if k in key_to_label]

    seleccion = st.pills("¿Qué síntomas principales presenta?", labels, selection_mode="multi",
                          default=default_labels, key=f"motivos_pills_{V}")
    con["motivos_sel"] = [label_to_motivo[l]["key"] for l in seleccion]

    for m in MOTIVOS_CONSULTA:
        if m["key"] not in con["motivos_sel"]:
            continue
        datos = con["motivos_datos"].setdefault(m["key"], {})
        with st.expander(f"{m['icono']}  {m['label']} — caracterización semiológica", expanded=True):
            st.caption(m["mnemonico"])
            cols = st.columns(2)
            for i, campo in enumerate(m["campos"]):
                col = cols[i % 2]
                wkey = f"mc_{m['key']}_{campo['key']}_{V}"
                if campo["tipo"] == "text":
                    datos[campo["key"]] = col.text_input(
                        campo["label"], value=datos.get(campo["key"], ""),
                        placeholder=campo.get("placeholder", ""), help=campo.get("help") or None, key=wkey,
                    )
                elif campo["tipo"] == "select":
                    opciones = [""] + campo["opciones"]
                    actual = datos.get(campo["key"], "")
                    datos[campo["key"]] = col.selectbox(
                        campo["label"], opciones, index=_idx(opciones, actual),
                        format_func=lambda x: "—" if x == "" else x,
                        help=campo.get("help") or None, key=wkey,
                    )
                elif campo["tipo"] == "slider":
                    datos[campo["key"]] = col.slider(
                        campo["label"], 0, 10, value=int(datos.get(campo["key"]) or 0),
                        help=campo.get("help") or None, key=wkey,
                    )

            narrativa = componer_narrativa(m["key"], m["label"], m["campos"], datos)
            if narrativa:
                with st.container(border=True):
                    st.caption("Vista previa de la redacción")
                    st.write(narrativa)
                if st.button("➕ Añadir al relato", key=f"add_{m['key']}_{V}"):
                    actual = con["enfermedad_actual"].strip()
                    con["enfermedad_actual"] = (actual + " " + narrativa).strip() if actual else narrativa
                    st.toast(f"Se añadió la caracterización de {m['label'].lower()} al relato", icon="✅")
                    st.rerun()
            else:
                st.caption("Completa al menos un campo para ver la redacción sugerida aquí.")

    section_title("Enfermedad Actual")
    con["enfermedad_actual"] = st.text_area(
        "Relato completo", value=con["enfermedad_actual"], height=260,
        help="Inicio, características del síntoma principal, evolución, síntomas asociados y qué lo trae a consulta.",
        placeholder='Paciente masculino/femenino de X años, natural y procedente de..., que refiere inicio de enfermedad actual el día...',
        label_visibility="collapsed",
    )

# ============================================================
# 3. ANTECEDENTES PERSONALES
# ============================================================
elif seccion == "antecedentes":
    header("Sección 3 de 9", "Antecedentes Personales", "Recorre cada bloque; lo seleccionado se redacta solo.")
    ant = hc["antecedentes"]
    L = CAMPOS_ANTECEDENTES_LIBRES

    section_title("Médicos — Infancia")
    ant["enf_infancia_sel"] = st.pills("Enfermedades de la infancia", ENF_INFANCIA, selection_mode="multi",
                                        default=ant["enf_infancia_sel"], key=f"ant_inf_{V}")
    ant["enf_infancia_otros"] = st.text_input("Otros detalles (infancia)", value=ant["enf_infancia_otros"],
                                               placeholder="Ej. Mononucleosis a los 9 años, sin complicaciones.")

    section_title("Médicos — Adultez")
    ant["enf_cronicas_sel"] = st.pills("Enfermedades crónicas conocidas", ENF_CRONICAS_ADULTO, selection_mode="multi",
                                        default=ant["enf_cronicas_sel"], key=f"ant_cron_{V}")
    ant["enf_cronicas_otros"] = st.text_area("Detalle (diagnóstico, año, tratamiento)", value=ant["enf_cronicas_otros"],
                                              height=90, placeholder="Ej. HTA diagnosticada en 2023, en tratamiento con Losartán.")

    for key in ["infecciones", "quirurgicos", "traumatologicos", "alergicos"]:
        cfg = L[key]
        section_title(cfg["label"])
        ant[key] = st.text_area(cfg["label"], value=ant[key], height=85, placeholder=cfg["placeholder"],
                                 help=cfg["help"], label_visibility="collapsed")

    section_title("Enfermedades de transmisión sexual")
    ant["ets_sel"] = st.pills("ETS", ETS, selection_mode="multi", default=ant["ets_sel"],
                               key=f"ant_ets_{V}", label_visibility="collapsed")
    ant["ets_otros"] = st.text_input("Detalles ETS", value=ant["ets_otros"], placeholder="Ej. Tratamiento recibido, año del diagnóstico.")

    for key in ["transfusionales"]:
        cfg = L[key]
        section_title(cfg["label"])
        ant[key] = st.text_area(cfg["label"], value=ant[key], height=75, placeholder=cfg["placeholder"],
                                 help=cfg["help"], label_visibility="collapsed")

    section_title("Ginecoobstétricos (si aplica)")
    c1, c2 = st.columns(2)
    ant["gineco_menarquia"] = c1.text_input("Menarquia", value=ant["gineco_menarquia"], placeholder="Ej. 12 años")
    ant["gineco_formula"] = c2.text_input("Fórmula obstétrica (G_P_A_C_)", value=ant["gineco_formula"], placeholder="Ej. G2 P1 A1 C0")
    c1, c2 = st.columns(2)
    ant["gineco_fur"] = c1.text_input("Fecha de última regla (FUR)", value=ant["gineco_fur"], placeholder="Ej. 15/07/2026")
    ant["gineco_mac"] = c2.text_input("Método anticonceptivo", value=ant["gineco_mac"], placeholder="Ej. Anticonceptivos orales")
    c1, c2 = st.columns(2)
    ant["gineco_menopausia"] = c1.text_input("Menopausia", value=ant["gineco_menopausia"], placeholder="Ej. No aplica")
    ant["gineco_procedimientos"] = c2.text_input("Procedimientos ginecológicos", value=ant["gineco_procedimientos"], placeholder="Ej. Biopsia cervical en 2022")
    ant["gineco_sx_menstruales"] = st.text_area("Síntomas menstruales / ciclo", value=ant["gineco_sx_menstruales"],
                                                 height=70, placeholder="Ej. Ciclos regulares cada 28 días, sin dismenorrea.")

    for key in ["inmunologicos", "medicamentos", "epidemiologicos"]:
        cfg = L[key]
        section_title(cfg["label"])
        ant[key] = st.text_area(cfg["label"], value=ant[key], height=85, placeholder=cfg["placeholder"],
                                 help=cfg["help"], label_visibility="collapsed")

# ============================================================
# 4. ANTECEDENTES FAMILIARES
# ============================================================
elif seccion == "familiares":
    header("Sección 4 de 9", "Antecedentes Familiares", "Agrega una fila por familiar directo relevante.")
    fam = hc["familiares"]
    FV = st.session_state.setdefault("fam_form_v", 0)

    with st.form(f"form_familiar_{FV}"):
        c1, c2, c3 = st.columns([2, 1.4, 1])
        parentesco = c1.selectbox("Parentesco", PARENTESCOS_FAMILIARES, key=f"fam_parentesco_{FV}")
        estado = c2.segmented_control("Estado", ["Vivo(a)", "Fallecido(a)"], default="Vivo(a)", key=f"fam_estado_{FV}")
        edad = c3.text_input("Edad", key=f"fam_edad_{FV}")
        enfermedades = st.multiselect("Enfermedades / causa de muerte", ENF_FAMILIARES_FRECUENTES, key=f"fam_enf_{FV}")
        enfermedades_otro = st.text_input("Otras enfermedades no listadas", key=f"fam_enf_otro_{FV}")
        if st.form_submit_button("➕ Agregar familiar", use_container_width=True):
            texto_enf = ", ".join(enfermedades + ([enfermedades_otro] if enfermedades_otro else [])) or "Aparentemente sano(a)"
            fam["filas"].append({"parentesco": parentesco, "estado": estado or "Vivo(a)", "edad": edad, "enfermedades": texto_enf})
            st.session_state["fam_form_v"] += 1
            st.rerun()

    if fam["filas"]:
        st.write("")
        for i, f in enumerate(fam["filas"]):
            with st.container(border=True):
                c1, c2 = st.columns([6, 1])
                c1.markdown(f"**{f['parentesco']}** — {f['estado']}, {f['edad']} años · {f['enfermedades']}")
                if c2.button("Eliminar", key=f"del_fam_{i}_{V}"):
                    fam["filas"].pop(i)
                    st.rerun()
    else:
        st.info("Aún no has agregado familiares.")

    fam["observaciones"] = st.text_area("Observaciones adicionales", value=fam["observaciones"], height=80)

# ============================================================
# 5. HÁBITOS PSICOBIOLÓGICOS
# ============================================================
elif seccion == "habitos":
    header("Sección 5 de 9", "Hábitos Psicobiológicos", "Interroga cada hábito de forma sistemática.")
    hab = hc["habitos"]

    section_title("🚬 Tabáquicos")
    tab = hab["tabaquico"]
    tab["fuma"] = st.toggle("¿Fuma o ha fumado alguna vez?", value=tab["fuma"])
    if tab["fuma"]:
        c1, c2 = st.columns(2)
        tab["cigarrillos_dia"] = c1.number_input("Cigarrillos por día", min_value=0, max_value=100,
                                                  value=int(tab["cigarrillos_dia"] or 0), step=1)
        tab["anios_fumando"] = c2.number_input("Años fumando", min_value=0, max_value=100,
                                                value=int(tab["anios_fumando"] or 0), step=1)
        tab["exfumador"] = st.toggle("Es exfumador (ya no fuma actualmente)", value=tab["exfumador"])
        if tab["exfumador"]:
            tab["anios_desde_dejo"] = st.number_input("¿Hace cuántos años dejó de fumar?", min_value=0, max_value=100,
                                                       value=int(tab["anios_desde_dejo"] or 0), step=1)

        ipa = indice_paquete_anio(tab)
        clasif, color = clasificar_ipa(ipa)
        c1, c2 = st.columns([1, 1])
        with c1:
            st.metric("Índice paquete-año", ipa, help="Fórmula: (cigarrillos/día ÷ 20) × años fumando")
        with c2:
            st.write("")
            st.badge(clasif, color=color)
        tab["notas"] = st.text_input("Notas adicionales", value=tab["notas"], placeholder="Ej. Fumador pasivo en el hogar.")
    else:
        tab["notas"] = st.text_input("Notas (opcional)", value=tab["notas"], placeholder="Ej. Niega hábito tabáquico.")

    for key, label, help_txt, placeholder in [
        ("oh", "🍷 Alcohólicos", "Tipo de bebida, frecuencia, cantidad, ¿llega a la embriaguez?", "Ej. Cerveza los fines de semana, 3-4 unidades."),
        ("cafeico", "☕ Cafeicos", "Tazas al día, con o sin azúcar", "Ej. 2 tazas de café al día, con 1 cucharada de azúcar."),
        ("alimentario", "🍽️ Alimentarios", "Número de comidas, tipo de dieta, predominio, cantidades", "Ej. 3 comidas al día, dieta balanceada."),
        ("drogas", "💊 Drogas ilícitas", "Tipo, dónde y cuántas, frecuencia, vía", "Ej. Niega consumo de drogas ilícitas."),
        ("actividad_fisica", "🏃 Actividad física / Ejercicio", "Tipo, frecuencia, duración, adecuado o sedentario", "Ej. Sedentario."),
        ("sueno", "😴 Sueño", "Horas, continuo o interrumpido, matutino/vespertino/diurno", "Ej. 6-7 horas nocturnas continuas."),
        ("sexuales", "💞 Sexuales", "Vida sexual activa, número de parejas, protección", "Ej. Vida sexual activa, pareja única, uso de preservativo."),
        ("estres", "🧘 Situación personal y estrés", "Fuentes de estrés, manejo", "Ej. Refiere estrés académico moderado."),
    ]:
        section_title(label)
        hab[key] = st.text_area(label, value=hab[key], height=70, placeholder=placeholder, help=help_txt, label_visibility="collapsed")

# ============================================================
# 6. FACTORES DE RIESGO CARDIOVASCULAR
# ============================================================
elif seccion == "frcv":
    header("Sección 6 de 9", "Factores de Riesgo Cardiovascular", "Clasifica los factores presentes en el paciente.")
    frcv = hc["frcv"]
    section_title("Modificables")
    frcv["modificables_sel"] = st.pills("Modificables", FRCV_MODIFICABLES, selection_mode="multi",
                                         default=frcv["modificables_sel"], key=f"frcv_mod_{V}", label_visibility="collapsed")
    section_title("No modificables")
    frcv["no_modificables_sel"] = st.pills("No modificables", FRCV_NO_MODIFICABLES, selection_mode="multi",
                                            default=frcv["no_modificables_sel"], key=f"frcv_nomod_{V}", label_visibility="collapsed")
    frcv["otros"] = st.text_area("Notas adicionales", value=frcv["otros"], height=80)

# ============================================================
# 7. REVISIÓN POR SISTEMAS
# ============================================================
elif seccion == "ros":
    header("Sección 7 de 9", "Revisión por Sistemas", "Interrogatorio funcional completo, aparato por aparato.")
    st.caption("Selecciona lo que el paciente refiere activamente. Lo no seleccionado se asume negado en la historia final.")
    ros = hc["ros"]
    for sec in REVISION_SISTEMAS:
        data = ros[sec["key"]]
        etiqueta = f"{sec['icono']}  {sec['label']}"
        with st.expander(etiqueta, expanded=False):
            if sec.get("guia"):
                st.markdown(f"<div class='mini-guia'>{sec['guia']}</div>", unsafe_allow_html=True)
            data["sintomas"] = st.pills("Síntomas que refiere", sec["sintomas"], selection_mode="multi",
                                         default=data["sintomas"], key=f"ros_sint_{sec['key']}_{V}",
                                         label_visibility="collapsed")
            data["detalles"] = st.text_area("Detalles / características", value=data["detalles"],
                                             key=f"ros_det_{sec['key']}_{V}", height=70,
                                             placeholder="Tiempo de evolución, intensidad, factores agravantes/atenuantes...",
                                             label_visibility="collapsed")

# ============================================================
# 8. EXAMEN FÍSICO
# ============================================================
elif seccion == "examen":
    header("Sección 8 de 9", "Examen Físico", "Signos vitales, exploración por sistemas y maniobras específicas.")
    ex = hc["examen"]

    section_title("Signos vitales")
    sv = ex["signos_vitales"]
    c1, c2, c3, c4 = st.columns(4)
    sv["temperatura"] = c1.text_input("Temperatura (°C)", value=sv["temperatura"], placeholder="36.5")
    sv["pulso"] = c2.text_input("Pulso (lpm)", value=sv["pulso"], placeholder="78")
    sv["fr"] = c3.text_input("Frec. respiratoria (rpm)", value=sv["fr"], placeholder="16")
    sv["spo2"] = c4.text_input("SpO2 (%)", value=sv["spo2"], placeholder="98")
    c1, c2, c3, c4 = st.columns(4)
    sv["ta_sistolica"] = c1.text_input("T.A. sistólica", value=sv["ta_sistolica"], placeholder="120")
    sv["ta_diastolica"] = c2.text_input("T.A. diastólica", value=sv["ta_diastolica"], placeholder="80")
    sv["peso"] = c3.text_input("Peso (kg)", value=sv["peso"], placeholder="70")
    sv["talla"] = c4.text_input("Talla (cm)", value=sv["talla"], placeholder="170")
    sv["llenado_capilar"] = st.text_input("Llenado capilar", value=sv["llenado_capilar"], placeholder="< 3 segundos")

    st.write("")
    section_title("Exploración por sistemas")
    st.caption("Marca 'Normal' para usar la plantilla estándar (editable), o 'Anormal' para elegir hallazgos.")

    sistemas = ex["sistemas"]
    extra = ex["extra"]
    ESTADOS = ["No explorado", "Normal", "Anormal"]

    for sec in EXAMEN_FISICO_SISTEMAS:
        data = sistemas[sec["key"]]
        with st.expander(f"{sec['icono']}  {sec['label']}", expanded=False):
            if sec.get("guia"):
                guia_popover(sec["guia"])
            data["estado"] = st.segmented_control("Estado", ESTADOS, default=data["estado"],
                                                    key=f"ef_estado_{sec['key']}_{V}", required=True)
            if data["estado"] == "Normal":
                data["texto"] = st.text_area("Descripción", value=data["texto"] or sec["normal"],
                                              key=f"ef_texto_{sec['key']}_{V}", height=90)
            elif data["estado"] == "Anormal":
                data["anormales"] = st.pills("Hallazgos anormales", sec["anormales"], selection_mode="multi",
                                              default=data["anormales"], key=f"ef_anorm_{sec['key']}_{V}")
                data["texto"] = st.text_area("Descripción detallada", value=data["texto"],
                                              key=f"ef_texto2_{sec['key']}_{V}", height=90,
                                              placeholder="Localización, características, severidad...")

            # ---- Bloques especiales por sistema ----
            if data["estado"] != "No explorado" and sec.get("extra") == "fitzpatrick":
                st.caption("Fototipo cutáneo")
                extra["piel"]["fitzpatrick"] = st.selectbox(
                    "Fototipo de Fitzpatrick", FITZPATRICK_OPCIONES,
                    index=_idx(FITZPATRICK_OPCIONES, extra["piel"]["fitzpatrick"]), key=f"fitz_{V}",
                )

            elif data["estado"] != "No explorado" and sec.get("extra") == "ojos_reflejos":
                st.caption("Reflejos pupilares")
                op = ["No evaluado", "Presente", "Ausente"]
                c1, c2 = st.columns(2)
                extra["ojos"]["fotomotor"] = c1.selectbox("Reflejo fotomotor", op, index=_idx(op, extra["ojos"]["fotomotor"]), key=f"fotomotor_{V}")
                extra["ojos"]["convergencia"] = c2.selectbox("Reflejo de convergencia", op, index=_idx(op, extra["ojos"]["convergencia"]), key=f"converg_{V}")

            elif data["estado"] != "No explorado" and sec.get("extra") == "weber_rinne":
                st.caption("Pruebas de diapasón")
                c1, c2 = st.columns(2)
                extra["oidos"]["weber"] = c1.selectbox("Weber", WEBER_OPCIONES, index=_idx(WEBER_OPCIONES, extra["oidos"]["weber"]), key=f"weber_{V}")
                extra["oidos"]["rinne"] = c2.selectbox("Rinne", RINNE_OPCIONES, index=_idx(RINNE_OPCIONES, extra["oidos"]["rinne"]), key=f"rinne_{V}")

            elif data["estado"] != "No explorado" and sec.get("extra") == "abdomen_maniobras":
                st.caption("Maniobras específicas")
                cols = st.columns(4)
                claves = ["murphy", "blumberg", "mcburney", "rovsing"]
                for i, (k, lab) in enumerate(zip(claves, ABDOMEN_MANIOBRAS)):
                    extra["abdomen"][k] = cols[i].selectbox(lab, ESTADO_MANIOBRA, index=_idx(ESTADO_MANIOBRA, extra["abdomen"][k]), key=f"ab_{k}_{V}")
                c1, c2 = st.columns(2)
                extra["abdomen"]["puno_percusion_der"] = c1.selectbox("Puño percusión derecho", ESTADO_MANIOBRA,
                                                                       index=_idx(ESTADO_MANIOBRA, extra["abdomen"]["puno_percusion_der"]), key=f"pp_der_{V}")
                extra["abdomen"]["puno_percusion_izq"] = c2.selectbox("Puño percusión izquierdo", ESTADO_MANIOBRA,
                                                                       index=_idx(ESTADO_MANIOBRA, extra["abdomen"]["puno_percusion_izq"]), key=f"pp_izq_{V}")

            elif data["estado"] != "No explorado" and sec.get("extra") == "neuro_completo":
                st.caption("Reflejos osteotendinosos")
                cols = st.columns(len(REFLEJOS_OSTEOTENDINOSOS))
                for i, r in enumerate(REFLEJOS_OSTEOTENDINOSOS):
                    extra["neurologico"]["reflejos"][r] = cols[i].selectbox(
                        r, GRADOS_REFLEJO, index=_idx(GRADOS_REFLEJO, extra["neurologico"]["reflejos"][r]), key=f"reflejo_{r}_{V}",
                    )
                st.caption("Signos meníngeos")
                extra["neurologico"]["signos_meningeos"] = st.pills(
                    "Signos meníngeos presentes", SIGNOS_MENINGEOS, selection_mode="multi",
                    default=extra["neurologico"]["signos_meningeos"], key=f"meningeos_{V}", label_visibility="collapsed",
                )
                st.caption("Pares craneales")
                extra["neurologico"]["pares_craneales_normal"] = st.toggle(
                    "Los 12 pares craneales están sin alteraciones", value=extra["neurologico"]["pares_craneales_normal"], key=f"pares_ok_{V}",
                )
                if extra["neurologico"]["pares_craneales_normal"]:
                    st.markdown(f"<div class='mini-guia'>{PARES_CRANEALES_TXT}</div>", unsafe_allow_html=True)
                else:
                    extra["neurologico"]["pares_craneales_detalle"] = st.text_area(
                        "Describe la alteración encontrada", value=extra["neurologico"]["pares_craneales_detalle"],
                        key=f"pares_det_{V}", height=70, placeholder="Ej. Parálisis facial periférica derecha (VII par).",
                    )

# ============================================================
# 9. SÍNTESIS DIAGNÓSTICA
# ============================================================
elif seccion == "sintesis":
    header("Sección 9 de 9", "Síntesis Diagnóstica", "Cierra la historia con el razonamiento clínico.")
    sin = hc["sintesis"]
    sin["datos_positivos"] = st.text_area("Resumen de datos positivos (ordenados por importancia)",
                                           value=sin["datos_positivos"], height=140,
                                           placeholder="1. Dolor abdominal tipo cólico...\n2. Vómitos de contenido alimentario...")

    st.caption("Síndromes frecuentes en medicina interna — puedes usarlos como punto de partida.")
    sugeridos = st.pills("Síndromes sugeridos", DIAGNOSTICOS_SINDROMATICOS_SUGERIDOS, selection_mode="multi",
                          key=f"sind_sugeridos_{V}", label_visibility="collapsed")
    valor_diag = sin["diagnosticos_sindromaticos"] or "\n".join(f"- {s}" for s in sugeridos)
    sin["diagnosticos_sindromaticos"] = st.text_area("Impresiones diagnósticas (en orden de importancia)",
                                                       value=valor_diag, height=140)
    sin["observaciones"] = st.text_area("Observaciones", value=sin["observaciones"], height=100)
    sin["diagnostico_definitivo"] = st.text_area("Diagnóstico definitivo (al cerrar el caso)",
                                                   value=sin["diagnostico_definitivo"], height=100)
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
    _autosave()
    pdf_bytes = generar_pdf(hc)
    nombre_archivo = f"historia_clinica_{(fil['apellidos'] or 'paciente').strip().replace(' ', '_').lower()}.pdf"

    st.download_button(
        "⬇️  Descargar Historia Clínica en PDF", data=pdf_bytes, file_name=nombre_archivo,
        mime="application/pdf", use_container_width=True, type="primary",
    )

    st.write("")
    with st.expander("Ver resumen por secciones", expanded=True):
        for key, label, icono in SECCIONES:
            if key == "vista_previa":
                continue
            llenos, total = progreso_seccion(key)
            estado = "✅ Completo" if llenos == total and total > 0 else ("🟡 Parcial" if llenos else "⚪ Vacío")
            st.markdown(f"**{icono} {label}** — {estado} ({llenos}/{total})")

# ============================================================
# NAVEGACIÓN INFERIOR — Anterior / Siguiente
# ============================================================
if seccion != "vista_previa":
    st.write("")
    st.markdown("<div style='border-top:1px solid var(--line); margin: 0.6rem 0 1.1rem 0;'></div>", unsafe_allow_html=True)
    claves = [s[0] for s in SECCIONES]
    idx_actual = claves.index(seccion)
    c1, c2, c3 = st.columns([1, 3, 1])
    with c1:
        if idx_actual > 0:
            if st.button("← Anterior", use_container_width=True):
                _autosave()
                st.session_state["seccion_actual"] = claves[idx_actual - 1]
                st.rerun()
    with c3:
        siguiente_label = "Ver Historia →" if claves[idx_actual + 1] == "vista_previa" else "Siguiente →"
        if st.button(siguiente_label, use_container_width=True, type="primary"):
            _autosave()
            st.session_state["seccion_actual"] = claves[idx_actual + 1]
            st.rerun()

version_footer()
