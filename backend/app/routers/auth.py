from fastapi import APIRouter, HTTPException, Depends

from fastapi.responses import RedirectResponse

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import supabase

from app.dependencies import get_current_user


router = APIRouter()
security = HTTPBearer()



    
    



@router.get("/login/github")
def login_github():
 
   
    response = supabase.auth.sign_in_with_oauth({
        "provider": "github",
        "options": {

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
        res = supabase.auth.exchange_code_for_session({"auth_code": code})
        token_de_acceso = res.session.access_token
        
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
        "rol": "cliente"
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
    



    