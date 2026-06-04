from fastapi import APIRouter, HTTPException, Depends
# ── Todas estas cosas ya vienen de FastAPI 
# Depends: Es un sistema de "dependencias".
# Sirve para decir: "Para ejecutar esta función, dependo de que esta otra cosa ocurra primero" (como revisar si el usuario está logueado).

from fastapi.responses import RedirectResponse
# ── Movimiento entre páginas 

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# ── FastAPI Security: herramientas ya especializadas en la protección de datos 
# HTTPBearer: Es un estándar de seguridad. Indica que el servidor espera un token para dejar pasar a alguien
# HTTPAuthorizationCredentials: Es la caja donde FastAPI guarda ese token una vez que el usuario lo envía, para poder revisarlo fácilmente

from app.database import supabase
# ── Comunicación con Supabase, que es donde tenemos la base de datos y la autenticación



router = APIRouter()
# Instanciar el objeto
security = HTTPBearer()
# Instanciar el objeto


# ── Dependency reutilizable ──────────────────────────────────────────────────

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    # Valida el JWT que manda el frontend en el header:
    # Authorization: Bearer <token>
    # Devuelve el objeto user de Supabase, o lanza 401.
    
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
 
    # Paso 1 del flujo OAuth 2:
    # Devuelve la URL de GitHub donde el usuario autoriza la app.
    # El frontend debe redirigir al usuario a esta URL.
   
    response = supabase.auth.sign_in_with_oauth({
        "provider": "github",
        "options": {

            # Supabase redirige aquí tras autenticar; el frontend captura el token
            "redirect_to": "http://localhost:8000/auth/callback"
        }
    })
    return {"url": response.url}


@router.get("/callback")

def auth_callback():
    return {"mensaje": "Autenticación exitosa. Copia el access_token del fragmento #hash de la URL."}

# Código viejo que parece no funcionar porque aún no hay front que transforme el token de GitHub en un JWT de Supa.
# def auth_callback(code: str = None, error: str = None):
    # code: str = None: Es una variable que espera recibir un "código temporal" de GitHub. Es como un vale que luego se canjea por la llave (token) real.
    # error: str = None: Si algo salió mal en GitHub (por ejemplo, el usuario le dio a "Cancelar"), GitHub enviará el motivo del error aquí.
    
    # Paso 2 del flujo OAuth 2:
    # GitHub redirige aquí con un `code`. Supabase lo intercambia por un JWT.

    # Nota: Supabase normalmente maneja este intercambio del lado del cliente
    # (usando su SDK JS). Si usas un frontend JS, este endpoint no es necesario.
    # Si el flujo es 100% server-side, aquí es donde procesas el code.
    
    # if error:
    #     raise HTTPException(status_code=400, detail=f"Error OAuth: {error}")
    
    # # Revisa si la variable error trae algo. Código 400 (que significa "Petición incorrecta")

    # if not code:
    #     raise HTTPException(status_code=400, detail="No se recibió código de autorización")

    # # Si no hay error, pero tampoco llegó el code (el vale de GitHub), significa que la comunicación se cortó o es inválida.

    # return {"mensaje": "Callback recibido. El frontend debe completar el intercambio con el SDK de Supabase."}


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
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