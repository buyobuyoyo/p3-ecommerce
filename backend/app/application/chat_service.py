
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
        msg_cliente = self.chat_repo.guardar_mensaje(Mensaje(
            contenido=contenido,
            remitente="cliente",
            conversacion_id=conversacion_id,
            timestamp=datetime.utcnow(),
        ))

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

        return self.chat_repo.obtener_mensajes(conversacion_id)

    def obtener_conversaciones(self) -> list[Conversacion]:

        return self.chat_repo.obtener_conversaciones()
