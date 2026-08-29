# Historia Clínica — Medicina Interna

App en **Python (Streamlit)** para llenar la historia clínica completa durante
el interrogatorio y examen físico del paciente, con descarga final en **PDF**.

## Estructura del proyecto

```
historia_clinica_app/
├── app.py                  # App principal (navegación + formularios)
├── requirements.txt
├── .streamlit/config.toml  # Tema de color (teal + slate)
├── data/campos.py          # Todo el contenido clínico: qué preguntar/explorar
└── utils/
    ├── state.py            # Estado de sesión y progreso por sección
    ├── styles.py           # CSS del diseño elegante (Lora + Montserrat)
    └── pdf_export.py       # Generación del PDF final (reportlab)
```

## Cómo correrla en tu computadora

```bash
cd historia_clinica_app
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá en `http://localhost:8501`.

## Cómo desplegarla (gratis) en Streamlit Community Cloud

1. Sube esta carpeta a un repositorio de GitHub (puede ser privado).
2. Entra a https://share.streamlit.io/ con tu cuenta de GitHub.
3. "New app" → selecciona el repo → archivo principal: `app.py` → Deploy.
4. En 1–2 minutos tendrás una URL pública (`tuapp.streamlit.app`) para usar
   desde el celular o la computadora en el hospital.

> Nota: Netlify **no puede ejecutar** esta app porque solo sirve archivos
> estáticos (HTML/CSS/JS) y esta app necesita un servidor Python corriendo
> permanentemente. Streamlit Community Cloud es el equivalente gratuito
> pensado exactamente para esto.

## Cómo usarla

1. Navega por las secciones desde el menú lateral (Filiación → Motivo →
   Antecedentes → ... → Examen Físico).
2. En **Revisión por Sistemas** y **Examen Físico**, cada aparato se despliega
   en un acordeón: marcas los síntomas/hallazgos con clics rápidos y agregas
   detalle en texto libre solo si hace falta — pensado para llenarse rápido
   junto a la cama del paciente.
3. En **Examen Físico**, si marcas "Normal" se autocompleta una plantilla de
   hallazgo normal (editable) para no reescribir lo mismo cada vez.
4. Al final, entra a **Vista Previa y PDF** y descarga el documento con el
   botón "Descargar Historia Clínica en PDF".
5. Los datos se mantienen mientras la pestaña del navegador esté abierta
   (no se guardan en un servidor ni en la nube).

## Próximos pasos sugeridos (dime cuál priorizar)

- Guardado/carga de historias como archivo `.json` para retomar un caso.
- Logo/membrete de tu institución en el PDF.
- Ajustar o añadir campos según tu rotación específica.
