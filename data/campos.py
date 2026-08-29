"""
Definiciones de contenido clínico para la Historia Clínica de Medicina Interna.
Todo el contenido "qué preguntar / qué explorar" vive aquí, separado de la UI,
para que sea fácil de ampliar o corregir sin tocar app.py.
"""

# ============================================================
# ANTECEDENTES PERSONALES — enfermedades de la infancia (checklist)
# ============================================================
ENF_INFANCIA = [
    "Sarampión", "Rubéola", "Varicela", "Parotiditis", "Tos ferina",
    "Escarlatina", "Mononucleosis infecciosa", "Difteria", "Poliomielitis",
    "Fiebre reumática", "Dengue",
]

ENF_CRONICAS_ADULTO = [
    "Hipertensión arterial", "Diabetes mellitus", "Enfermedad renal crónica",
    "Asma", "EPOC", "Cardiopatía isquémica", "Insuficiencia cardíaca",
    "Enfermedad cerebrovascular", "Hipotiroidismo", "Hipertiroidismo",
    "Dislipidemia", "Enfermedad hepática crónica", "Anemia",
    "Enfermedad autoinmune", "Cáncer", "Tuberculosis", "VIH",
    "Enfermedad psiquiátrica",
]

ETS = ["Sífilis", "Gonorrea", "VPH", "Hepatitis B", "Hepatitis C", "VIH", "Herpes genital"]

# ============================================================
# ANTECEDENTES FAMILIARES — parentescos sugeridos
# ============================================================
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
# REVISIÓN POR SISTEMAS (interrogatorio funcional)
# Cada sección: síntomas típicos a interrogar activamente.
# ============================================================
REVISION_SISTEMAS = [
    {
        "key": "general",
        "label": "Generales",
        "icono": "🩺",
        "sintomas": [
            "Fiebre", "Pérdida de peso", "Aumento de peso", "Astenia",
            "Anorexia", "Diaforesis / sudoración nocturna", "Escalofríos",
            "Malestar general",
        ],
    },
    {
        "key": "piel",
        "label": "Piel y anexos",
        "icono": "🧴",
        "sintomas": [
            "Prurito", "Erupciones / rash", "Cambios de coloración",
            "Caída del cabello", "Resequedad", "Edema", "Cicatrización lenta",
            "Aparición de nódulos o lesiones", "Cambios en lunares",
        ],
    },
    {
        "key": "cabeza",
        "label": "Cabeza",
        "icono": "🧠",
        "sintomas": ["Cefalea", "Mareos", "Síncope", "Traumatismos craneales"],
    },
    {
        "key": "ojos",
        "label": "Ojos",
        "icono": "👁️",
        "sintomas": [
            "Disminución de agudeza visual", "Visión borrosa", "Diplopía",
            "Fotofobia", "Dolor ocular", "Lagrimeo excesivo / xeroftalmia",
            "Secreción", "Uso de lentes correctivos",
        ],
    },
    {
        "key": "oidos",
        "label": "Oídos",
        "icono": "👂",
        "sintomas": [
            "Hipoacusia", "Tinnitus", "Vértigo", "Otalgia", "Otorrea",
            "Sensación de plenitud auricular",
        ],
    },
    {
        "key": "nariz",
        "label": "Nariz",
        "icono": "👃",
        "sintomas": [
            "Obstrucción nasal", "Epistaxis", "Rinorrea", "Estornudos",
            "Anosmia / hiposmia", "Dolor en senos paranasales",
        ],
    },
    {
        "key": "boca_garganta",
        "label": "Boca y garganta",
        "icono": "🦷",
        "sintomas": [
            "Odinofagia", "Disfagia", "Ronquera / disfonía",
            "Sangrado gingival", "Halitosis", "Lesiones orales",
            "Alteración del gusto",
        ],
    },
    {
        "key": "cuello",
        "label": "Cuello",
        "icono": "🧣",
        "sintomas": ["Masas cervicales", "Dolor cervical", "Rigidez", "Adenopatías palpables"],
    },
    {
        "key": "respiratorio",
        "label": "Respiratorio",
        "icono": "🫁",
        "sintomas": [
            "Tos seca", "Tos productiva", "Disnea", "Sibilancias",
            "Dolor torácico pleurítico", "Hemoptisis", "Ortopnea",
        ],
    },
    {
        "key": "cardiovascular",
        "label": "Cardiovascular",
        "icono": "❤️",
        "sintomas": [
            "Dolor torácico", "Palpitaciones", "Disnea de esfuerzo",
            "Disnea paroxística nocturna", "Ortopnea", "Edema en miembros inferiores",
            "Claudicación intermitente", "Síncope", "Cianosis",
        ],
    },
    {
        "key": "gastrointestinal",
        "label": "Gastrointestinal",
        "icono": "🍽️",
        "sintomas": [
            "Dolor abdominal", "Náuseas", "Vómitos", "Diarrea",
            "Estreñimiento", "Pirosis", "Disfagia", "Hematemesis",
            "Melena", "Rectorragia", "Ictericia", "Distensión abdominal",
            "Cambios en el apetito", "Intolerancia alimentaria",
        ],
    },
    {
        "key": "genitourinario",
        "label": "Genitourinario",
        "icono": "🚻",
        "sintomas": [
            "Disuria", "Hematuria", "Polaquiuria", "Nicturia",
            "Incontinencia urinaria", "Urgencia miccional",
            "Tenesmo vesical", "Secreción uretral", "Dolor lumbar",
            "Cambios en el chorro urinario", "Espuma en orina",
        ],
    },
    {
        "key": "ginecologico",
        "label": "Ginecológico (si aplica)",
        "icono": "♀️",
        "sintomas": [
            "Alteraciones del ciclo menstrual", "Dismenorrea",
            "Sangrado intermenstrual", "Flujo vaginal anormal",
            "Dispareunia", "Síntomas de menopausia", "Masa o dolor mamario",
        ],
    },
    {
        "key": "endocrino",
        "label": "Endocrino",
        "icono": "⚖️",
        "sintomas": [
            "Intolerancia al frío", "Intolerancia al calor", "Poliuria",
            "Polidipsia", "Polifagia", "Cambios de peso inexplicados",
            "Hirsutismo", "Temblor fino",
        ],
    },
    {
        "key": "hematologico",
        "label": "Hematológico",
        "icono": "🩸",
        "sintomas": [
            "Equimosis fáciles", "Sangrado prolongado", "Palidez",
            "Adenopatías generalizadas", "Petequias",
        ],
    },
    {
        "key": "musculoesqueletico",
        "label": "Osteomuscular",
        "icono": "🦴",
        "sintomas": [
            "Artralgias", "Mialgias", "Rigidez matutina", "Debilidad muscular",
            "Deformidades articulares", "Limitación funcional", "Dolor óseo",
        ],
    },
    {
        "key": "neurologico",
        "label": "Neurológico",
        "icono": "🧠",
        "sintomas": [
            "Convulsiones", "Pérdida de conciencia", "Parestesias",
            "Debilidad / paresia", "Alteración de la marcha", "Temblor",
            "Alteración del habla", "Vértigo", "Pérdida de memoria",
        ],
    },
    {
        "key": "psiquiatrico",
        "label": "Psiquiátrico",
        "icono": "🧩",
        "sintomas": [
            "Ansiedad", "Tristeza / ánimo bajo", "Alteraciones del sueño",
            "Cambios de humor", "Ideas de muerte o suicidas",
            "Alucinaciones", "Dificultad para concentrarse",
        ],
    },
]

# ============================================================
# EXAMEN FÍSICO — plantilla de hallazgo normal + hallazgos anormales comunes
# ============================================================
EXAMEN_FISICO_SISTEMAS = [
    {
        "key": "aspecto_general",
        "label": "Aspecto general",
        "icono": "🧍",
        "normal": "Paciente en buenas condiciones generales, ubicado en tiempo, espacio y persona, colaborador, hidratado, eupneico, afebril al tacto y tolerando la vía oral.",
        "anormales": [
            "Facies de dolor", "Deshidratado", "Taquipneico", "Diaforético",
            "Mal estado general", "Palidez cutaneomucosa", "Ictericia",
        ],
    },
    {
        "key": "piel",
        "label": "Piel y anexos",
        "icono": "🧴",
        "normal": "Piel con elasticidad y turgor conservados, untuosidad y humedad adecuadas, sin lesiones, cicatrices, ni erupciones. Uñas y cabello de características normales.",
        "anormales": [
            "Palidez", "Ictericia", "Cianosis", "Lesiones tipo rash",
            "Equimosis / petequias", "Edema", "Cicatrices", "Nódulos",
            "Onicolisis", "Alopecia",
        ],
    },
    {
        "key": "cabeza",
        "label": "Cabeza",
        "icono": "🧠",
        "normal": "Normocéfalo, sin tumoraciones, reblandecimientos ni puntos dolorosos a la palpación. Pulsos temporales presentes y simétricos.",
        "anormales": ["Dolor a la palpación", "Tumoraciones", "Asimetría craneal", "Cicatrices"],
    },
    {
        "key": "ojos",
        "label": "Ojos",
        "icono": "👁️",
        "normal": "Conjuntivas y escleras indemnes, sin palidez ni ictericia. Pupilas isocóricas, normorreactivas a la luz. Movimientos oculares extrínsecos conservados. Reflejo fotomotor directo y consensual presente.",
        "anormales": [
            "Palidez conjuntival", "Ictericia escleral", "Anisocoria",
            "Exoftalmos", "Ptosis", "Nistagmus", "Limitación de movimientos oculares",
        ],
    },
    {
        "key": "oidos",
        "label": "Oídos",
        "icono": "👂",
        "normal": "Pabellones auriculares de características normales, sin dolor a la tracción del trago. Conductos auditivos externos permeables. Membrana timpánica visible, brillante, con triángulo luminoso presente.",
        "anormales": [
            "Dolor a la tracción", "Cerumen impactado", "Secreción ótica",
            "Membrana timpánica opaca o perforada", "Hipoacusia detectable",
        ],
    },
    {
        "key": "nariz_senos",
        "label": "Nariz y senos paranasales",
        "icono": "👃",
        "normal": "Pirámide nasal de características normales, fosas nasales permeables, sin secreciones. Senos paranasales no dolorosos a la palpación ni percusión.",
        "anormales": ["Desviación septal", "Secreción nasal", "Dolor sinusal", "Pólipos"],
    },
    {
        "key": "boca_orofaringe",
        "label": "Boca y orofaringe",
        "icono": "🦷",
        "normal": "Labios, encías y mucosa oral sin lesiones. Lengua de características normales. Orofaringe sin eritema ni exudados, úvula central y móvil.",
        "anormales": [
            "Eritema faríngeo", "Exudados amigdalinos", "Lesiones orales",
            "Sequedad de mucosas", "Halitosis marcada", "Caries múltiples",
        ],
    },
    {
        "key": "cuello",
        "label": "Cuello",
        "icono": "🧣",
        "normal": "Cuello simétrico, sin tumoraciones, no doloroso a la palpación. Tráquea central y móvil, tiroides no palpable. Pulso carotídeo presente, sin soplos ni ingurgitación yugular.",
        "anormales": [
            "Adenopatías palpables", "Bocio / tiromegalia", "Ingurgitación yugular",
            "Soplo carotídeo", "Masa cervical", "Rigidez de nuca",
        ],
    },
    {
        "key": "torax_pulmones",
        "label": "Tórax y pulmones",
        "icono": "🫁",
        "normal": "Tórax simétrico, normoexpansible, sin uso de músculos accesorios. Vibraciones vocales conservadas y simétricas. Murmullo vesicular presente en ambos campos pulmonares, sin ruidos agregados.",
        "anormales": [
            "Estertores crepitantes", "Sibilancias", "Roncus", "Frote pleural",
            "Disminución del murmullo vesicular", "Matidez a la percusión",
            "Hiperresonancia", "Tiraje / uso de músculos accesorios",
        ],
    },
    {
        "key": "cardiovascular",
        "label": "Cardiovascular",
        "icono": "❤️",
        "normal": "Ruidos cardíacos rítmicos y regulares, de buena intensidad, sin soplos, galopes ni frotes. Pulsos periféricos presentes, simétricos, sin edema en miembros inferiores.",
        "anormales": [
            "Taquicardia", "Bradicardia", "Arritmia", "Soplo cardíaco",
            "Galope (R3/R4)", "Edema en miembros inferiores",
            "Pulsos disminuidos o asimétricos", "Ingurgitación yugular",
        ],
    },
    {
        "key": "abdomen",
        "label": "Abdomen",
        "icono": "🩻",
        "normal": "Abdomen simétrico, depresible, no doloroso a la palpación, sin masas ni visceromegalias. Ruidos hidroaéreos presentes. Sin signos de irritación peritoneal.",
        "anormales": [
            "Dolor a la palpación", "Defensa muscular", "Signo de rebote (Blumberg +)",
            "Hepatomegalia", "Esplenomegalia", "Masa palpable", "Distensión",
            "Ascitis", "Ruidos hidroaéreos aumentados o ausentes",
        ],
    },
    {
        "key": "genitourinario",
        "label": "Genitourinario",
        "icono": "🚻",
        "normal": "Genitales externos de características normales para la edad y sexo, sin lesiones ni secreciones. Puño percusión renal negativa bilateral.",
        "anormales": [
            "Puño percusión positiva", "Secreción anormal", "Lesiones genitales",
            "Masa palpable", "Dolor a la palpación renal",
        ],
    },
    {
        "key": "osteomuscular",
        "label": "Osteomuscular",
        "icono": "🦴",
        "normal": "Movimientos activos y pasivos conservados en todas las articulaciones, sin dolor, deformidad ni limitación funcional. Fuerza muscular 5/5 en las cuatro extremidades.",
        "anormales": [
            "Dolor articular", "Deformidad", "Limitación funcional",
            "Inflamación articular", "Disminución de fuerza muscular",
            "Atrofia muscular",
        ],
    },
    {
        "key": "extremidades",
        "label": "Extremidades",
        "icono": "🦵",
        "normal": "Extremidades simétricas, sin edema, cianosis ni várices. Llenado capilar menor a 3 segundos. Pulsos distales presentes y simétricos.",
        "anormales": [
            "Edema", "Várices", "Cianosis distal", "Llenado capilar prolongado",
            "Pulsos distales disminuidos", "Úlceras",
        ],
    },
    {
        "key": "neurologico",
        "label": "Neurológico",
        "icono": "🧠",
        "normal": "Paciente consciente, orientado en tiempo, espacio y persona. Pares craneales sin alteraciones. Fuerza y tono muscular conservados. Reflejos osteotendinosos presentes y simétricos. Sensibilidad conservada. Marcha y coordinación sin alteraciones.",
        "anormales": [
            "Alteración del estado de conciencia", "Desorientación",
            "Déficit motor (paresia/plejia)", "Alteración sensitiva",
            "Reflejos asimétricos o ausentes", "Babinski positivo",
            "Alteración de la marcha", "Rigidez / signos meníngeos",
            "Temblor",
        ],
    },
]

# Diagnósticos sindromáticos frecuentes en medicina interna (sugerencias rápidas)
DIAGNOSTICOS_SINDROMATICOS_SUGERIDOS = [
    "Síndrome febril", "Síndrome anémico", "Síndrome urémico",
    "Síndrome edematoso", "Síndrome doloroso abdominal",
    "Síndrome de repuesta inflamatoria sistémica (SIRS)",
    "Síndrome de insuficiencia cardíaca", "Síndrome de condensación pulmonar",
    "Síndrome meníngeo", "Síndrome ictérico", "Síndrome consuntivo",
    "Síndrome hipertensivo",
]
