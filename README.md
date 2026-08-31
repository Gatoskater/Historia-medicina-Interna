# Historia Clínica — Medicina Interna

App en **Python (Streamlit)** para llenar la historia clínica completa durante
el interrogatorio y examen físico del paciente, con descarga final en **PDF**.

Diseñada y desarrollada por **Jade Díaz**.

## Qué trae esta versión

- **Diseño corporativo navy + oro**, tipografía Playfair Display (títulos) +
  Inter (cuerpo), embebida de verdad tanto en la interfaz como en el PDF
  final (no son fuentes genéricas del sistema).
- **Asistente dinámico de Enfermedad Actual**: eliges los síntomas guía
  (Dolor, Fiebre, Tos, Disnea, Diarrea, Vómitos, Cefalea, Edema, Síncope,
  Palpitaciones) y la app te muestra exactamente qué interrogar de cada uno
  (p. ej. Dolor → ALICIDPH), con un botón para insertar la redacción
  generada directamente en el relato libre — que sigues pudiendo editar a mano.
- **Calculadora de índice paquete-año**: colocas cigarrillos/día y años
  fumando, y la app calcula `(cigarrillos ÷ 20) × años` y clasifica el
  hábito (leve/moderado/severo) automáticamente.
- **Maniobras semiológicas** en el examen físico: Murphy, Blumberg,
  McBurney, Rovsing, puño-percusión renal, Weber, Rinne, reflejos
  osteotendinosos graduados (0 a IV/IV), signos meníngeos, fototipo de
  Fitzpatrick, reflejos pupilares — todo con menús rápidos, no listas
  interminables de casillas.
- **Ayuda contextual en cada campo**: casi todos los campos tienen un
  ejemplo (placeholder) de qué escribir y, donde aplica, un ícono de ayuda
  (ⓘ) o un botón "¿Qué explorar aquí?" con la guía semiológica — sin saturar
  la pantalla.
- **Interacciones modernas**: chips seleccionables (pills) en vez de menús
  desplegables, controles segmentados para Normal/Anormal, interruptores
  (toggles), notificaciones flotantes al añadir texto al relato, navegación
  Anterior/Siguiente tipo asistente guiado, además del menú lateral.

## Estructura del proyecto

```
historia_clinica_app/
├── app.py                     # App principal (navegación + formularios)
├── requirements.txt
├── .streamlit/config.toml     # Tema de color (navy + oro)
├── assets/fonts/               # Playfair Display + Inter, embebidas en el PDF
├── data/campos.py             # Todo el contenido clínico: qué preguntar/explorar
└── utils/
    ├── state.py                # Estado de sesión, progreso, fórmula IPA
    ├── styles.py                # CSS del diseño (masthead, sidebar, pills...)
    ├── narrativa.py             # Compone la redacción semiológica automática
    └── pdf_export.py            # Generación del PDF final (reportlab)
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

1. Sube **toda la carpeta completa** (incluyendo `utils/`, `data/` y
   `assets/`) a un repositorio de GitHub. Si usas la web de GitHub, arrastra
   las carpetas completas al área de "Upload files" — el botón de
   "choose your files" no sube carpetas, solo el arrastre sí. La forma más
   confiable es usar GitHub Desktop o `git` desde la terminal.
2. Entra a https://share.streamlit.io/ con tu cuenta de GitHub.
3. "New app" → selecciona el repo → archivo principal: `app.py` → Deploy.
4. En 1–2 minutos tendrás una URL pública (`tuapp.streamlit.app`).

> Netlify no puede ejecutar esta app porque solo sirve archivos estáticos
> (HTML/CSS/JS); esta app necesita un servidor Python corriendo
> permanentemente. Streamlit Community Cloud es el equivalente gratuito
> pensado para esto.

## Cómo usarla

1. Navega por las secciones desde el menú lateral, o usa los botones
   "← Anterior" / "Siguiente →" al final de cada pantalla.
2. En **Enfermedad Actual**, toca los síntomas que aplican (p. ej. "Dolor"),
   llena los campos guiados que aparecen, revisa la vista previa de la
   redacción y dale a "Añadir al relato" para insertarla en el texto libre.
3. En **Hábitos**, activa "¿Fuma o ha fumado?" para que aparezca la
   calculadora de índice paquete-año.
4. En **Revisión por Sistemas** y **Examen Físico**, cada aparato se
   despliega en un acordeón con chips rápidos de tocar.
5. En **Examen Físico**, los sistemas con maniobras especiales (Piel,
   Ojos, Oídos, Abdomen, Neurológico) muestran campos adicionales en cuanto
   los marcas como explorados.
6. Al final, entra a **Vista Previa y PDF** y descarga el documento.
7. Los datos se mantienen mientras la pestaña del navegador esté abierta
   (no se guardan en un servidor ni en la nube). El botón "Nueva historia"
   en el menú lateral borra todo para empezar un caso nuevo.

## Próximos pasos sugeridos (dime cuál priorizar)

- Guardado/carga de historias como archivo `.json` para retomar un caso.
- Logo/membrete de tu institución en el PDF.
- Más motivos de consulta guiados (p. ej. mareo/vértigo, sangrados).
- Ajustar el contenido clínico de alguna sección específica.
