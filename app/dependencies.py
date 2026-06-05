from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import supabase

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user = supabase.auth.get_user(credentials.credentials)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        return user.user
    except Exception:
        raise HTTPException(status_code=401, detail="No autorizado")


def require_role(required_role: str):
    """
    Fábrica de dependencias. Uso:
        _user = Depends(require_role("admin"))
    Verifica que el usuario tenga el rol requerido en su Profile.
    """
    def role_checker(current_user=Depends(get_current_user)):
        profile = (
            supabase.table("Profile")
            .select("rol")
            .eq("user_id", current_user.id)
            .single()
            .execute()
        )
        if not profile.data or profile.data.get("rol") != required_role:
            raise HTTPException(status_code=403, detail="No tienes permiso para esta acción")
        return current_user
    return role_checker