"""
app/dependencies.py
───────────────────
Dependencias reutilizables de FastAPI.
Importa `get_current_user` en cualquier router para proteger sus endpoints.

Uso:
    from app.dependencies import get_current_user
    from fastapi import Depends

    @router.get("/")
    def mi_endpoint(user = Depends(get_current_user)):
        return {"user_id": user.id}
"""

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import supabase

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Valida el JWT enviado en el header Authorization: Bearer <token>.
    Devuelve el objeto user de Supabase.
    Lanza HTTP 401 si el token es inválido o expiró.
    """
    try:
        user = supabase.auth.get_user(credentials.credentials)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        return user.user
    except Exception:
        raise HTTPException(status_code=401, detail="No autorizado")