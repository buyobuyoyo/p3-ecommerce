from fastapi import APIRouter
from app.database import supabase

router = APIRouter()

#Crear perfil
@router.post("/")
def crear_profile(nombre: str, apellido: str, email: str, telefono: str = None):
    data = supabase.table("Profile").insert({
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "telefono": telefono
    }).execute()
    return data

#Obtener todos los perfiles
@router.get("/")
def obtener_profiles():
    data = supabase.table("Profile").select("*").execute()
    return data

#Obtener un perfil por ID
@router.get("/{id_profile}")
def obtener_profile(id_profile: str):
    data = supabase.table("Profile").select("*").eq("id_profile", id_profile).execute()
    return data

#Actualizar perfil
@router.put("/{id_profile}")
def actualizar_profile(id_profile: str, nombre: str = None, apellido: str = None, telefono: str = None):
    data = supabase.table("Profile").update({
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono
    }).eq("id_profile", id_profile).execute()
    return data

#Eliminar perfil
@router.delete("/{id_profile}")
def eliminar_profile(id_profile: str):
    data = supabase.table("Profile").delete().eq("id_profile", id_profile).execute()
    return data