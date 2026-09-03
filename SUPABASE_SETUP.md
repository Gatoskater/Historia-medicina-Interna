# Configuración de Supabase — Cuentas, Suscripción, Sesión Única y Autosave

## Por qué esta arquitectura (y no una "key" suelta)

Consulté esto porque es una decisión que conviene dejar bien fundamentada:

**No recomiendo una "key" compartida** (un código que repartes por WhatsApp).
Es fácil de reenviar sin que te enteres, no puedes revocar a UNA persona sin
invalidar a todos los demás, y no queda registro de quién es quién.

**Sí recomiendo cuentas reales (correo + contraseña) con una suscripción
asociada**, que es como funciona cualquier SaaS (Netflix, Notion, etc.):

- Cada usuario se registra con su correo → tiene una identidad real.
- Tú activas su suscripción manualmente en Supabase después de que te pague
  (por ahora; más adelante se puede automatizar con Stripe/PayPal).
- Puedes desactivar a una sola persona sin afectar a las demás.
- La "sesión única" se controla con una tabla que guarda cuál es el
  navegador/dispositivo activo de cada usuario — si alguien más entra con
  el mismo correo, el primero se desconecta automáticamente.
- Con contraseña + Supabase Auth, además tienes recuperación de contraseña
  gratis, sin que tengas que construir nada de eso.

## Paso 1 — Crear el proyecto

1. Entra a https://supabase.com, inicia sesión con la cuenta que ya tienes.
2. "New project" → nómbralo (ej. `historia-clinica-jade`) → elige una
   contraseña de base de datos (guárdala, no la necesitarás en el día a día
   pero es tu respaldo) → elige la región más cercana → "Create".
3. Espera 1-2 minutos a que aprovisione el proyecto.

## Paso 2 — Activar inicio de sesión por correo/contraseña

1. En el menú lateral: **Authentication → Providers**.
2. Confirma que "Email" esté habilitado (lo está por defecto).
3. **Authentication → Settings** (o "URL Configuration"): por ahora puedes
   dejar "Confirm email" activado (pide confirmar el correo) o desactivarlo
   si quieres que la gente entre de inmediato tras registrarse. Para
   arrancar rápido, te sugiero **desactivarlo** al inicio y reactivarlo
   cuando ya tengas usuarios reales pagando.

## Paso 3 — Crear las tablas (SQL Editor)

Ve a **SQL Editor → New query**, pega esto completo y dale "Run":

```sql
-- ============================================================
-- 1. Suscripciones — el "interruptor" de acceso de cada usuario
-- ============================================================
create table public.subscriptions (
  user_id uuid primary key references auth.users(id) on delete cascade,
  status text not null default 'inactive'
    check (status in ('active','inactive','expired','canceled')),
  plan text default 'mensual',
  expires_at timestamptz,
  tos_accepted_at timestamptz,
  created_at timestamptz default now()
);

alter table public.subscriptions enable row level security;

-- Un usuario solo puede LEER su propia fila (para saber si está activo)
create policy "select_own_subscription"
  on public.subscriptions for select
  using (auth.uid() = user_id);

-- Un usuario SÍ puede marcar que aceptó los términos (solo esa columna
-- importa aquí; el status lo cambias tú manualmente desde el Table Editor)
create policy "update_own_tos"
  on public.subscriptions for update
  using (auth.uid() = user_id);

-- Crea automáticamente la fila de suscripción (inactiva) cuando alguien
-- se registra — así nunca activas nada sin querer.
create function public.handle_new_user()
returns trigger as $$
begin
  insert into public.subscriptions (user_id, status) values (new.id, 'inactive');
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- ============================================================
-- 2. Sesión activa — para permitir solo 1 dispositivo a la vez
-- ============================================================
create table public.active_sessions (
  user_id uuid primary key references auth.users(id) on delete cascade,
  session_token text not null,
  last_seen timestamptz default now()
);

alter table public.active_sessions enable row level security;

create policy "select_own_session"
  on public.active_sessions for select using (auth.uid() = user_id);
create policy "insert_own_session"
  on public.active_sessions for insert with check (auth.uid() = user_id);
create policy "update_own_session"
  on public.active_sessions for update using (auth.uid() = user_id);

-- ============================================================
-- 3. Borrador de la historia — autosave por usuario
-- ============================================================
create table public.historia_draft (
  user_id uuid primary key references auth.users(id) on delete cascade,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz default now()
);

alter table public.historia_draft enable row level security;

create policy "select_own_draft"
  on public.historia_draft for select using (auth.uid() = user_id);
create policy "insert_own_draft"
  on public.historia_draft for insert with check (auth.uid() = user_id);
create policy "update_own_draft"
  on public.historia_draft for update using (auth.uid() = user_id);
```

Si todo corrió sin errores rojos, ya tienes las 3 tablas con seguridad a
nivel de fila (RLS): cada usuario solo puede tocar SU PROPIA fila en cada
tabla — ni con la contraseña de otro podrían ver los datos de alguien más.

## Paso 4 — Copiar tus llaves

**Project Settings → API**:
- `Project URL` (algo como `https://xxxxx.supabase.co`)
- `anon public` key (una cadena larga) — **esta es segura de usar en la
  app**, porque las políticas RLS de arriba ya restringen qué puede hacer
  cada usuario con ella.
- **NUNCA** copies la `service_role` key a la app ni a Streamlit Cloud; esa
  key se salta todas las reglas de seguridad. Solo la usarías tú mismo,
  manualmente, si algún día construyes automatización de pagos.

## Paso 5 — Pegar las llaves en Streamlit

**En tu computadora (para probar local):** crea el archivo
`.streamlit/secrets.toml` (NO lo subas a GitHub — ya está en `.gitignore`)
con este contenido, reemplazando con tus valores reales:

```toml
[supabase]
url = "https://xxxxx.supabase.co"
anon_key = "tu-anon-key-aqui"
```

**En Streamlit Community Cloud (para producción):** entra a tu app →
menú (⋮) → **Settings → Secrets** → pega el mismo contenido de arriba →
Save. La app se reinicia sola y ya queda conectada.

## Paso 6 — Activar tu propia cuenta para probar

1. Corre la app, regístrate con tu correo desde la pantalla de login.
2. Ve a Supabase → **Table Editor → subscriptions** → busca la fila con tu
   `user_id` → edita la columna `status` a `active` → en `expires_at` pon
   una fecha lejana (ej. dentro de 1 año) → Save.
3. Vuelve a la app y entra: ya deberías tener acceso completo.

## Cómo activas a un cliente que te paga

Cada vez que alguien te pague la suscripción mensual: Table Editor →
`subscriptions` → busca su fila (por `user_id`; puedes cruzarlo con su
correo en **Authentication → Users**) → cambia `status` a `active` y
`expires_at` a la fecha en que vence ese mes. Cuando quieras cortarle el
acceso, cambias `status` a `expired` o `canceled` — se le cierra la sesión
la próxima vez que la app revise (máximo ~30 segundos después, ver más abajo).

## Sobre "temporizador" en la key

No uses una key con expiración propia — usa el campo `expires_at` de la
tabla `subscriptions`, que ya es exactamente eso: la app revisa en cada
inicio de sesión (y periódicamente mientras la usan) si `expires_at` ya
pasó, y si pasó, bloquea el acceso automáticamente aunque tú te olvides de
desactivarlo a mano. Es más simple y más seguro que fechas dentro de una key.
