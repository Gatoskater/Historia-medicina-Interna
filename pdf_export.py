"""
Generación del PDF final de la Historia Clínica, con un diseño limpio y
profesional (encabezado tipo membrete, tipografía serif para títulos,
acentos en color teal, tablas para datos estructurados).
"""

import io
from datetime import date, datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)

from data.campos import REVISION_SISTEMAS, EXAMEN_FISICO_SISTEMAS

ACCENT = colors.HexColor("#0d9488")
ACCENT_DARK = colors.HexColor("#0f766e")
INK = colors.HexColor("#0f172a")
INK_SOFT = colors.HexColor("#334155")
LINE = colors.HexColor("#cbd5e1")
BG_SOFT = colors.HexColor("#f0fdfa")


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(
        "TituloPortada", parent=ss["Title"], fontName="Times-Bold",
        fontSize=20, textColor=INK, spaceAfter=2, alignment=TA_CENTER,
    ))
    ss.add(ParagraphStyle(
        "Subtitulo", parent=ss["Normal"], fontName="Helvetica",
        fontSize=10, textColor=INK_SOFT, alignment=TA_CENTER, spaceAfter=0,
    ))
    ss.add(ParagraphStyle(
        "Seccion", parent=ss["Heading1"], fontName="Times-Bold",
        fontSize=13.5, textColor=INK, spaceBefore=14, spaceAfter=6,
        borderColor=ACCENT, borderWidth=0, leftIndent=0,
    ))
    ss.add(ParagraphStyle(
        "SubSeccion", parent=ss["Heading2"], fontName="Helvetica-Bold",
        fontSize=10.3, textColor=ACCENT_DARK, spaceBefore=8, spaceAfter=3,
        textTransform="uppercase",
    ))
    ss.add(ParagraphStyle(
        "Cuerpo", parent=ss["Normal"], fontName="Helvetica",
        fontSize=9.6, textColor=INK, leading=13.5, alignment=TA_LEFT,
    ))
    ss.add(ParagraphStyle(
        "CuerpoMuted", parent=ss["Normal"], fontName="Helvetica-Oblique",
        fontSize=9.2, textColor=INK_SOFT, leading=13,
    ))
    ss.add(ParagraphStyle(
        "Etiqueta", parent=ss["Normal"], fontName="Helvetica-Bold",
        fontSize=8.6, textColor=INK_SOFT,
    ))
    return ss


def _accent_rule():
    return HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceAfter=10)


def _campo(label, value):
    value = value if value not in (None, "") else "—"
    return f"<b>{label}:</b> {value}"


def _tabla_2col(pairs, styles, col_widths=(9 * cm, 8 * cm)):
    rows = []
    for a, b in pairs:
        rows.append([Paragraph(a, styles["Cuerpo"]), Paragraph(b, styles["Cuerpo"])])
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
    ]))
    return t


def _fmt_fecha(d):
    if not d:
        return "—"
    if isinstance(d, (date, datetime)):
        return d.strftime("%d/%m/%Y")
    return str(d)


def _lista_a_texto(items):
    return ", ".join(items) if items else ""


def generar_pdf(hc: dict) -> bytes:
    styles = _styles()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=1.6 * cm, bottomMargin=1.6 * cm,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
        title="Historia Clínica - Medicina Interna",
    )
    story = []

    fil = hc["filiacion"]
    medico = hc.get("medico", {})
    nombre_completo = f"{fil.get('nombres','').strip()} {fil.get('apellidos','').strip()}".strip() or "Paciente sin nombre registrado"

    # ---------- Encabezado / portada ----------
    if medico.get("hospital"):
        story.append(Paragraph(medico["hospital"].upper(), styles["Subtitulo"]))
    story.append(Paragraph("Historia Clínica", styles["TituloPortada"]))
    story.append(Paragraph("Medicina Interna", ParagraphStyle(
        "sub2", parent=styles["Subtitulo"], fontName="Times-Italic",
        fontSize=12, textColor=ACCENT_DARK, spaceAfter=6,
    )))
    story.append(_accent_rule())

    story.append(_tabla_2col([
        (_campo("Paciente", nombre_completo), _campo("C.I.", fil.get("ci", ""))),
        (_campo("Edad", fil.get("edad", "")), _campo("Sexo", fil.get("sexo", ""))),
        (_campo("Fecha de nacimiento", _fmt_fecha(fil.get("fecha_nacimiento"))),
         _campo("Fecha de ingreso", _fmt_fecha(fil.get("fecha_ingreso")))),
        (_campo("Sala / Cama", fil.get("sala_cama", "")),
         _campo("Ocupación", fil.get("ocupacion", ""))),
    ], styles))
    story.append(Spacer(1, 10))

    # ---------- Datos de filiación completos ----------
    story.append(Paragraph("Datos de Filiación", styles["Seccion"]))
    story.append(_tabla_2col([
        (_campo("Estado civil", fil.get("estado_civil", "")), _campo("Religión", fil.get("religion", ""))),
        (_campo("Raza", fil.get("raza", "")), _campo("Dominancia", fil.get("dominancia", ""))),
        (_campo("Lugar de nacimiento", fil.get("lugar_nacimiento", "")),
         _campo("Lugar de procedencia", fil.get("lugar_procedencia", ""))),
        (_campo("Teléfono", fil.get("telefono", "")), ""),
    ], styles))
    story.append(Paragraph("Contacto de emergencia", styles["SubSeccion"]))
    story.append(_tabla_2col([
        (_campo("Nombre", fil.get("contacto_nombre", "")), _campo("Teléfono", fil.get("contacto_telefono", ""))),
        (_campo("Parentesco", fil.get("contacto_parentesco", "")), _campo("Dirección", fil.get("contacto_direccion", ""))),
    ], styles))

    # ---------- Motivo y enfermedad actual ----------
    con = hc["consulta"]
    story.append(Paragraph("Motivo de Consulta", styles["Seccion"]))
    story.append(Paragraph(f"“{con.get('motivo','').strip() or '—'}”", ParagraphStyle(
        "motivo", parent=styles["Cuerpo"], fontName="Times-Italic", fontSize=11,
    )))
    story.append(Paragraph("Enfermedad Actual", styles["Seccion"]))
    story.append(Paragraph((con.get("enfermedad_actual", "").strip() or "—").replace("\n", "<br/>"), styles["Cuerpo"]))

    # ---------- Antecedentes personales ----------
    ant = hc["antecedentes"]
    story.append(Paragraph("Antecedentes Personales", styles["Seccion"]))

    story.append(Paragraph("Médicos (infancia)", styles["SubSeccion"]))
    texto = _lista_a_texto(ant["enf_infancia_sel"]) or "Niega antecedentes relevantes."
    if ant.get("enf_infancia_otros"):
        texto += f" {ant['enf_infancia_otros']}"
    story.append(Paragraph(texto, styles["Cuerpo"]))

    story.append(Paragraph("Médicos (adultez)", styles["SubSeccion"]))
    texto = _lista_a_texto(ant["enf_cronicas_sel"]) or "Niega enfermedades crónicas conocidas."
    if ant.get("enf_cronicas_otros"):
        texto += f" {ant['enf_cronicas_otros']}"
    story.append(Paragraph(texto, styles["Cuerpo"]))

    story.append(Paragraph("Quirúrgicos", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("quirurgicos", "").strip() or "Niega antecedentes quirúrgicos.", styles["Cuerpo"]))

    story.append(Paragraph("Traumatológicos", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("traumatologicos", "").strip() or "Niega antecedentes traumatológicos.", styles["Cuerpo"]))

    story.append(Paragraph("Alérgicos", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("alergicos", "").strip() or "Niega alergias conocidas.", styles["Cuerpo"]))

    story.append(Paragraph("Enfermedades de transmisión sexual", styles["SubSeccion"]))
    texto = _lista_a_texto(ant["ets_sel"]) or "Niega antecedentes de ETS."
    if ant.get("ets_otros"):
        texto += f" {ant['ets_otros']}"
    story.append(Paragraph(texto, styles["Cuerpo"]))

    story.append(Paragraph("Transfusionales", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("transfusionales", "").strip() or "Niega transfusiones previas.", styles["Cuerpo"]))

    if any([ant.get("gineco_menarquia"), ant.get("gineco_formula"), ant.get("gineco_fur"), ant.get("gineco_mac"), ant.get("gineco_otros")]):
        story.append(Paragraph("Ginecoobstétricos", styles["SubSeccion"]))
        story.append(_tabla_2col([
            (_campo("Menarquia", ant.get("gineco_menarquia", "")), _campo("Fórmula obstétrica", ant.get("gineco_formula", ""))),
            (_campo("FUR", ant.get("gineco_fur", "")), _campo("Método anticonceptivo", ant.get("gineco_mac", ""))),
        ], styles))
        if ant.get("gineco_otros"):
            story.append(Paragraph(ant["gineco_otros"], styles["Cuerpo"]))

    story.append(Paragraph("Inmunológicos", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("inmunologicos", "").strip() or "—", styles["Cuerpo"]))

    story.append(Paragraph("Medicamentos actuales", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("medicamentos", "").strip() or "Niega uso de medicamentos.", styles["Cuerpo"]))

    story.append(Paragraph("Epidemiológicos", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("epidemiologicos", "").strip() or "—", styles["Cuerpo"]))

    # ---------- Antecedentes familiares ----------
    fam = hc["familiares"]
    story.append(Paragraph("Antecedentes Familiares", styles["Seccion"]))
    if fam["filas"]:
        rows = [[Paragraph(x, styles["Etiqueta"]) for x in ["Parentesco", "Estado", "Edad", "Enfermedades"]]]
        for f in fam["filas"]:
            rows.append([
                Paragraph(f.get("parentesco", ""), styles["Cuerpo"]),
                Paragraph(f.get("estado", ""), styles["Cuerpo"]),
                Paragraph(str(f.get("edad", "")), styles["Cuerpo"]),
                Paragraph(f.get("enfermedades", ""), styles["Cuerpo"]),
            ])
        t = Table(rows, colWidths=(3.2 * cm, 2.6 * cm, 2 * cm, 9.2 * cm))
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BG_SOFT),
            ("LINEBELOW", (0, 0), (-1, 0), 1, ACCENT),
            ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
    else:
        story.append(Paragraph("Sin antecedentes familiares registrados.", styles["Cuerpo"]))
    if fam.get("observaciones"):
        story.append(Spacer(1, 4))
        story.append(Paragraph(fam["observaciones"], styles["Cuerpo"]))

    # ---------- Hábitos psicobiológicos ----------
    hab = hc["habitos"]
    story.append(Paragraph("Hábitos Psicobiológicos", styles["Seccion"]))
    etiquetas_hab = [
        ("tabaquico", "Tabáquicos"), ("oh", "Alcohólicos"), ("cafeico", "Cafeicos"),
        ("alimentario", "Alimentarios"), ("drogas", "Drogas"),
        ("actividad_fisica", "Actividad física"), ("sueno", "Sueño"),
        ("sexuales", "Sexuales"), ("estres", "Situación personal y estrés"),
    ]
    for k, lab in etiquetas_hab:
        v = hab.get(k, "").strip()
        if v:
            story.append(Paragraph(f"<b>{lab}:</b> {v}", styles["Cuerpo"]))

    # ---------- Factores de riesgo CV ----------
    frcv = hc["frcv"]
    if frcv["modificables_sel"] or frcv["no_modificables_sel"] or frcv.get("otros"):
        story.append(Paragraph("Factores de Riesgo Cardiovascular", styles["Seccion"]))
        story.append(Paragraph(f"<b>Modificables:</b> {_lista_a_texto(frcv['modificables_sel']) or '—'}", styles["Cuerpo"]))
        story.append(Paragraph(f"<b>No modificables:</b> {_lista_a_texto(frcv['no_modificables_sel']) or '—'}", styles["Cuerpo"]))
        if frcv.get("otros"):
            story.append(Paragraph(frcv["otros"], styles["Cuerpo"]))

    # ---------- Revisión por sistemas ----------
    story.append(PageBreak())
    story.append(Paragraph("Revisión por Sistemas (Interrogatorio Funcional)", styles["Seccion"]))
    ros = hc["ros"]
    for sec in REVISION_SISTEMAS:
        data = ros[sec["key"]]
        if not data["sintomas"] and not data["detalles"]:
            continue
        story.append(Paragraph(sec["label"], styles["SubSeccion"]))
        if data["sintomas"]:
            story.append(Paragraph(f"Refiere: {_lista_a_texto(data['sintomas'])}.", styles["Cuerpo"]))
        if data["detalles"]:
            story.append(Paragraph(data["detalles"], styles["CuerpoMuted"]))
    negados = [sec["label"] for sec in REVISION_SISTEMAS if not ros[sec["key"]]["sintomas"] and not ros[sec["key"]]["detalles"]]
    if negados:
        story.append(Paragraph("Sistemas sin hallazgos referidos", styles["SubSeccion"]))
        story.append(Paragraph("Niega sintomatología por: " + _lista_a_texto(negados) + ".", styles["CuerpoMuted"]))

    # ---------- Examen físico ----------
    story.append(PageBreak())
    story.append(Paragraph("Examen Físico", styles["Seccion"]))
    sv = hc["examen"]["signos_vitales"]
    story.append(Paragraph("Signos vitales", styles["SubSeccion"]))
    rows = [[
        Paragraph("Temp.", styles["Etiqueta"]), Paragraph("Pulso", styles["Etiqueta"]),
        Paragraph("F.R.", styles["Etiqueta"]), Paragraph("T.A.", styles["Etiqueta"]),
        Paragraph("SpO2", styles["Etiqueta"]), Paragraph("Peso", styles["Etiqueta"]),
        Paragraph("Talla", styles["Etiqueta"]), Paragraph("IMC", styles["Etiqueta"]),
    ]]
    try:
        peso = float(sv.get("peso") or 0)
        talla = float(sv.get("talla") or 0) / 100
        imc = f"{peso / (talla ** 2):.1f}" if peso and talla else "—"
    except (ValueError, ZeroDivisionError):
        imc = "—"
    ta = f"{sv.get('ta_sistolica','—')}/{sv.get('ta_diastolica','—')}"
    rows.append([
        Paragraph(f"{sv.get('temperatura','—')} °C", styles["Cuerpo"]),
        Paragraph(f"{sv.get('pulso','—')} lpm", styles["Cuerpo"]),
        Paragraph(f"{sv.get('fr','—')} rpm", styles["Cuerpo"]),
        Paragraph(f"{ta} mmHg", styles["Cuerpo"]),
        Paragraph(f"{sv.get('spo2','—')} %", styles["Cuerpo"]),
        Paragraph(f"{sv.get('peso','—')} kg", styles["Cuerpo"]),
        Paragraph(f"{sv.get('talla','—')} cm", styles["Cuerpo"]),
        Paragraph(imc, styles["Cuerpo"]),
    ])
    t = Table(rows, colWidths=[2.2 * cm] * 8)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BG_SOFT),
        ("LINEBELOW", (0, 0), (-1, 0), 1, ACCENT),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

    ex = hc["examen"]["sistemas"]
    for sec in EXAMEN_FISICO_SISTEMAS:
        data = ex[sec["key"]]
        if data["estado"] == "No explorado":
            continue
        story.append(Paragraph(sec["label"], styles["SubSeccion"]))
        if data["estado"] == "Normal":
            texto = data["texto"].strip() or sec["normal"]
            story.append(Paragraph(texto, styles["Cuerpo"]))
        else:
            partes = []
            if data["anormales"]:
                partes.append(_lista_a_texto(data["anormales"]) + ".")
            if data["texto"].strip():
                partes.append(data["texto"].strip())
            story.append(Paragraph(" ".join(partes) or "Hallazgos anormales sin especificar.", styles["Cuerpo"]))

    # ---------- Síntesis diagnóstica ----------
    story.append(PageBreak())
    story.append(Paragraph("Síntesis Diagnóstica", styles["Seccion"]))
    sin = hc["sintesis"]
    for lab, key in [
        ("Resumen de datos positivos", "datos_positivos"),
        ("Impresiones diagnósticas / diagnóstico sindromático", "diagnosticos_sindromaticos"),
        ("Observaciones", "observaciones"),
        ("Diagnóstico definitivo", "diagnostico_definitivo"),
        ("Plan / Tratamiento", "plan"),
    ]:
        story.append(Paragraph(lab, styles["SubSeccion"]))
        story.append(Paragraph((sin.get(key, "").strip() or "—").replace("\n", "<br/>"), styles["Cuerpo"]))

    # ---------- Pie ----------
    story.append(Spacer(1, 22))
    story.append(_accent_rule())
    pie = f"Historia clínica generada el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}"
    if medico.get("nombre"):
        pie += f" — {medico['nombre']}"
    if medico.get("servicio"):
        pie += f" · {medico['servicio']}"
    story.append(Paragraph(pie, styles["CuerpoMuted"]))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
