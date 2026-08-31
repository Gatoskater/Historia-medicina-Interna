"""
Generación del PDF final de la Historia Clínica — diseño corporativo
refinado: navy + oro, Playfair Display (títulos) + Inter (cuerpo), ambas
embebidas de verdad (no fuentes base14). Pie de página con crédito de
autoría en cada hoja.
"""

import io
import os
from datetime import date, datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)

from data.campos import (
    REVISION_SISTEMAS, EXAMEN_FISICO_SISTEMAS, MOTIVOS_CONSULTA,
    REFLEJOS_OSTEOTENDINOSOS,
)
from utils.state import APP_AUTHOR, indice_paquete_anio, clasificar_ipa

# ============================================================
# Paleta
# ============================================================
NAVY = colors.HexColor("#101a34")
NAVY_SOFT = colors.HexColor("#2a3660")
GOLD = colors.HexColor("#b0894f")
GOLD_DEEP = colors.HexColor("#8f6d3a")
INK = colors.HexColor("#171a21")
INK_SOFT = colors.HexColor("#5b5f6b")
INK_FAINT = colors.HexColor("#9a9ea8")
LINE = colors.HexColor("#e8e3d6")
GOLD_TINT = colors.HexColor("#f6efe0")

# ============================================================
# Tipografías embebidas
# ============================================================
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_FONTS_DIR = os.path.join(_BASE_DIR, "assets", "fonts")
_FONTS_READY = False


def _asegurar_fuentes():
    global _FONTS_READY
    if _FONTS_READY:
        return
    mapping = {
        "Playfair": "PlayfairDisplay-Regular.ttf",
        "Playfair-Bold": "PlayfairDisplay-Bold.ttf",
        "Playfair-Italic": "PlayfairDisplay-Italic.ttf",
        "Inter": "Inter-Regular.ttf",
        "Inter-Medium": "Inter-Medium.ttf",
        "Inter-SemiBold": "Inter-SemiBold.ttf",
        "Inter-Italic": "Inter-Italic.ttf",
    }
    for name, filename in mapping.items():
        path = os.path.join(_FONTS_DIR, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily(
        "Playfair", normal="Playfair", bold="Playfair-Bold",
        italic="Playfair-Italic", boldItalic="Playfair-Bold",
    )
    pdfmetrics.registerFontFamily(
        "Inter", normal="Inter", bold="Inter-SemiBold",
        italic="Inter-Italic", boldItalic="Inter-SemiBold",
    )
    _FONTS_READY = True


def _styles():
    _asegurar_fuentes()
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle("TituloPortada", parent=ss["Title"], fontName="Playfair-Bold",
                           fontSize=22, textColor=NAVY, spaceAfter=2, alignment=TA_CENTER))
    ss.add(ParagraphStyle("Subtitulo", parent=ss["Normal"], fontName="Inter",
                           fontSize=9.5, textColor=INK_SOFT, alignment=TA_CENTER, spaceAfter=0))
    ss.add(ParagraphStyle("SubtituloItalico", parent=ss["Normal"], fontName="Playfair-Italic",
                           fontSize=12.5, textColor=GOLD_DEEP, alignment=TA_CENTER, spaceAfter=6))
    ss.add(ParagraphStyle("Seccion", parent=ss["Heading1"], fontName="Playfair-Bold",
                           fontSize=13.5, textColor=NAVY, spaceBefore=14, spaceAfter=6))
    ss.add(ParagraphStyle("SubSeccion", parent=ss["Heading2"], fontName="Inter-SemiBold",
                           fontSize=9.6, textColor=GOLD_DEEP, spaceBefore=8, spaceAfter=3))
    ss.add(ParagraphStyle("Cuerpo", parent=ss["Normal"], fontName="Inter",
                           fontSize=9.4, textColor=INK, leading=13.5, alignment=TA_LEFT))
    ss.add(ParagraphStyle("CuerpoMuted", parent=ss["Normal"], fontName="Inter-Italic",
                           fontSize=8.9, textColor=INK_SOFT, leading=12.8))
    ss.add(ParagraphStyle("Etiqueta", parent=ss["Normal"], fontName="Inter-SemiBold",
                           fontSize=8.3, textColor=INK_SOFT))
    ss.add(ParagraphStyle("Footer", parent=ss["Normal"], fontName="Inter",
                           fontSize=7.6, textColor=INK_FAINT))
    return ss


def _accent_rule(color=GOLD, thickness=1.4):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=10)


def _campo(label, value):
    value = value if value not in (None, "") else "—"
    return f"<b>{label}:</b> {value}"


def _tabla_2col(pairs, styles, col_widths=(9 * cm, 8 * cm)):
    rows = [[Paragraph(a, styles["Cuerpo"]), Paragraph(b, styles["Cuerpo"])] for a, b in pairs]
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


def _lista(items):
    return ", ".join(items) if items else ""


def _draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(1.8 * cm, 1.25 * cm, letter[0] - 1.8 * cm, 1.25 * cm)
    canvas.setFont("Inter", 7.6)
    canvas.setFillColor(INK_FAINT)
    canvas.drawString(1.8 * cm, 0.95 * cm,
                       f"Historia Clínica · Medicina Interna — aplicación desarrollada por {APP_AUTHOR}")
    canvas.drawRightString(letter[0] - 1.8 * cm, 0.95 * cm, f"Página {doc.page}")
    canvas.restoreState()


def generar_pdf(hc: dict) -> bytes:
    styles = _styles()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=1.5 * cm, bottomMargin=1.7 * cm,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
        title="Historia Clínica - Medicina Interna",
        author=APP_AUTHOR,
    )
    story = []

    fil = hc["filiacion"]
    medico = hc.get("medico", {})
    nombre_completo = f"{fil.get('nombres','').strip()} {fil.get('apellidos','').strip()}".strip() or "Paciente sin nombre registrado"

    # ---------- Portada ----------
    if medico.get("hospital"):
        story.append(Paragraph(medico["hospital"].upper(), styles["Subtitulo"]))
    story.append(Paragraph("Historia Clínica", styles["TituloPortada"]))
    story.append(Paragraph("Medicina Interna", styles["SubtituloItalico"]))
    story.append(_accent_rule())

    story.append(_tabla_2col([
        (_campo("Paciente", nombre_completo), _campo("C.I.", fil.get("ci", ""))),
        (_campo("Edad", fil.get("edad", "")), _campo("Sexo", fil.get("sexo", ""))),
        (_campo("Fecha de nacimiento", _fmt_fecha(fil.get("fecha_nacimiento"))),
         _campo("Fecha de ingreso", _fmt_fecha(fil.get("fecha_ingreso")))),
        (_campo("Sala / Cama", fil.get("sala_cama", "")), _campo("Ocupación", fil.get("ocupacion", ""))),
    ], styles))
    story.append(Spacer(1, 10))

    # ---------- Filiación ----------
    story.append(Paragraph("Datos de Filiación", styles["Seccion"]))
    story.append(_tabla_2col([
        (_campo("Estado civil", fil.get("estado_civil", "")), _campo("Religión", fil.get("religion", ""))),
        (_campo("Raza", fil.get("raza", "")), _campo("Dominancia", fil.get("dominancia", ""))),
        (_campo("Lugar de nacimiento", fil.get("lugar_nacimiento", "")), _campo("Lugar de procedencia", fil.get("lugar_procedencia", ""))),
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
        "motivo", parent=styles["Cuerpo"], fontName="Playfair-Italic", fontSize=11.5,
    )))
    story.append(Paragraph("Enfermedad Actual", styles["Seccion"]))
    motivos_labels = {m["key"]: m["label"] for m in MOTIVOS_CONSULTA}
    if con.get("motivos_sel"):
        etiquetas = _lista([motivos_labels.get(k, k) for k in con["motivos_sel"]])
        story.append(Paragraph(f"Motivos explorados con guía semiológica: {etiquetas}.", styles["CuerpoMuted"]))
        story.append(Spacer(1, 3))
    story.append(Paragraph((con.get("enfermedad_actual", "").strip() or "—").replace("\n", "<br/>"), styles["Cuerpo"]))

    # ---------- Antecedentes personales ----------
    ant = hc["antecedentes"]
    story.append(Paragraph("Antecedentes Personales", styles["Seccion"]))

    story.append(Paragraph("Médicos — infancia", styles["SubSeccion"]))
    texto = _lista(ant["enf_infancia_sel"]) or "Niega antecedentes relevantes."
    if ant.get("enf_infancia_otros"):
        texto += f" {ant['enf_infancia_otros']}"
    story.append(Paragraph(texto, styles["Cuerpo"]))

    story.append(Paragraph("Médicos — adultez", styles["SubSeccion"]))
    texto = _lista(ant["enf_cronicas_sel"]) or "Niega enfermedades crónicas conocidas."
    if ant.get("enf_cronicas_otros"):
        texto += f" {ant['enf_cronicas_otros']}"
    story.append(Paragraph(texto, styles["Cuerpo"]))

    if ant.get("infecciones"):
        story.append(Paragraph("Infecciones relevantes", styles["SubSeccion"]))
        story.append(Paragraph(ant["infecciones"], styles["Cuerpo"]))

    story.append(Paragraph("Quirúrgicos", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("quirurgicos", "").strip() or "Niega antecedentes quirúrgicos.", styles["Cuerpo"]))

    story.append(Paragraph("Traumatológicos", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("traumatologicos", "").strip() or "Niega antecedentes traumatológicos.", styles["Cuerpo"]))

    story.append(Paragraph("Alérgicos", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("alergicos", "").strip() or "Niega alergias conocidas.", styles["Cuerpo"]))

    story.append(Paragraph("Enfermedades de transmisión sexual", styles["SubSeccion"]))
    texto = _lista(ant["ets_sel"]) or "Niega antecedentes de ETS."
    if ant.get("ets_otros"):
        texto += f" {ant['ets_otros']}"
    story.append(Paragraph(texto, styles["Cuerpo"]))

    story.append(Paragraph("Transfusionales", styles["SubSeccion"]))
    story.append(Paragraph(ant.get("transfusionales", "").strip() or "Niega transfusiones previas.", styles["Cuerpo"]))

    gineco_pairs = [
        ("Menarquia", ant.get("gineco_menarquia", "")), ("Fórmula obstétrica", ant.get("gineco_formula", "")),
        ("FUR", ant.get("gineco_fur", "")), ("Método anticonceptivo", ant.get("gineco_mac", "")),
        ("Menopausia", ant.get("gineco_menopausia", "")), ("Procedimientos", ant.get("gineco_procedimientos", "")),
    ]
    if any(v for _, v in gineco_pairs) or ant.get("gineco_sx_menstruales"):
        story.append(Paragraph("Ginecoobstétricos", styles["SubSeccion"]))
        story.append(_tabla_2col([
            (_campo(gineco_pairs[0][0], gineco_pairs[0][1]), _campo(gineco_pairs[1][0], gineco_pairs[1][1])),
            (_campo(gineco_pairs[2][0], gineco_pairs[2][1]), _campo(gineco_pairs[3][0], gineco_pairs[3][1])),
            (_campo(gineco_pairs[4][0], gineco_pairs[4][1]), _campo(gineco_pairs[5][0], gineco_pairs[5][1])),
        ], styles))
        if ant.get("gineco_sx_menstruales"):
            story.append(Paragraph(ant["gineco_sx_menstruales"], styles["Cuerpo"]))

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
            ("BACKGROUND", (0, 0), (-1, 0), GOLD_TINT),
            ("LINEBELOW", (0, 0), (-1, 0), 1, GOLD),
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

    tab = hab["tabaquico"]
    story.append(Paragraph("Tabáquicos", styles["SubSeccion"]))
    if tab.get("fuma") or (tab.get("cigarrillos_dia") or 0) > 0:
        ipa = indice_paquete_anio(tab)
        clasif, _ = clasificar_ipa(ipa)
        linea = (f"Fumador de {tab.get('cigarrillos_dia', 0)} cigarrillos/día durante {tab.get('anios_fumando', 0)} años "
                 f"— Índice paquete-año: <b>{ipa}</b> ({clasif}).")
        if tab.get("exfumador"):
            linea += f" Exfumador desde hace {tab.get('anios_desde_dejo', 0)} años."
        story.append(Paragraph(linea, styles["Cuerpo"]))
        if tab.get("notas"):
            story.append(Paragraph(tab["notas"], styles["CuerpoMuted"]))
    else:
        story.append(Paragraph(tab.get("notas") or "Niega hábito tabáquico.", styles["Cuerpo"]))

    for key, label in [("oh", "Alcohólicos"), ("cafeico", "Cafeicos"), ("alimentario", "Alimentarios"),
                        ("drogas", "Drogas"), ("actividad_fisica", "Actividad física"), ("sueno", "Sueño"),
                        ("sexuales", "Sexuales"), ("estres", "Situación personal y estrés")]:
        v = hab.get(key, "").strip()
        if v:
            story.append(Paragraph(f"<b>{label}:</b> {v}", styles["Cuerpo"]))

    # ---------- FRCV ----------
    frcv = hc["frcv"]
    if frcv["modificables_sel"] or frcv["no_modificables_sel"] or frcv.get("otros"):
        story.append(Paragraph("Factores de Riesgo Cardiovascular", styles["Seccion"]))
        story.append(Paragraph(f"<b>Modificables:</b> {_lista(frcv['modificables_sel']) or '—'}", styles["Cuerpo"]))
        story.append(Paragraph(f"<b>No modificables:</b> {_lista(frcv['no_modificables_sel']) or '—'}", styles["Cuerpo"]))
        if frcv.get("otros"):
            story.append(Paragraph(frcv["otros"], styles["Cuerpo"]))

    # ---------- Revisión por sistemas ----------
    story.append(PageBreak())
    story.append(Paragraph("Revisión por Sistemas", styles["Seccion"]))
    ros = hc["ros"]
    for sec in REVISION_SISTEMAS:
        data = ros[sec["key"]]
        if not data["sintomas"] and not data["detalles"]:
            continue
        story.append(Paragraph(sec["label"], styles["SubSeccion"]))
        if data["sintomas"]:
            story.append(Paragraph(f"Refiere: {_lista(data['sintomas'])}.", styles["Cuerpo"]))
        if data["detalles"]:
            story.append(Paragraph(data["detalles"], styles["CuerpoMuted"]))
    negados = [sec["label"] for sec in REVISION_SISTEMAS if not ros[sec["key"]]["sintomas"] and not ros[sec["key"]]["detalles"]]
    if negados:
        story.append(Paragraph("Sistemas sin hallazgos referidos", styles["SubSeccion"]))
        story.append(Paragraph("Niega sintomatología por: " + _lista(negados) + ".", styles["CuerpoMuted"]))

    # ---------- Examen físico ----------
    story.append(PageBreak())
    story.append(Paragraph("Examen Físico", styles["Seccion"]))
    sv = hc["examen"]["signos_vitales"]
    story.append(Paragraph("Signos vitales", styles["SubSeccion"]))
    rows = [[Paragraph(x, styles["Etiqueta"]) for x in ["Temp.", "Pulso", "F.R.", "T.A.", "SpO2", "Peso", "Talla", "IMC"]]]
    try:
        peso = float(sv.get("peso") or 0)
        talla = float(sv.get("talla") or 0) / 100
        imc = f"{peso / (talla ** 2):.1f}" if peso and talla else "—"
    except (ValueError, ZeroDivisionError):
        imc = "—"
    def _v(k):
        return sv.get(k) or "—"

    ta_s, ta_d = sv.get("ta_sistolica"), sv.get("ta_diastolica")
    ta = f"{ta_s}/{ta_d}" if (ta_s or ta_d) else "—"
    rows.append([
        Paragraph(f"{_v('temperatura')} °C", styles["Cuerpo"]),
        Paragraph(f"{_v('pulso')} lpm", styles["Cuerpo"]),
        Paragraph(f"{_v('fr')} rpm", styles["Cuerpo"]),
        Paragraph(f"{ta} mmHg" if ta != "—" else "—", styles["Cuerpo"]),
        Paragraph(f"{_v('spo2')} %", styles["Cuerpo"]),
        Paragraph(f"{_v('peso')} kg", styles["Cuerpo"]),
        Paragraph(f"{_v('talla')} cm", styles["Cuerpo"]),
        Paragraph(imc, styles["Cuerpo"]),
    ])
    t = Table(rows, colWidths=[2.2 * cm] * 8)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GOLD_TINT),
        ("LINEBELOW", (0, 0), (-1, 0), 1, GOLD),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

    ex = hc["examen"]["sistemas"]
    extra = hc["examen"].get("extra", {})
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
                partes.append(_lista(data["anormales"]) + ".")
            if data["texto"].strip():
                partes.append(data["texto"].strip())
            story.append(Paragraph(" ".join(partes) or "Hallazgos anormales sin especificar.", styles["Cuerpo"]))

        # --- Hallazgos estructurados adicionales por sistema ---
        if sec["key"] == "piel":
            fp = extra.get("piel", {}).get("fitzpatrick", "No evaluado")
            if fp != "No evaluado":
                story.append(Paragraph(f"Fototipo de Fitzpatrick: {fp}.", styles["CuerpoMuted"]))
        elif sec["key"] == "ojos":
            o = extra.get("ojos", {})
            partes = []
            if o.get("fotomotor", "No evaluado") != "No evaluado":
                partes.append(f"Reflejo fotomotor {o['fotomotor'].lower()}")
            if o.get("convergencia", "No evaluado") != "No evaluado":
                partes.append(f"convergencia {o['convergencia'].lower()}")
            if partes:
                story.append(Paragraph(_lista(partes) + ".", styles["CuerpoMuted"]))
        elif sec["key"] == "oidos":
            o = extra.get("oidos", {})
            partes = []
            if o.get("weber", "No realizado") != "No realizado":
                partes.append(f"Weber: {o['weber']}")
            if o.get("rinne", "No realizado") != "No realizado":
                partes.append(f"Rinne: {o['rinne']}")
            if partes:
                story.append(Paragraph(_lista(partes) + ".", styles["CuerpoMuted"]))
        elif sec["key"] == "abdomen":
            a = extra.get("abdomen", {})
            maniobras = []
            for k, lab in [("murphy", "Murphy"), ("blumberg", "Blumberg"), ("mcburney", "McBurney"), ("rovsing", "Rovsing")]:
                if a.get(k, "No evaluado") != "No evaluado":
                    maniobras.append(f"{lab} {a[k].lower()}")
            if maniobras:
                story.append(Paragraph("Signos: " + _lista(maniobras) + ".", styles["CuerpoMuted"]))
            pp = []
            if a.get("puno_percusion_der", "No evaluado") != "No evaluado":
                pp.append(f"derecha {a['puno_percusion_der'].lower()}")
            if a.get("puno_percusion_izq", "No evaluado") != "No evaluado":
                pp.append(f"izquierda {a['puno_percusion_izq'].lower()}")
            if pp:
                story.append(Paragraph("Puño percusión: " + _lista(pp) + ".", styles["CuerpoMuted"]))
        elif sec["key"] == "neurologico":
            n = extra.get("neurologico", {})
            reflejos_txt = [f"{r} {g.split(' ')[0]}" for r, g in n.get("reflejos", {}).items() if g != "No evaluado"]
            if reflejos_txt:
                story.append(Paragraph("Reflejos osteotendinosos: " + _lista(reflejos_txt) + ".", styles["CuerpoMuted"]))
            if n.get("signos_meningeos"):
                story.append(Paragraph("Signos meníngeos presentes: " + _lista(n["signos_meningeos"]) + ".", styles["CuerpoMuted"]))
            if not n.get("pares_craneales_normal", True) and n.get("pares_craneales_detalle"):
                story.append(Paragraph(f"Pares craneales: {n['pares_craneales_detalle']}", styles["CuerpoMuted"]))

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

    story.append(Spacer(1, 18))
    story.append(_accent_rule(color=LINE, thickness=1))
    pie = f"Historia clínica generada el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}"
    if medico.get("nombre"):
        pie += f" — {medico['nombre']}"
    if medico.get("servicio"):
        pie += f" · {medico['servicio']}"
    story.append(Paragraph(pie, styles["CuerpoMuted"]))

    doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)
    buffer.seek(0)
    return buffer.getvalue()
