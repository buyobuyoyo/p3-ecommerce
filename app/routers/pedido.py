
#Los tres routers siguen la misma estructura, solo cambia la tabla y los campos que manejan

from fastapi import APIRouter
from app.database import supabase

router = APIRouter()

#Crear pedido
@router.post("/")
def crear_pedido(id_profile: str, id_product: str, fecha_renta: str, fecha_devolucion: str, total: float):
    data = supabase.table("Pedido").insert({
        "id_profile": id_profile,
        "id_product": id_product,
        "fecha_renta": fecha_renta,
        "fecha_devolucion": fecha_devolucion,
        "estado": "activo",
        "total": total
    }).execute()
    return data

#Obtener todos los pedidos
@router.get("/")
def obtener_pedidos():
    data = supabase.table("Pedido").select("*").execute()
    return data

#Obtener un pedido por ID
@router.get("/{id_pedido}")
def obtener_pedido(id_pedido: str):
    data = supabase.table("Pedido").select("*").eq("id_pedido", id_pedido).execute()
    return data

#Actualizar estado del pedido
@router.put("/{id_pedido}")
def actualizar_pedido(id_pedido: str, estado: str):
    data = supabase.table("Pedido").update({
        "estado": estado
    }).eq("id_pedido", id_pedido).execute()
    return data

#Eliminar pedido
@router.delete("/{id_pedido}")
def eliminar_pedido(id_pedido: str):
    data = supabase.table("Pedido").delete().eq("id_pedido", id_pedido).execute()
    return data


"""
from fastapi import APIRouter trae el sistema de rutas de FastAPI
from app.database import supabase trae la conexión a Supabase que hicimos en database.py
router = APIRouter() crea el enrutador, es como una mini-app solo para Profile

Cada endpoint sigue el mismo patrón:
@router.post("/") decorador que le dice a FastAPI qué método HTTP usa y en qué URL
def crear_profile(...) la función que se ejecuta cuando alguien llama ese endpoint
supabase.table("Profile").insert({...}) le dice a Supabase inserta esto en tal tabla
.execute() ejecuta la operación
return data devuelve el resultado

Las diferencias entre endpoints:
.insert() CREATE (POST)
.select("*") READ (GET), el * significa "todos los campos"
.eq("id_profile", id_profile) significa "donde id_profile sea igual a este valor"
.update() UPDATE (PUT)
.delete() DELETE
"""