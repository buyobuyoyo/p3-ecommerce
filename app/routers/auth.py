from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import supabase

router = APIRouter()
security = HTTPBearer()


# ── Dependency reutilizable ──────────────────────────────────────────────────

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Valida el JWT que manda el frontend en el header:
        Authorization: Bearer <token>
    Devuelve el objeto user de Supabase, o lanza 401.
    """
    try:
        user = supabase.auth.get_user(credentials.credentials)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        return user.user
    except Exception:
        raise HTTPException(status_code=401, detail="No autorizado")


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/login/github")
def login_github():
    """
    Paso 1 del flujo OAuth 2:
    Devuelve la URL de GitHub donde el usuario autoriza la app.
    El frontend debe redirigir al usuario a esta URL.
    """
    response = supabase.auth.sign_in_with_oauth({
        "provider": "github",
        "options": {
            # Supabase redirige aquí tras autenticar; el frontend captura el token
            "redirect_to": "http://localhost:8000/auth/callback"
        }
    })
    return {"url": response.url}


@router.get("/callback")
def auth_callback(code: str = None, error: str = None):
    """
    Paso 2 del flujo OAuth 2:
    GitHub redirige aquí con un `code`. Supabase lo intercambia por un JWT.

    Nota: Supabase normalmente maneja este intercambio del lado del cliente
    (usando su SDK JS). Si usas un frontend JS, este endpoint no es necesario.
    Si el flujo es 100% server-side, aquí es donde procesas el code.
    """
    if error:
        raise HTTPException(status_code=400, detail=f"Error OAuth: {error}")

    if not code:
        raise HTTPException(status_code=400, detail="No se recibió código de autorización")

    # En flujo server-side puro podrías intercambiar el code aquí.
    # Con Supabase + frontend JS el SDK cliente maneja esto automáticamente.
    return {"mensaje": "Callback recibido. El frontend debe completar el intercambio con el SDK de Supabase."}


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """
    Devuelve los datos del usuario autenticado.
    Útil para que el frontend sepa quién está logueado.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "metadata": current_user.user_metadata
    }


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Invalida la sesión del usuario en Supabase.
    El frontend también debe limpiar el token de su storage local.
    """
    try:
        supabase.auth.sign_out()
        return {"mensaje": "Sesión cerrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cerrar sesión: {str(e)}")