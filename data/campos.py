"""
Contenido clínico de la Historia Clínica — Medicina Interna (v2).
Basado en: formato del Hospital Vargas de Caracas, historia redactada de
referencia, y el guion de interrogatorio/examen físico del usuario.
Todo el "qué preguntar / qué explorar" vive aquí, separado de la UI.
"""

# ============================================================
# ANTECEDENTES PERSONALES
# ============================================================
ENF_INFANCIA = [
    "Sarampión", "Rubéola", "Varicela", "Parotiditis", "Tos ferina",
    "Escarlatina", "Mononucleosis infecciosa", "Difteria", "Poliomielitis",
    "Fiebre reumática", "Dengue",
]

ENF_CRONICAS_ADULTO = [
    "Hipertensión arterial", "Diabetes mellitus", "Enfermedad renal crónica",
    "Asma", "EPOC", "Cardiopatía isquémica", "Infarto de miocardio",
    "Insuficiencia cardíaca", "Enfermedad cerebrovascular", "Hipotiroidismo",
    "Hipertiroidismo", "Dislipidemia", "Enfermedad hepática crónica",
    "Anemia", "Enfermedad autoinmune", "Cáncer", "Tuberculosis",
    "VIH", "COVID-19", "Enfermedad psiquiátrica",
]

ETS = ["Sífilis", "Gonorrea", "VPH", "Hepatitis B", "Hepatitis C", "VIH", "Herpes genital"]

CAMPOS_ANTECEDENTES_LIBRES = {
    "infecciones": {
        "label": "Infecciones relevantes o recurrentes",
        "placeholder": "Ej. Infecciones urinarias a repetición, neumonías previas...",
        "help": "Distinto de las enfermedades de la infancia: procesos infecciosos que se repiten o marcaron su historia médica.",
    },
    "quirurgicos": {
        "label": "Antecedentes quirúrgicos",
        "placeholder": "Ej. Apendicectomía en 2019, sin complicaciones.",
        "help": "Tipo de cirugía, año, motivo y si hubo complicaciones.",
    },
    "traumatologicos": {
        "label": "Antecedentes traumatológicos",
        "placeholder": "Ej. Fractura de muñeca izquierda en 2015 por caída, tratada con yeso.",
        "help": "Fracturas, caídas, esguinces o lesiones relevantes y su tratamiento.",
    },
    "alergicos": {
        "label": "Alérgicos",
        "placeholder": "Ej. Alergia a la penicilina (rash cutáneo); niega alergias alimentarias.",
        "help": "Medicamentos, alimentos u otros alérgenos, y el tipo de reacción presentada.",
    },
    "transfusionales": {
        "label": "Transfusionales",
        "placeholder": "Ej. 2 transfusiones de concentrado globular en 2023 por anemia, sin reacciones.",
        "help": "Número de transfusiones, motivo, y si hubo reacciones transfusionales.",
    },
    "inmunologicos": {
        "label": "Inmunológicos (vacunación)",
        "placeholder": "Ej. Esquema de vacunación completo; refuerzo de tétanos en 2022.",
        "help": "Esquema de vacunación de la infancia y adultez; vacunas pendientes o incompletas.",
    },
    "medicamentos": {
        "label": "Medicamentos actuales",
        "placeholder": "Ej. Losartán 50mg VO OD, Metformina 850mg VO BID.",
        "help": "Fármaco, dosis, frecuencia y vía. Incluye anticonceptivos y suplementos.",
    },
    "epidemiologicos": {
        "label": "Epidemiológicos",
        "placeholder": "Ej. Vivienda con 3 habitaciones, servicios básicos completos, convive con 4 personas y 1 mascota.",
        "help": "Tipo de vivienda, disposición de excretas, servicios básicos, convivientes, mascotas, viajes recientes.",
    },
}

CAMPOS_GINECOOBSTETRICOS = {
    "menarquia": {"label": "Menarquia", "placeholder": "Ej. 12 años"},
    "formula": {"label": "Fórmula obstétrica (G_P_A_C_)", "placeholder": "Ej. G2 P1 A1 C0"},
    "fur": {"label": "Fecha de última regla (FUR)", "placeholder": "Ej. 15/07/2026"},
    "mac": {"label": "Método anticonceptivo", "placeholder": "Ej. Anticonceptivos orales combinados"},
    "menopausia": {"label": "Menopausia", "placeholder": "Ej. No aplica / A los 50 años"},
    "sx_menstruales": {"label": "Síntomas menstruales / ciclo", "placeholder": "Ej. Ciclos regulares cada 28 días, sin dismenorrea."},
    "procedimientos": {"label": "Procedimientos ginecológicos", "placeholder": "Ej. Biopsia cervical en 2022, resultado benigno."},
}

PARENTESCOS_FAMILIARES = [
    "Madre", "Padre", "Hermano(a)", "Abuelo(a) materno(a)",
    "Abuelo(a) paterno(a)", "Tío(a)", "Hijo(a)",
]

ENF_FAMILIARES_FRECUENTES = [
    "Hipertensión arterial", "Diabetes mellitus", "Cáncer",
    "Cardiopatías", "Enfermedad renal", "Enfermedad autoinmune",
    "Enfermedad psiquiátrica", "Enfermedad tiroidea", "Dislipidemia",
    "Muerte súbita / cardíaca temprana",
]

# ============================================================
# HÁBITOS PSICOBIOLÓGICOS
# ============================================================
HABITOS_CAMPOS = [
    ("oh", "Alcohólicos", "Tipo de bebida, frecuencia, cantidad, ¿llega a la embriaguez?", "Ej. Cerveza los fines de semana, 3-4 unidades, sin llegar a la embriaguez."),
    ("cafeico", "Cafeicos", "Tazas al día, con o sin azúcar", "Ej. 2 tazas de café al día, con 1 cucharada de azúcar."),
    ("alimentario", "Alimentarios", "Número de comidas, tipo de dieta, predominio, cantidades", "Ej. 3 comidas al día, dieta balanceada con predominio de carbohidratos."),
    ("drogas", "Drogas ilícitas", "Tipo, dónde y cuántas, frecuencia, vía", "Ej. Niega consumo de drogas ilícitas."),
    ("actividad_fisica", "Actividad física / Ejercicio", "Tipo, frecuencia, duración, adecuado o sedentario", "Ej. Sedentario, no realiza actividad física de forma regular."),
    ("sueno", "Sueño", "Horas, continuo o interrumpido, matutino/vespertino/diurno", "Ej. 6-7 horas nocturnas continuas, sin dificultad para conciliar el sueño."),
    ("sexuales", "Sexuales", "Vida sexual activa, número de parejas, protección", "Ej. Vida sexual activa, pareja única, uso de preservativo."),
    ("estres", "Situación personal y estrés", "Fuentes de estrés, manejo", "Ej. Refiere estrés académico moderado, sin estrategias de manejo activas."),
]

CLASIFICACION_IPA = [
    (0, 0, "Sin hábito relevante", "gray"),
    (0.01, 9.99, "Leve", "blue"),
    (10, 19.99, "Moderado", "orange"),
    (20, 10_000, "Severo", "red"),
]

# ============================================================
# FACTORES DE RIESGO CARDIOVASCULAR
# ============================================================
FRCV_MODIFICABLES = [
    "Hipertensión arterial", "Diabetes mellitus", "Dislipidemia",
    "Tabaquismo", "Obesidad / sobrepeso", "Sedentarismo",
    "Dieta rica en sodio/grasas", "Consumo de alcohol", "Estrés crónico",
    "Enfermedad renal crónica",
]
FRCV_NO_MODIFICABLES = [
    "Edad (hombre ≥45 / mujer ≥55 años)", "Sexo masculino",
    "Antecedente familiar de cardiopatía temprana",
    "Menopausia precoz", "Carga genética",
]

# ============================================================
# MOTIVOS DE CONSULTA FRECUENTES — asistente guiado para Enfermedad Actual
# Cada síntoma trae sus propios sub-campos de caracterización semiológica.
# ============================================================
MOTIVOS_CONSULTA = [
    {
        "key": "dolor", "label": "Dolor", "icono": "⚡",
        "mnemonico": "ALICIDPH — Aparición, Localización, Irradiación, Carácter, Intensidad, Duración, Periodicidad, Horario",
        "campos": [
            {"key": "aparicion", "label": "Aparición", "tipo": "text", "placeholder": "Ej. Inicio súbito hace 6 horas, en reposo", "help": "¿Cómo y cuándo comenzó? ¿Súbito o progresivo?"},
            {"key": "localizacion", "label": "Localización", "tipo": "text", "placeholder": "Ej. Epigastrio", "help": "¿Dónde exactamente lo siente el paciente?"},
            {"key": "irradiacion", "label": "Irradiación", "tipo": "text", "placeholder": "Ej. Hacia el hombro derecho / No se irradia", "help": "¿Se corre hacia otra parte del cuerpo?"},
            {"key": "caracter", "label": "Carácter", "tipo": "select", "opciones": ["Punzante", "Opresivo", "Cólico", "Urente", "Pulsátil", "Sordo", "Lacerante", "Tipo cólico"], "help": "¿Cómo describe el paciente la sensación?"},
            {"key": "intensidad", "label": "Intensidad (EVA 0-10)", "tipo": "slider", "help": "Escala Visual Análoga del dolor."},
            {"key": "duracion", "label": "Duración", "tipo": "text", "placeholder": "Ej. Episodios de 20-30 minutos", "help": "¿Cuánto dura cada episodio?"},
            {"key": "periodicidad", "label": "Periodicidad", "tipo": "select", "opciones": ["Continuo", "Intermitente", "Recidivante"], "help": ""},
            {"key": "horario", "label": "Horario / predominio", "tipo": "text", "placeholder": "Ej. Predominio postprandial", "help": "¿Hay un momento del día en que predomina?"},
            {"key": "atenuantes", "label": "Atenuantes / Agravantes", "tipo": "text", "placeholder": "Ej. Mejora con el ayuno, empeora con la ingesta de grasas", "help": "¿Qué lo alivia? ¿Qué lo empeora?"},
            {"key": "concomitantes", "label": "Síntomas concomitantes", "tipo": "text", "placeholder": "Ej. Náuseas, diaforesis, palidez", "help": "¿Qué otros síntomas aparecen junto al dolor?"},
        ],
    },
    {
        "key": "fiebre", "label": "Fiebre", "icono": "🌡️",
        "mnemonico": "Aparición, cuantificación, escalofríos, horario, periodicidad, atenuantes",
        "campos": [
            {"key": "aparicion", "label": "Aparición", "tipo": "text", "placeholder": "Ej. Hace 3 días", "help": "¿Cuándo empezó?"},
            {"key": "cuantificacion", "label": "¿Logró cuantificarla?", "tipo": "text", "placeholder": "Ej. 38.5 °C axilar", "help": "Temperatura máxima registrada, si la midió."},
            {"key": "escalofrios", "label": "¿Precedida de escalofríos?", "tipo": "select", "opciones": ["Sí", "No"], "help": ""},
            {"key": "horario", "label": "Horario / predominio", "tipo": "text", "placeholder": "Ej. Predominio vespertino", "help": "¿A qué hora del día predomina?"},
            {"key": "periodicidad", "label": "Periodicidad", "tipo": "select", "opciones": ["Continua", "Intermitente", "Recidivante", "Remitente"], "help": ""},
            {"key": "atenuantes", "label": "Atenuantes", "tipo": "text", "placeholder": "Ej. Cede parcialmente con acetaminofén", "help": "¿Qué la hace ceder?"},
            {"key": "concomitantes", "label": "Síntomas concomitantes", "tipo": "text", "placeholder": "Ej. Diaforesis, mialgias, artralgias", "help": ""},
        ],
    },
    {
        "key": "tos", "label": "Tos", "icono": "😮‍💨",
        "mnemonico": "Tiempo de evolución, tipo, esputo, horario, desencadenantes",
        "campos": [
            {"key": "evolucion", "label": "Tiempo de evolución", "tipo": "text", "placeholder": "Ej. 5 días", "help": ""},
            {"key": "tipo", "label": "Tipo", "tipo": "select", "opciones": ["Seca", "Productiva"], "help": "¿Húmeda/productiva o seca?"},
            {"key": "esputo", "label": "Características del esputo", "tipo": "text", "placeholder": "Ej. Blanquecino, escasa cantidad", "help": "Color, cantidad, olor (si es productiva)."},
            {"key": "horario", "label": "Horario / periodicidad", "tipo": "text", "placeholder": "Ej. Predominio nocturno", "help": ""},
            {"key": "desencadenantes", "label": "Desencadenantes", "tipo": "text", "placeholder": "Ej. Decúbito, esfuerzo, cambios de temperatura", "help": ""},
            {"key": "concomitantes", "label": "Síntomas concomitantes", "tipo": "text", "placeholder": "Ej. Disnea, dolor torácico, fiebre", "help": ""},
        ],
    },
    {
        "key": "disnea", "label": "Disnea", "icono": "🫁",
        "mnemonico": "Relación con el esfuerzo, clase funcional, ortopnea, DPN",
        "campos": [
            {"key": "relacion_esfuerzo", "label": "Relación con el esfuerzo", "tipo": "select", "opciones": ["De reposo", "De esfuerzo", "Ortopnea", "Disnea paroxística nocturna"], "help": ""},
            {"key": "clase_funcional", "label": "Clase funcional (NYHA)", "tipo": "select", "opciones": ["I — sin limitación", "II — limitación leve", "III — limitación marcada", "IV — síntomas en reposo"], "help": "Clasificación funcional de la New York Heart Association."},
            {"key": "evolucion", "label": "Tiempo de evolución", "tipo": "text", "placeholder": "Ej. Progresiva en los últimos 2 meses", "help": ""},
            {"key": "desencadenantes", "label": "Desencadenantes", "tipo": "text", "placeholder": "Ej. Subir escaleras, decúbito", "help": ""},
            {"key": "concomitantes", "label": "Síntomas concomitantes", "tipo": "text", "placeholder": "Ej. Palpitaciones, edema en miembros inferiores, tos", "help": ""},
        ],
    },
    {
        "key": "diarrea", "label": "Diarrea", "icono": "🚰",
        "mnemonico": "Frecuencia, consistencia, moco/sangre, desencadenante",
        "campos": [
            {"key": "evolucion", "label": "Tiempo de evolución", "tipo": "text", "placeholder": "Ej. 2 días", "help": ""},
            {"key": "num_evacuaciones", "label": "Número de evacuaciones/día", "tipo": "text", "placeholder": "Ej. 5-6 veces al día", "help": ""},
            {"key": "consistencia", "label": "Consistencia", "tipo": "select", "opciones": ["Líquida", "Semilíquida", "Pastosa"], "help": ""},
            {"key": "color", "label": "Color / características", "tipo": "text", "placeholder": "Ej. Amarillenta, sin restos alimentarios", "help": ""},
            {"key": "moco_sangre", "label": "¿Moco o sangre?", "tipo": "select", "opciones": ["No", "Moco", "Sangre", "Moco y sangre"], "help": ""},
            {"key": "desencadenante", "label": "Desencadenante", "tipo": "text", "placeholder": "Ej. Ingesta de alimentos en la calle", "help": "¿Alimento sospechoso, viaje reciente, contacto con enfermos?"},
            {"key": "concomitantes", "label": "Síntomas concomitantes", "tipo": "text", "placeholder": "Ej. Dolor abdominal tipo cólico, fiebre, náuseas", "help": ""},
        ],
    },
    {
        "key": "vomitos", "label": "Vómitos / Náuseas", "icono": "🤢",
        "mnemonico": "Náuseas previas, contenido, cantidad, relación con la ingesta",
        "campos": [
            {"key": "nauseas_previas", "label": "¿Precedidos de náuseas?", "tipo": "select", "opciones": ["Sí", "No"], "help": ""},
            {"key": "num_episodios", "label": "Número de episodios", "tipo": "text", "placeholder": "Ej. 8 episodios en 24 horas", "help": ""},
            {"key": "contenido", "label": "Contenido", "tipo": "select", "opciones": ["Alimentario", "Bilioso", "Hemático", "Fecaloideo"], "help": ""},
            {"key": "cantidad", "label": "Cantidad aproximada", "tipo": "text", "placeholder": "Ej. Abundante, ~200 mL por episodio", "help": ""},
            {"key": "horario", "label": "Relación con la ingesta / horario", "tipo": "text", "placeholder": "Ej. Postprandial inmediato", "help": ""},
            {"key": "concomitantes", "label": "Síntomas concomitantes", "tipo": "text", "placeholder": "Ej. Dolor abdominal, mareos, fiebre", "help": ""},
        ],
    },
    {
        "key": "cefalea", "label": "Cefalea", "icono": "🧠",
        "mnemonico": "Localización, carácter, intensidad, síntomas asociados",
        "campos": [
            {"key": "localizacion", "label": "Localización", "tipo": "text", "placeholder": "Ej. Holocraneana / Hemicraneana derecha", "help": ""},
            {"key": "caracter", "label": "Carácter", "tipo": "select", "opciones": ["Opresivo", "Pulsátil", "Punzante", "Tipo peso"], "help": ""},
            {"key": "intensidad", "label": "Intensidad (EVA 0-10)", "tipo": "slider", "help": ""},
            {"key": "duracion", "label": "Duración / frecuencia", "tipo": "text", "placeholder": "Ej. Episodios de 4-6 horas, 2 veces por semana", "help": ""},
            {"key": "asociados", "label": "Síntomas asociados", "tipo": "text", "placeholder": "Ej. Náuseas, fotofobia, fonofobia", "help": "¿Náuseas, fotofobia, fonofobia, aura visual?"},
            {"key": "desencadenantes", "label": "Desencadenantes", "tipo": "text", "placeholder": "Ej. Estrés, ayuno prolongado, poco sueño", "help": ""},
        ],
    },
    {
        "key": "edema", "label": "Edema", "icono": "💧",
        "mnemonico": "Localización, godet/fóvea, horario",
        "campos": [
            {"key": "localizacion", "label": "Localización", "tipo": "text", "placeholder": "Ej. Miembros inferiores, bilateral, hasta el tercio medio de la pierna", "help": ""},
            {"key": "fovea", "label": "Godet / Fóvea", "tipo": "select", "opciones": ["Ausente", "Presente (+)", "Presente (++)", "Presente (+++)", "Presente (++++)"], "help": "Grado de fóvea a la digitopresión."},
            {"key": "horario", "label": "Horario / periodicidad", "tipo": "select", "opciones": ["Vespertino", "Matutino", "Constante"], "help": ""},
            {"key": "concomitantes", "label": "Signos concomitantes", "tipo": "text", "placeholder": "Ej. Disnea, ortopnea, aumento de peso", "help": ""},
        ],
    },
    {
        "key": "sincope", "label": "Pérdida de conciencia / Convulsión", "icono": "🌀",
        "mnemonico": "Pródromo, duración, esfínteres, recuperación",
        "campos": [
            {"key": "prodromo", "label": "Pródromo", "tipo": "text", "placeholder": "Ej. Mareo y visión borrosa previos", "help": "¿Hubo síntomas antes del episodio?"},
            {"key": "duracion", "label": "Duración", "tipo": "text", "placeholder": "Ej. Aproximadamente 30 segundos", "help": ""},
            {"key": "esfinteres", "label": "Relajación de esfínteres", "tipo": "select", "opciones": ["Sí", "No"], "help": ""},
            {"key": "movimientos", "label": "Movimientos anormales / convulsión", "tipo": "text", "placeholder": "Ej. Movimientos tónico-clónicos generalizados", "help": "Focal o generalizada; describir si hubo."},
            {"key": "recuperacion", "label": "Recuperación", "tipo": "text", "placeholder": "Ej. Recuperación inmediata sin confusión / con periodo postictal de 10 min", "help": ""},
            {"key": "desencadenante", "label": "Desencadenante", "tipo": "text", "placeholder": "Ej. Bipedestación prolongada, esfuerzo, emoción intensa", "help": ""},
        ],
    },
    {
        "key": "palpitaciones", "label": "Palpitaciones", "icono": "💓",
        "mnemonico": "Inicio/término, ritmo percibido, duración, desencadenantes",
        "campos": [
            {"key": "inicio_termino", "label": "Forma de inicio y término", "tipo": "select", "opciones": ["Súbito", "Gradual"], "help": ""},
            {"key": "ritmo", "label": "Ritmo percibido", "tipo": "select", "opciones": ["Regular", "Irregular"], "help": ""},
            {"key": "duracion", "label": "Duración", "tipo": "text", "placeholder": "Ej. Episodios de 5-10 minutos", "help": ""},
            {"key": "desencadenantes", "label": "Desencadenantes", "tipo": "text", "placeholder": "Ej. Esfuerzo, café, estrés", "help": ""},
            {"key": "concomitantes", "label": "Síntomas concomitantes", "tipo": "text", "placeholder": "Ej. Dolor torácico, disnea, síncope", "help": ""},
        ],
    },
]

# ============================================================
# REVISIÓN POR SISTEMAS (interrogatorio funcional)
# ============================================================
REVISION_SISTEMAS = [
    {
        "key": "general", "label": "Generales", "icono": "🩺",
        "guia": "Pregunta siempre por estos aunque el motivo de consulta sea otro: orientan hacia procesos sistémicos.",
        "sintomas": ["Fiebre", "Pérdida de peso", "Aumento de peso", "Astenia", "Anorexia",
                     "Diaforesis / sudoración nocturna", "Escalofríos", "Malestar general"],
    },
    {
        "key": "piel", "label": "Piel y anexos", "icono": "🧴",
        "guia": "Incluye cabello y uñas, no solo piel.",
        "sintomas": ["Prurito", "Erupciones / rash", "Cambios de coloración", "Caída del cabello",
                     "Resequedad", "Edema", "Cicatrización lenta", "Aparición de nódulos o lesiones",
                     "Cambios en lunares"],
    },
    {
        "key": "cabeza", "label": "Cabeza", "icono": "🧠",
        "guia": "",
        "sintomas": ["Cefalea", "Mareos", "Síncope", "Traumatismos craneales"],
    },
    {
        "key": "ojos", "label": "Ojos", "icono": "👁️",
        "guia": "",
        "sintomas": ["Disminución de agudeza visual", "Visión borrosa", "Diplopía", "Fotofobia",
                     "Dolor ocular", "Lagrimeo excesivo / xeroftalmia", "Secreción",
                     "Sensación de cuerpo extraño", "Uso de lentes correctivos"],
    },
    {
        "key": "oidos", "label": "Oídos", "icono": "👂",
        "guia": "",
        "sintomas": ["Hipoacusia", "Tinnitus", "Vértigo", "Otalgia", "Otorrea",
                     "Sensación de plenitud auricular"],
    },
    {
        "key": "nariz", "label": "Nariz", "icono": "👃",
        "guia": "",
        "sintomas": ["Obstrucción nasal", "Epistaxis", "Rinorrea", "Estornudos",
                     "Anosmia / hiposmia", "Dolor en senos paranasales"],
    },
    {
        "key": "boca_garganta", "label": "Boca y garganta", "icono": "🦷",
        "guia": "En disfagia, siempre precisar si es a líquidos, a sólidos o a ambos.",
        "sintomas": ["Odontalgia", "Odinofagia", "Disfagia (líquidos y/o sólidos)", "Ronquera / disfonía",
                     "Sangrado gingival", "Halitosis", "Lesiones orales", "Alteración del gusto"],
    },
    {
        "key": "cuello", "label": "Cuello", "icono": "🧣",
        "guia": "",
        "sintomas": ["Masas cervicales", "Dolor cervical", "Rigidez", "Adenopatías palpables"],
    },
    {
        "key": "respiratorio", "label": "Respiratorio", "icono": "🫁",
        "guia": "",
        "sintomas": ["Tos seca", "Tos productiva", "Disnea", "Sibilancias",
                     "Dolor torácico pleurítico", "Hemoptisis", "Ortopnea"],
    },
    {
        "key": "cardiovascular", "label": "Cardiovascular", "icono": "❤️",
        "guia": "",
        "sintomas": ["Dolor torácico", "Palpitaciones", "Disnea de esfuerzo",
                     "Disnea paroxística nocturna", "Ortopnea", "Edema en miembros inferiores",
                     "Claudicación intermitente", "Síncope", "Cianosis"],
    },
    {
        "key": "gastrointestinal", "label": "Gastrointestinal", "icono": "🍽️",
        "guia": "Precisa siempre el hábito intestinal: frecuencia, forma, color y consistencia.",
        "sintomas": ["Dolor abdominal", "Náuseas", "Vómitos", "Diarrea", "Estreñimiento",
                     "Pirosis", "Disfagia", "Hematemesis", "Melena", "Rectorragia", "Ictericia",
                     "Distensión abdominal", "Cambios en el apetito", "Intolerancia alimentaria"],
    },
    {
        "key": "genitourinario", "label": "Genitourinario", "icono": "🚻",
        "guia": "",
        "sintomas": ["Disuria", "Hematuria", "Polaquiuria", "Nicturia", "Incontinencia urinaria",
                     "Urgencia miccional", "Tenesmo vesical", "Secreción uretral", "Dolor lumbar",
                     "Disminución del calibre del chorro urinario", "Esfuerzo miccional",
                     "Espuma en la orina"],
    },
    {
        "key": "ginecologico", "label": "Ginecológico (si aplica)", "icono": "♀️",
        "guia": "",
        "sintomas": ["Alteraciones del ciclo menstrual", "Dismenorrea", "Sangrado intermenstrual",
                     "Flujo vaginal anormal", "Dispareunia", "Síntomas de menopausia",
                     "Masa o dolor mamario"],
    },
    {
        "key": "endocrino", "label": "Endocrino", "icono": "⚖️",
        "guia": "",
        "sintomas": ["Intolerancia al frío", "Intolerancia al calor", "Poliuria", "Polidipsia",
                     "Polifagia", "Cambios de peso inexplicados", "Hirsutismo", "Temblor fino"],
    },
    {
        "key": "hematologico", "label": "Hematológico", "icono": "🩸",
        "guia": "",
        "sintomas": ["Equimosis fáciles", "Sangrado prolongado", "Palidez",
                     "Adenopatías generalizadas", "Petequias"],
    },
    {
        "key": "musculoesqueletico", "label": "Osteomuscular", "icono": "🦴",
        "guia": "",
        "sintomas": ["Artralgias", "Mialgias", "Rigidez matutina", "Debilidad muscular",
                     "Deformidades articulares", "Limitación funcional", "Dolor óseo"],
    },
    {
        "key": "neurologico", "label": "Neurológico", "icono": "🧠",
        "guia": "",
        "sintomas": ["Convulsiones", "Pérdida de conciencia", "Parestesias", "Debilidad / paresia",
                     "Alteración de la marcha", "Temblor", "Alteración del habla", "Vértigo",
                     "Pérdida de memoria"],
    },
    {
        "key": "psiquiatrico", "label": "Psiquiátrico", "icono": "🧩",
        "guia": "Pregunta siempre, aunque no parezca el motivo de consulta.",
        "sintomas": ["Ansiedad", "Tristeza / ánimo bajo", "Alteraciones del sueño",
                     "Cambios de humor", "Ideas de muerte o suicidas", "Alucinaciones",
                     "Dificultad para concentrarse"],
    },
]

# ============================================================
# EXAMEN FÍSICO
# ============================================================
EXAMEN_FISICO_SISTEMAS = [
    {
        "key": "aspecto_general", "label": "Aspecto general", "icono": "🧍",
        "normal": "Paciente en buenas condiciones generales, ubicado en tiempo, espacio y persona, colaborador, hidratado, eupneico, afebril al tacto y tolerando la vía oral.",
        "anormales": ["Facies de dolor", "Deshidratado", "Taquipneico", "Diaforético",
                      "Mal estado general", "Palidez cutaneomucosa", "Ictericia"],
        "guia": "Facies, actitud, marcha al entrar, estado de conciencia, hidratación, constitución.",
    },
    {
        "key": "piel", "label": "Piel y anexos", "icono": "🧴",
        "normal": "Piel con elasticidad y turgor conservados, untuosidad y humedad adecuadas, sin lesiones, cicatrices, ni erupciones. Uñas y cabello de características normales.",
        "anormales": ["Palidez", "Ictericia", "Cianosis", "Lesiones tipo rash", "Equimosis / petequias",
                      "Edema", "Cicatrices", "Nódulos", "Onicolisis", "Alopecia"],
        "guia": "Color, humedad, textura, temperatura, elasticidad, turgor, pigmentación, fototipo (Fitzpatrick), lesiones, uñas, cabello.",
        "extra": "fitzpatrick",
    },
    {
        "key": "cabeza", "label": "Cabeza", "icono": "🧠",
        "normal": "Normocéfalo, sin tumoraciones, reblandecimientos ni puntos dolorosos a la palpación. Pulsos temporales presentes y simétricos.",
        "anormales": ["Dolor a la palpación", "Tumoraciones", "Asimetría craneal", "Cicatrices"],
        "guia": "Forma (inspección y medición), puntos dolorosos, cuero cabelludo, pulsos temporales.",
    },
    {
        "key": "ojos", "label": "Ojos", "icono": "👁️",
        "normal": "Cejas y pestañas de características normales. Conjuntivas y escleras indemnes, sin palidez ni ictericia. Párpados y córnea sin alteraciones. Pupilas isocóricas, normorreactivas a la luz, con reflejo fotomotor directo y consensual conservado, y reflejo de convergencia presente. Movimientos oculares extrínsecos conservados. Tonometría sin alteraciones.",
        "anormales": ["Palidez conjuntival", "Ictericia escleral", "Anisocoria", "Exoftalmos",
                      "Ptosis", "Nistagmus", "Limitación de movimientos oculares", "Opacidad corneal"],
        "guia": "Cejas/pestañas, párpados, conjuntiva, esclera, córnea, pupilas (tamaño, forma, fotomotor, consensuado, convergencia), movimientos oculares, fondo de ojo, tonometría.",
        "extra": "ojos_reflejos",
    },
    {
        "key": "oidos", "label": "Oídos", "icono": "👂",
        "normal": "Pabellones auriculares de características normales, sin dolor a la tracción del trago. Conductos auditivos externos permeables. Otoscopia sin alteraciones, membrana timpánica visible, brillante, con triángulo luminoso presente.",
        "anormales": ["Dolor a la tracción", "Cerumen impactado", "Secreción ótica",
                      "Membrana timpánica opaca o perforada", "Hipoacusia detectable"],
        "guia": "Pabellones, dolor a tracción/trago, otoscopia, membrana timpánica, pruebas de Weber y Rinne.",
        "extra": "weber_rinne",
    },
    {
        "key": "nariz_senos", "label": "Nariz y senos paranasales", "icono": "👃",
        "normal": "Pirámide nasal de características normales, fosas nasales permeables, tabique central, sin secreciones. Senos paranasales no dolorosos a la palpación ni percusión, transiluminación negativa.",
        "anormales": ["Desviación septal", "Secreción nasal", "Dolor sinusal", "Pólipos",
                      "Transiluminación positiva"],
        "guia": "Pirámide nasal, fosas nasales, tabique, rinoscopia, dolor a la digitopresión de senos, transiluminación.",
    },
    {
        "key": "boca_orofaringe", "label": "Boca y orofaringe", "icono": "🦷",
        "normal": "Apertura bucal adecuada. Labios, carrillos, encías y dientes sin lesiones. Lengua y paladar de características normales. Reflejo oropalatino presente. Orofaringe sin eritema ni exudados, amígdalas sin hipertrofia, úvula central y móvil.",
        "anormales": ["Eritema faríngeo", "Exudados amigdalinos", "Lesiones orales",
                      "Sequedad de mucosas", "Halitosis marcada", "Caries múltiples", "Reflejo oropalatino ausente"],
        "guia": "Apertura bucal, labios, carrillos, encías, dientes, lengua, paladar, amígdalas, reflejo oropalatino (úvula).",
    },
    {
        "key": "cuello", "label": "Cuello", "icono": "🧣",
        "normal": "Cuello simétrico, sin tumoraciones, no doloroso a la palpación. Movimientos activos y pasivos conservados (rotación, flexión, extensión). Tráquea central y móvil, tiroides no palpable. Ganglios no palpables. Pulso carotídeo presente, sin soplos ni ingurgitación yugular.",
        "anormales": ["Adenopatías palpables", "Bocio / tiromegalia", "Ingurgitación yugular",
                      "Soplo carotídeo", "Masa cervical", "Rigidez de nuca", "Limitación de la movilidad"],
        "guia": "Inspección, movilidad (rotación/flexión/extensión), tráquea, tiroides, ganglios, auscultación de soplos carotídeos.",
    },
    {
        "key": "torax_pulmones", "label": "Tórax y pulmones", "icono": "🫁",
        "normal": "Tórax simétrico, normoexpansible, sin lesiones ni uso de músculos accesorios. Vibraciones vocales conservadas y simétricas. Sonoridad pulmonar conservada a la percusión. Murmullo vesicular presente en ambos campos pulmonares, sin ruidos agregados.",
        "anormales": ["Estertores crepitantes", "Sibilancias", "Roncus", "Frote pleural",
                      "Disminución del murmullo vesicular", "Matidez a la percusión",
                      "Hiperresonancia", "Tiraje / uso de músculos accesorios"],
        "guia": "Forma, lesiones/dolor, uso de músculos accesorios, expansibilidad, vibraciones vocales, percusión, auscultación.",
    },
    {
        "key": "cardiovascular", "label": "Cardiovascular", "icono": "❤️",
        "normal": "Pulso arterial rítmico, regular, de amplitud y forma normal. Pulso venoso con tope no visible. Área precordial sin retracciones; choque de la punta no visible, palpable en el 5to espacio intercostal izquierdo con línea medioclavicular. Ruidos cardíacos rítmicos y regulares, de buena intensidad, sin soplos, galopes ni frotes.",
        "anormales": ["Taquicardia", "Bradicardia", "Arritmia", "Soplo cardíaco", "Galope (R3/R4)",
                      "Frote pericárdico", "Choque de la punta sostenido/hipercinético",
                      "Ingurgitación yugular"],
        "guia": "Focos de auscultación: Aórtico (2° EID), Pulmonar (2° EII), Accesorio/Erb (3° EII), Tricuspídeo (4° EII), Mitral (5° EII, línea medioclavicular). Pulso arterial y venoso, área precordial, ritmo, soplos, galopes, frotes.",
    },
    {
        "key": "abdomen", "label": "Abdomen y fosas renales", "icono": "🩻",
        "normal": "Abdomen simétrico, depresible, no doloroso a la palpación superficial ni profunda, sin masas ni visceromegalias. Ruidos hidroaéreos presentes. Hígado y bazo no palpables. Puño percusión renal negativa bilateral.",
        "anormales": ["Dolor a la palpación", "Defensa muscular", "Hepatomegalia", "Esplenomegalia",
                      "Masa palpable", "Distensión", "Ascitis",
                      "Ruidos hidroaéreos aumentados o ausentes"],
        "guia": "Inspección (forma, volumen, vello), auscultación (RHA/min, soplos, frotes), percusión, palpación superficial y profunda, hepatometría, bazo (Naegele/Schuster), puntos ureterales, puño-percusión.",
        "extra": "abdomen_maniobras",
    },
    {
        "key": "genitourinario", "label": "Genitales", "icono": "🚻",
        "normal": "Genitales externos de características normales para la edad y sexo, sin lesiones ni secreciones.",
        "anormales": ["Secreción anormal", "Lesiones genitales", "Masa palpable",
                      "Dolor a la palpación"],
        "guia": "Inspección de genitales externos, ganglios inguinales; en el hombre: escroto, testículos, próstata si aplica; en la mujer: vulva, vagina, cuello uterino si aplica.",
    },
    {
        "key": "osteomuscular", "label": "Osteomuscular", "icono": "🦴",
        "normal": "Movimientos activos y pasivos conservados en todas las articulaciones, sin dolor, deformidad ni limitación funcional. Fuerza muscular 5/5 en las cuatro extremidades. Masas musculares simétricas.",
        "anormales": ["Dolor articular", "Deformidad", "Limitación funcional", "Inflamación articular",
                      "Disminución de fuerza muscular", "Atrofia muscular", "Rigidez"],
        "guia": "Deformidades, dolor, impotencia funcional y rango de movimiento de cada articulación (columna, hombro, codo, carpo, cadera, rodilla, tobillo).",
    },
    {
        "key": "extremidades", "label": "Extremidades", "icono": "🦵",
        "normal": "Extremidades simétricas, sin edema, cianosis ni várices. Llenado capilar menor a 3 segundos. Pulsos distales presentes y simétricos.",
        "anormales": ["Edema", "Várices", "Cianosis distal", "Llenado capilar prolongado",
                      "Pulsos distales disminuidos", "Úlceras", "Deformidades"],
        "guia": "Color, edema, temblor, deformidades, pulsos distales, llenado capilar, úlceras, várices.",
    },
    {
        "key": "neurologico", "label": "Neurológico", "icono": "🧠",
        "normal": "Paciente consciente, orientado en tiempo, espacio y persona. Lenguaje fluente, con adecuada comprensión, repetición, nominación y prosodia. Pares craneales sin alteraciones. Fuerza y tono muscular conservados (5/5), trofismo conservado. Reflejos osteotendinosos presentes y simétricos (II/IV). Sensibilidad superficial y profunda conservada. Coordinación, marcha, praxia y gnosia sin alteraciones. Signos meníngeos negativos.",
        "anormales": ["Alteración del estado de conciencia", "Desorientación",
                      "Déficit motor (paresia/plejia)", "Alteración sensitiva",
                      "Reflejos asimétricos o ausentes", "Alteración de la marcha",
                      "Rigidez", "Temblor", "Alteración del lenguaje"],
        "guia": "Estado mental y lenguaje, 12 pares craneales, fuerza/tono/trofismo, reflejos osteotendinosos y cutáneos, sensibilidad, coordinación (taxia), marcha/praxia/gnosia, signos meníngeos, Mini Mental si aplica.",
        "extra": "neuro_completo",
    },
]

FITZPATRICK_OPCIONES = [
    "No evaluado", "Tipo I — muy clara, siempre se quema", "Tipo II — clara, se quema fácil",
    "Tipo III — media, se quema moderado", "Tipo IV — oliva, rara vez se quema",
    "Tipo V — morena, casi nunca se quema", "Tipo VI — negra, nunca se quema",
]

WEBER_OPCIONES = ["No realizado", "Sin lateralización", "Lateralizado a la derecha", "Lateralizado a la izquierda"]
RINNE_OPCIONES = ["No realizado", "Positivo bilateral", "Negativo derecho", "Negativo izquierdo", "Negativo bilateral"]

ABDOMEN_MANIOBRAS = ["Blumberg", "Murphy", "McBurney", "Rovsing"]
ESTADO_MANIOBRA = ["No evaluado", "Negativo", "Positivo"]

REFLEJOS_OSTEOTENDINOSOS = ["Bicipital", "Tricipital", "Estiloradial", "Patelar", "Aquiliano"]
GRADOS_REFLEJO = ["No evaluado", "0 (arreflexia)", "I/IV (hiporreflexia)", "II/IV (normal)", "III/IV (vivo)", "IV/IV (clonus)"]
SIGNOS_MENINGEOS = ["Rigidez de nuca", "Kernig", "Brudzinski"]
PARES_CRANEALES_TXT = "I Olfatorio · II Óptico · III-IV-VI Oculomotores · V Trigémino · VII Facial · VIII Vestibulococlear · IX Glosofaríngeo · X Vago · XI Accesorio · XII Hipogloso"

DIAGNOSTICOS_SINDROMATICOS_SUGERIDOS = [
    "Síndrome febril", "Síndrome anémico", "Síndrome urémico", "Síndrome edematoso",
    "Síndrome doloroso abdominal", "Síndrome de respuesta inflamatoria sistémica (SIRS)",
    "Síndrome de insuficiencia cardíaca", "Síndrome de condensación pulmonar",
    "Síndrome meníngeo", "Síndrome ictérico", "Síndrome consuntivo", "Síndrome hipertensivo",
]
