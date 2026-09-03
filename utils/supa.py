"""
Autenticación y control de acceso vía Supabase:
- Login / registro con correo y contraseña (Supabase Auth).
- Verificación de suscripción activa (tabla `subscriptions`).
- Sesión única por usuario (tabla `active_sessions`): si la misma cuenta
  inicia sesión en otro dispositivo, la sesión anterior se cierra sola.
- Autosave del borrador de la historia (tabla `historia_draft`).

Si `st.secrets["supabase"]` no está configurado, la app sigue funcionando
en "modo local" sin login (útil para seguir desarrollando sin depender de
Supabase), mostrando un aviso claro en vez de romperse.
"""

import json
import uuid
from datetime import date, datetime, timezone

import streamlit as st

_REVALIDATE_SEGUNDOS = 25  # cada cuánto se re-chequea sesión/suscripción


# ============================================================
# Cliente
# ============================================================
def supabase_configurado() -> bool:
    try:
        return bool(st.secrets["supabase"]["url"]) and bool(st.secrets["supabase"]["anon_key"])
    except Exception:
        return False


@st.cache_resource(show_spinner=False)
def _cliente():
    from supabase import create_client
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["anon_key"])


def _cliente_con_sesion():
    """Cliente con el access_token del usuario actual, para que las
    políticas RLS (auth.uid() = user_id) funcionen correctamente."""
    c = _cliente()
    sess = st.session_state.get("auth_session")
    if sess:
        try:
            c.postgrest.auth(sess["access_token"])
        except Exception:
            pass
    return c


# ============================================================
# Serialización del borrador (las fechas no son JSON-serializables)
# ============================================================
def _serializar(obj):
    if isinstance(obj, dict):
        return {k: _serializar(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serializar(v) for v in obj]
    if isinstance(obj, (date, datetime)):
        return {"__date__": obj.isoformat()}
    return obj


def _deserializar(obj):
    if isinstance(obj, dict):
        if set(obj.keys()) == {"__date__"}:
            try:
                return date.fromisoformat(obj["__date__"][:10])
            except ValueError:
                return None
        return {k: _deserializar(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_deserializar(v) for v in obj]
    return obj


def guardar_borrador(hc: dict):
    if not supabase_configurado() or "auth_user" not in st.session_state:
        return
    try:
        c = _cliente_con_sesion()
        user_id = st.session_state["auth_user"]["id"]
        c.table("historia_draft").upsert({
            "user_id": user_id,
            "data": _serializar(hc),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception as e:
        st.toast(f"No se pudo guardar el borrador: {e}", icon="⚠️")


def cargar_borrador():
    if not supabase_configurado() or "auth_user" not in st.session_state:
        return None
    try:
        c = _cliente_con_sesion()
        user_id = st.session_state["auth_user"]["id"]
        res = c.table("historia_draft").select("data").eq("user_id", user_id).limit(1).execute()
        if res.data:
            return _deserializar(res.data[0]["data"])
    except Exception:
        return None
    return None


# ============================================================
# Sesión única
# ============================================================
def _registrar_sesion_activa(user_id: str) -> str:
    token = str(uuid.uuid4())
    c = _cliente_con_sesion()
    c.table("active_sessions").upsert({
        "user_id": user_id, "session_token": token,
        "last_seen": datetime.now(timezone.utc).isoformat(),
    }).execute()
    return token


def _sesion_sigue_activa(user_id: str, token: str) -> bool:
    c = _cliente_con_sesion()
    res = c.table("active_sessions").select("session_token").eq("user_id", user_id).limit(1).execute()
    if not res.data:
        return False
    return res.data[0]["session_token"] == token


def _suscripcion_activa(user_id: str):
    c = _cliente_con_sesion()
    res = c.table("subscriptions").select("*").eq("user_id", user_id).limit(1).execute()
    if not res.data:
        return False, None
    row = res.data[0]
    if row["status"] != "active":
        return False, row
    if row.get("expires_at"):
        try:
            exp = datetime.fromisoformat(row["expires_at"].replace("Z", "+00:00"))
            if exp < datetime.now(timezone.utc):
                return False, row
        except ValueError:
            pass
    return True, row


def cerrar_sesion(borrar_activa: bool = True):
    if borrar_activa and supabase_configurado() and "auth_user" in st.session_state:
        try:
            c = _cliente_con_sesion()
            c.table("active_sessions").delete().eq("user_id", st.session_state["auth_user"]["id"]).execute()
        except Exception:
            pass
    for k in ["auth_user", "auth_session", "session_token", "tos_ok", "_last_revalidate", "sub_row"]:
        st.session_state.pop(k, None)
    st.rerun()


# ============================================================
# UI de login / registro
# ============================================================
def _pantalla_login():
    st.markdown(
        """
        <div style="text-align:center; padding: 2.2rem 0 1rem 0;">
            <div style="font-family:'Playfair Display', serif; font-weight:700; font-size:2rem; color:#101a34;">
                QuickChart
            </div>
            <div style="font-family:'Playfair Display', serif; font-style:italic; color:#8f6d3a; font-size:1.05rem;">
                Historia Clínica · Medicina Interna
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        with st.container(border=True):
            tab_login, tab_signup = st.tabs(["Iniciar sesión", "Crear cuenta"])

            with tab_login:
                email = st.text_input("Correo", key="login_email")
                pwd = st.text_input("Contraseña", type="password", key="login_pwd")
                if st.button("Entrar", type="primary", use_container_width=True):
                    _intentar_login(email, pwd)

            with tab_signup:
                email_s = st.text_input("Correo", key="signup_email")
                pwd_s = st.text_input("Contraseña (mínimo 6 caracteres)", type="password", key="signup_pwd")
                if st.button("Registrarme", use_container_width=True):
                    _intentar_signup(email_s, pwd_s)

    st.caption("¿Ya pagaste tu suscripción y no tienes acceso? Escribe a la persona que te dio este enlace.")


def _intentar_login(email, pwd):
    if not email or not pwd:
        st.error("Completa correo y contraseña.")
        return
    try:
        c = _cliente()
        res = c.auth.sign_in_with_password({"email": email, "password": pwd})
    except Exception as e:
        st.error(f"No se pudo iniciar sesión: {e}")
        return
    if not res.user:
        st.error("Correo o contraseña incorrectos.")
        return

    st.session_state["auth_user"] = {"id": res.user.id, "email": res.user.email}
    st.session_state["auth_session"] = {"access_token": res.session.access_token}

    ok, row = _suscripcion_activa(res.user.id)
    if not ok:
        st.session_state.pop("auth_user", None)
        st.session_state.pop("auth_session", None)
        st.error("Tu suscripción no está activa. Contacta a la persona que administra el acceso.")
        return

    token = _registrar_sesion_activa(res.user.id)
    st.session_state["session_token"] = token
    st.session_state["sub_row"] = row
    st.session_state["_last_revalidate"] = datetime.now(timezone.utc).timestamp()
    st.rerun()


def _intentar_signup(email, pwd):
    if not email or not pwd or len(pwd) < 6:
        st.error("Correo válido y contraseña de al menos 6 caracteres.")
        return
    try:
        c = _cliente()
        c.auth.sign_up({"email": email, "password": pwd})
    except Exception as e:
        st.error(f"No se pudo crear la cuenta: {e}")
        return
    st.success("Cuenta creada. Ya puedes iniciar sesión — tu acceso se activará cuando se confirme el pago de la suscripción.")


# ============================================================
# Punto de entrada — llamar al inicio de app.py
# ============================================================
def requerir_login() -> bool:
    """Devuelve True si hay una sesión válida y con suscripción activa.
    Si no, dibuja la pantalla de login/bloqueo y devuelve False."""
    if not supabase_configurado():
        st.info(
            "🔧 El acceso con cuenta todavía no está configurado (falta `st.secrets['supabase']`). "
            "Sigue `SUPABASE_SETUP.md` para activarlo. Mientras tanto, la app funciona en modo abierto.",
            icon="🔧",
        )
        return True

    if "auth_user" not in st.session_state:
        _pantalla_login()
        return False

    # Revalidación periódica (no en cada rerun, para no saturar la red)
    ahora = datetime.now(timezone.utc).timestamp()
    if ahora - st.session_state.get("_last_revalidate", 0) > _REVALIDATE_SEGUNDOS:
        user_id = st.session_state["auth_user"]["id"]
        token = st.session_state.get("session_token")
        if not _sesion_sigue_activa(user_id, token):
            st.warning("Tu sesión se cerró porque iniciaste sesión en otro dispositivo.")
            cerrar_sesion(borrar_activa=False)
            return False
        ok, row = _suscripcion_activa(user_id)
        if not ok:
            st.warning("Tu suscripción ya no está activa.")
            cerrar_sesion(borrar_activa=False)
            return False
        st.session_state["sub_row"] = row
        st.session_state["_last_revalidate"] = ahora

    return True
