from fastapi import APIRouter
from app.database import supabase

router = APIRouter()

#Crear producto
@router.post("/")
def crear_product(titulo: str, descripcion: str, genero: str, precio: float, imgurl: str = None, duracion: int = None, lanzamiento: str = None):
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

#Obtener todos los productos
@router.get("/")
def obtener_products():
    data = supabase.table("Product").select("*").execute()
    return data

#Obtener un producto por ID
@router.get("/{id_product}")
def obtener_product(id_product: str):
    data = supabase.table("Product").select("*").eq("id_product", id_product).execute()
    return data

#Actualizar producto
@router.put("/{id_product}")
def actualizar_product(id_product: str, titulo: str = None, precio: float = None, disponible: bool = None, lanzamiento: str = None):
    data = supabase.table("Product").update({
        "titulo": titulo,
        "precio": precio,
        "disponible": disponible,
        "lanzamiento": lanzamiento
    }).eq("id_product", id_product).execute()
    return data

#Eliminar producto
@router.delete("/{id_product}")
def eliminar_product(id_product: str):
    data = supabase.table("Product").delete().eq("id_product", id_product).execute()
    return data