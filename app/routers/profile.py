from fastapi import APIRouter, Depends
from app.database import supabase
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/")
def crear_profile(
    nombre: str,
    apellido: str,
    email: str,
    telefono: str = None,
    _user=Depends(get_current_user)          # 🔒 requiere token válido
):
    data = supabase.table("Profile").insert({
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "telefono": telefono
    }).execute()
    return data


@router.get("/")
def obtener_profiles(_user=Depends(get_current_user)):   # 🔒
    data = supabase.table("Profile").select("*").execute()
    return data


@router.get("/{id_profile}")
def obtener_profile(id_profile: str, _user=Depends(get_current_user)):  # 🔒
    data = supabase.table("Profile").select("*").eq("id_profile", id_profile).execute()
    return data


@router.put("/{id_profile}")
def actualizar_profile(
    id_profile: str,
    nombre: str = None,
    apellido: str = None,
    telefono: str = None,
    _user=Depends(get_current_user)          # 🔒
):
    data = supabase.table("Profile").update({
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono
    }).eq("id_profile", id_profile).execute()
    return data


@router.delete("/{id_profile}")
def eliminar_profile(id_profile: str, _user=Depends(get_current_user)):  # 🔒
    data = supabase.table("Profile").delete().eq("id_profile", id_profile).execute()
    return data

