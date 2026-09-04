"""
Términos de Uso y pantalla de aceptación obligatoria.

AVISO IMPORTANTE PARA JADE: este texto es un punto de partida razonable,
no asesoría legal. Antes de cobrar por el uso de la app, especialmente
porque maneja datos de pacientes, te recomiendo que un abogado (idealmente
con experiencia en salud/datos personales en Venezuela) lo revise. Dos
cosas que un abogado sí debe mirar con cuidado:
  1. Manejo de datos de pacientes: aunque el "usuario" que paga eres tú
     vendiéndole a un estudiante/médico, la app procesa datos de terceros
     (los pacientes). Conviene dejar explícito quién es responsable de
     proteger esos datos y que el uso debe cumplir la normativa de
     protección de datos e historia clínica que aplique.
  2. Cláusulas de limitación de responsabilidad y de pago tienen más peso
     legal si están redactadas o revisadas por un abogado local.
"""

import streamlit as st
from datetime import datetime, timezone

APP_VERSION = "2.2.3"

TERMINOS_TEXTO = """
**Términos de Uso — QuickChart (Historia Clínica · Medicina Interna)**
*Última actualización: 2026*

**1. Naturaleza de la herramienta.** QuickChart es una herramienta de
apoyo para la redacción y organización de historias clínicas durante la
formación médica. No sustituye el juicio clínico, la supervisión docente
ni ninguna guía o protocolo institucional. No es un dispositivo médico ni
un sistema de historia clínica electrónica certificado.

**2. Responsabilidad del usuario.** El uso de la información generada por
esta aplicación —incluyendo el contenido clínico, las plantillas de
examen físico y cualquier texto sugerido— es responsabilidad exclusiva de
quien la utiliza. Cada usuario debe verificar, corregir y validar toda la
información antes de usarla con fines académicos, asistenciales o de
cualquier otro tipo. El desarrollador no se hace responsable por
decisiones clínicas, errores de transcripción, uso indebido de la
información generada, ni por consecuencias derivadas de su uso.

**3. Datos de pacientes.** Si el usuario introduce datos de pacientes
reales, es su responsabilidad exclusiva contar con la autorización
correspondiente y cumplir con la normativa de protección de datos y de
historia clínica aplicable en su jurisdicción e institución. Se recomienda
no introducir datos que permitan identificar a un paciente salvo que ello
esté permitido por la institución donde se realiza la práctica.

**4. Suscripción y pagos.** El acceso a la aplicación está sujeto a una
suscripción de pago con la periodicidad y el monto acordados al momento de
la contratación. El usuario se compromete a cumplir con lo acordado en
cuanto a forma de pago, monto y vigencia del acceso. El acceso puede ser
suspendido de forma automática o manual al vencerse el período pagado, sin
que ello genere responsabilidad para el desarrollador. El uso compartido
de una misma cuenta con terceros no autorizados constituye un
incumplimiento de estos términos y puede resultar en la suspensión
inmediata del acceso, sin reembolso.

**5. Disponibilidad.** La aplicación se ofrece "tal cual", sin garantías
de disponibilidad continua, ausencia de errores, o idoneidad para un fin
particular. El desarrollador podrá modificar, suspender o descontinuar la
aplicación o alguna de sus funciones en cualquier momento.

**6. Propiedad intelectual.** El contenido, diseño y código de la
aplicación son propiedad de su desarrolladora. El usuario no está
autorizado a redistribuir, revender o realizar ingeniería inversa de la
aplicación sin autorización expresa.

**7. Aceptación.** Al marcar la casilla de aceptación, el usuario declara
haber leído y comprendido estos términos, y acepta usar la aplicación bajo
su propia responsabilidad y bajo las condiciones aquí descritas.
"""


def _guardar_aceptacion_supabase():
    try:
        from utils.supa import _cliente_con_sesion, supabase_configurado
        if not supabase_configurado() or "auth_user" not in st.session_state:
            return
        c = _cliente_con_sesion()
        c.table("subscriptions").update({
            "tos_accepted_at": datetime.now(timezone.utc).isoformat()
        }).eq("user_id", st.session_state["auth_user"]["id"]).execute()
    except Exception:
        pass  # no bloquear el flujo si esto falla; ya quedó aceptado localmente


def requerir_aceptacion_terminos() -> bool:
    """Devuelve True si el usuario ya aceptó (en esta sesión o antes, según
    Supabase). Si no, muestra la pantalla de aceptación y devuelve False."""
    if st.session_state.get("tos_ok"):
        return True

    # Si ya aceptó antes (columna en Supabase), no lo volvemos a molestar.
    sub_row = st.session_state.get("sub_row")
    if sub_row and sub_row.get("tos_accepted_at"):
        st.session_state["tos_ok"] = True
        return True

    st.markdown(
        "<div style='font-family:\"Playfair Display\",serif; font-weight:700; font-size:1.4rem; color:#101a34; margin-bottom:0.6rem;'>Términos de Uso</div>",
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown(TERMINOS_TEXTO)

    acepto = st.checkbox(
        "He leído y acepto los Términos de Uso, incluyendo que el uso de la "
        "información generada es mi responsabilidad y que debo cumplir con "
        "lo acordado en cuanto a pago y vigencia de la suscripción."
    )
    if st.button("Continuar", type="primary", disabled=not acepto, use_container_width=True):
        st.session_state["tos_ok"] = True
        _guardar_aceptacion_supabase()
        st.rerun()
    return False


def version_footer():
    st.markdown(
        f"""
        <div style="text-align:center; color:#9a9ea8; font-size:0.72rem; padding: 1.2rem 0 0.4rem 0;">
            QuickChart · Historia Clínica — versión {APP_VERSION}
        </div>
        """,
        unsafe_allow_html=True,
    )
