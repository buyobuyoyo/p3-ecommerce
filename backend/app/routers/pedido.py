from fastapi import APIRouter, Depends
from app.database import supabase
from app.dependencies import get_current_user, require_role

router = APIRouter()


@router.post("/")
def crear_pedido(
    id_product: str,
    fecha_renta: str,
    fecha_devolucion: str,
    total: float,
    current_user=Depends(get_current_user)      
    ):  
    profile = (
        supabase.table("Profile")
        .select("id_profile")
        .eq("user_id", current_user.id)
        .single()
        .execute()
    )
    data = supabase.table("Pedido").insert({
        "id_profile": profile.data["id_profile"],
        "id_product": id_product,
        "fecha_renta": fecha_renta,
        "fecha_devolucion": fecha_devolucion,
        "estado": "activo",
        "total": total
    }).execute()
    return data


@router.get("/")
def obtener_pedidos(_user=Depends(require_role("admin"))):   
    data = supabase.table("Pedido").select("*").execute()
    return data


@router.get("/mis-pedidos")
def obtener_mis_pedidos(current_user=Depends(get_current_user)):  
    profile = (
        supabase.table("Profile")
        .select("id_profile")
        .eq("user_id", current_user.id)
        .single()
        .execute()
    )
    data = (
        supabase.table("Pedido")
        .select("*")
        .eq("id_profile", profile.data["id_profile"])
        .execute()
    )
    return data


@router.get("/{id_pedido}")
def obtener_pedido(id_pedido: str, _user=Depends(require_role("admin"))):  
    data = supabase.table("Pedido").select("*").eq("id_pedido", id_pedido).execute()
    return data


@router.put("/{id_pedido}")
def actualizar_pedido(
    id_pedido: str,
    estado: str,
    _user=Depends(require_role("admin"))         
):
    if not estado:
        return {"error": "No se envió ningún campo para actualizar"}
    data = supabase.table("Pedido").update({"estado": estado}).eq("id_pedido", id_pedido).execute()
    return data


@router.delete("/{id_pedido}")
def eliminar_pedido(id_pedido: str, _user=Depends(require_role("admin"))): 
    data = supabase.table("Pedido").delete().eq("id_pedido", id_pedido).execute()
    return data