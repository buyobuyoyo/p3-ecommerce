from fastapi import APIRouter, Depends
from app.database import supabase
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/")
def crear_product(
    titulo: str,
    descripcion: str,
    genero: str,
    precio: float,
    imgurl: str = None,
    duracion: int = None,
    lanzamiento: str = None,
    _user=Depends(get_current_user)          # 🔒
):
    data = supabase.table("Product").insert({
        "titulo": titulo,
        "descripcion": descripcion,
        "genero": genero,
        "precio": precio,
        "disponible": True,
        "imgurl": imgurl,
        "duracion": duracion,
        "lanzamiento": lanzamiento
    }).execute()
    return data


# GET / es público — el catálogo de películas no requiere login
@router.get("/")
def obtener_products():
    data = supabase.table("Product").select("*").execute()
    return data


# GET por ID también público
@router.get("/{id_product}")
def obtener_product(id_product: str):
    data = supabase.table("Product").select("*").eq("id_product", id_product).execute()
    return data


@router.put("/{id_product}")
def actualizar_product(
    id_product: str,
    titulo: str = None,
    precio: float = None,
    disponible: bool = None,
    lanzamiento: str = None,
    _user=Depends(get_current_user)          # 🔒
):
    data = supabase.table("Product").update({
        "titulo": titulo,
        "precio": precio,
        "disponible": disponible,
        "lanzamiento": lanzamiento
    }).eq("id_product", id_product).execute()
    return data


@router.delete("/{id_product}")
def eliminar_product(id_product: str, _user=Depends(get_current_user)):  # 🔒
    data = supabase.table("Product").delete().eq("id_product", id_product).execute()
    return data