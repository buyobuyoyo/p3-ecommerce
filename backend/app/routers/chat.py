"""
app/routers/chat.py
────────────────────
Adaptador HTTP/WebSocket — capa más externa de la arquitectura hexagonal.
Conecta FastAPI con los casos de uso del chat.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.application.chat_service import ChatService
from app.infrastructure.chat_repository import SupabaseChatRepository
from app.infrastructure.faq_repository import FAQRepository
from app.realtime.websocket_manager import manager
from app.dependencies import get_current_user

router = APIRouter()


def get_chat_service() -> ChatService:
    """Inyección de dependencias — aquí se conectan los puertos con sus adaptadores."""
    return ChatService(
        chat_repo=SupabaseChatRepository(),
        respuesta_auto=FAQRepository(),
    )



@router.post("/conversacion")
def iniciar_conversacion(
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    """Cliente inicia una nueva conversación."""
    conv = service.iniciar_conversacion(current_user.id)
    return {"conversacion_id": conv.id, "estado": conv.estado}


@router.get("/conversacion/{conversacion_id}/historial")
def obtener_historial(
    conversacion_id: str,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    """Obtiene el historial de mensajes de una conversación."""
    mensajes = service.obtener_historial(conversacion_id)
    return [
        {
            "id": m.id,
            "contenido": m.contenido,
            "remitente": m.remitente,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in mensajes
    ]


@router.get("/conversaciones")
def obtener_conversaciones(
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    """Admin obtiene todas las conversaciones."""
    convs = service.obtener_conversaciones()
    return [{"id": c.id, "user_id": c.user_id, "estado": c.estado} for c in convs]



@router.websocket("/ws/{conversacion_id}")
async def websocket_chat(
    websocket: WebSocket,
    conversacion_id: str,
    service: ChatService = Depends(get_chat_service),
):
    """
    Endpoint WebSocket del chat.
    El cliente se conecta y envía mensajes en texto plano.
    El servidor responde con JSON:
        { "remitente": "cliente"|"asistente", "contenido": "...", "timestamp": "..." }
    """
    await manager.conectar(websocket, conversacion_id)
    try:
        while True:
            texto = await websocket.receive_text()

            msg_cliente, msg_asistente = service.procesar_mensaje(conversacion_id, texto)

            await manager.broadcast(conversacion_id, {
                "remitente": "cliente",
                "contenido": msg_cliente.contenido,
                "timestamp": msg_cliente.timestamp.isoformat(),
            })

            if msg_asistente:
                await manager.broadcast(conversacion_id, {
                    "remitente": "asistente",
                    "contenido": msg_asistente.contenido,
                    "timestamp": msg_asistente.timestamp.isoformat(),
                })

    except WebSocketDisconnect:
        manager.desconectar(websocket, conversacion_id)


from app.dependencies import get_current_user, require_role

@router.get("/conversaciones")
def obtener_conversaciones(
    _user=Depends(require_role("admin")),
    service: ChatService = Depends(get_chat_service),
):
    """Admin obtiene todas las conversaciones."""
    convs = service.obtener_conversaciones()
    return [{"id": c.id, "user_id": c.user_id, "estado": c.estado} for c in convs]


@router.post("/conversacion/{conversacion_id}/responder")
async def admin_responder(
    conversacion_id: str,
    contenido: str,
    _user=Depends(require_role("admin")),
    service: ChatService = Depends(get_chat_service),
):
    """Admin envía un mensaje a una conversación."""
    from datetime import datetime
    from app.domain.entities import Mensaje
    from app.infrastructure.chat_repository import SupabaseChatRepository

    repo = SupabaseChatRepository()
    msg = repo.guardar_mensaje(Mensaje(
        contenido=contenido,
        remitente="admin",
        conversacion_id=conversacion_id,
        timestamp=datetime.utcnow(),
    ))

    await manager.broadcast(conversacion_id, {
        "remitente": "admin",
        "contenido": msg.contenido,
        "timestamp": msg.timestamp.isoformat(),
    })

    return {"ok": True, "mensaje_id": msg.id}
