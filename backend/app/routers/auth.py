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

from app.dependencies import get_current_user


router = APIRouter()
# # Instanciar el objeto
security = HTTPBearer()
# # Instanciar el objeto


# # ── Dependency reutilizable ──────────────────────────────────────────────────

# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    
#     # Valida el JWT que manda el frontend en el header:
#     # Authorization: Bearer <token>
#     # Devuelve el objeto user de Supabase, o lanza 401.
    
#     try:
#         user = supabase.auth.get_user(credentials.credentials)
#         if not user or not user.user:
#             raise HTTPException(status_code=401, detail="Token inválido o expirado")
#         return user.user
#     except Exception:
#         raise HTTPException(status_code=401, detail="No autorizado")


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

from fastapi.responses import RedirectResponse

@router.get("/callback")
def auth_callback(code: str = None):
    if not code:
        raise HTTPException(status_code=400, detail="No se recibió el código de autorización")
    
    try:
        # 1. Intercambiamos el código temporal por los tokens de sesión reales de Supabase
        res = supabase.auth.exchange_code_for_session({"auth_code": code})
        token_de_acceso = res.session.access_token
        
        # 2. Redirigimos automáticamente al navegador de vuelta a tu frontend (puerto 3000)
        # Pasamos el token limpio en el fragmento #hash de la URL
        return RedirectResponse(url=f"http://localhost:3000/login.html#access_token={token_de_acceso}")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al canjear el código de seguridad: {str(e)}")


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "metadata": current_user.user_metadata
    }




@router.post("/register")
def register(current_user=Depends(get_current_user)):
    """
    Crea el Profile del usuario autenticado si aún no existe.
    Se llama una vez después del primer login con GitHub.
    """
    existing = (
        supabase.table("Profile")
        .select("id_profile")
        .eq("user_id", current_user.id)
        .execute()
    )
    if existing.data:
        return {"mensaje": "El perfil ya existe"}

    email = current_user.email or ""
    metadata = current_user.user_metadata or {}

    data = supabase.table("Profile").insert({
        "user_id": current_user.id,
        "nombre": metadata.get("user_name", email),
        "apellido": "",
        "email": email,
        "rol": "cliente"          # rol por defecto
    }).execute()

    return {"mensaje": "Perfil creado correctamente", "data": data.data}



@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user = supabase.auth.get_user(credentials.credentials)
        supabase.auth.admin.sign_out(user.user.id)
        return {"mensaje": "Sesión cerrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cerrar sesión: {str(e)}")
    



    