"""
app/application/chat_service.py
────────────────────────────────
Capa de aplicación — casos de uso del chat.
Orquesta el dominio sin depender de FastAPI, Supabase, ni WebSockets.
Solo habla con puertos (interfaces), nunca con implementaciones concretas.
"""

from datetime import datetime
from typing import Optional

from app.domain.entities import Mensaje, Conversacion
from app.domain.ports import ChatRepositoryPort, RespuestaAutomaticaPort


class ChatService:
    """
    Casos de uso del sistema de chat.
    Recibe puertos inyectados — fácil de testear y de escalar.
    """

    def __init__(
        self,
        chat_repo: ChatRepositoryPort,
        respuesta_auto: RespuestaAutomaticaPort,
    ):
        self.chat_repo = chat_repo
        self.respuesta_auto = respuesta_auto

    def iniciar_conversacion(self, user_id: str) -> Conversacion:
        """Caso de uso: cliente inicia una nueva conversación."""
        return self.chat_repo.crear_conversacion(user_id)

    def procesar_mensaje(self, conversacion_id: str, contenido: str) -> tuple[Mensaje, Optional[Mensaje]]:
        """
        Caso de uso principal: procesa un mensaje del cliente.
        1. Guarda el mensaje del cliente.
        2. Busca respuesta automática.
        3. Si hay respuesta, guarda y devuelve el mensaje del asistente.
        Devuelve (mensaje_cliente, mensaje_asistente | None)
        """
        # Guardar mensaje del cliente
        msg_cliente = self.chat_repo.guardar_mensaje(Mensaje(
            contenido=contenido,
            remitente="cliente",
            conversacion_id=conversacion_id,
            timestamp=datetime.utcnow(),
        ))

        # Intentar respuesta automática
        respuesta = self.respuesta_auto.obtener_respuesta(contenido)
        msg_asistente = None

        if respuesta:
            msg_asistente = self.chat_repo.guardar_mensaje(Mensaje(
                contenido=respuesta,
                remitente="asistente",
                conversacion_id=conversacion_id,
                timestamp=datetime.utcnow(),
            ))

        return msg_cliente, msg_asistente

    def obtener_historial(self, conversacion_id: str) -> list[Mensaje]:
        """Caso de uso: obtener historial de una conversación."""
        return self.chat_repo.obtener_mensajes(conversacion_id)

    def obtener_conversaciones(self) -> list[Conversacion]:
        """Caso de uso: admin obtiene todas las conversaciones."""
        return self.chat_repo.obtener_conversaciones()
