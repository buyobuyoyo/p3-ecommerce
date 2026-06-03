from fastapi import APIRouter, Depends
from app.database import supabase
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/")
def crear_pedido(
    id_profile: str,
    id_product: str,
    fecha_renta: str,
    fecha_devolucion: str,
    total: float,
    _user=Depends(get_current_user)          # 🔒
):
    data = supabase.table("Pedido").insert({
        "id_profile": id_profile,
        "id_product": id_product,
        "fecha_renta": fecha_renta,
        "fecha_devolucion": fecha_devolucion,
        "estado": "activo",
        "total": total
    }).execute()
    return data


@router.get("/")
def obtener_pedidos(_user=Depends(get_current_user)):    # 🔒
    data = supabase.table("Pedido").select("*").execute()
    return data


@router.get("/{id_pedido}")
def obtener_pedido(id_pedido: str, _user=Depends(get_current_user)):    # 🔒
    data = supabase.table("Pedido").select("*").eq("id_pedido", id_pedido).execute()
    return data


@router.put("/{id_pedido}")
def actualizar_pedido(
    id_pedido: str,
    estado: str,
    _user=Depends(get_current_user)          # 🔒
):
    data = supabase.table("Pedido").update({
        "estado": estado
    }).eq("id_pedido", id_pedido).execute()
    return data


@router.delete("/{id_pedido}")
def eliminar_pedido(id_pedido: str, _user=Depends(get_current_user)):   # 🔒
    data = supabase.table("Pedido").delete().eq("id_pedido", id_pedido).execute()
    return data