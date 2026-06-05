"""
app/domain/ports.py
───────────────────
Puertos (interfaces abstractas) del dominio.
Definen QUÉ se necesita hacer, sin importar CÓMO se hace.
Esto permite reemplazar implementaciones sin tocar el núcleo del negocio.
"""

from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities import Mensaje, Conversacion


class RespuestaAutomaticaPort(ABC):
    """
    Puerto para el motor de respuestas automáticas.
    Hoy puede ser búsqueda simple por keywords.
    Mañana puede ser un LLM, embeddings, RAG, etc.
    Solo hay que crear una nueva clase que implemente este puerto.
    """

    @abstractmethod
    def obtener_respuesta(self, texto: str) -> Optional[str]:
        """
        Recibe el mensaje del cliente.
        Devuelve una respuesta automática, o None si no hay coincidencia.
        """
        ...


class ChatRepositoryPort(ABC):
    """Puerto para persistencia de mensajes y conversaciones."""

    @abstractmethod
    def guardar_mensaje(self, mensaje: Mensaje) -> Mensaje:
        ...

    @abstractmethod
    def obtener_mensajes(self, conversacion_id: str) -> list[Mensaje]:
        ...

    @abstractmethod
    def crear_conversacion(self, user_id: str) -> Conversacion:
        ...

    @abstractmethod
    def obtener_conversacion(self, conversacion_id: str) -> Optional[Conversacion]:
        ...

    @abstractmethod
    def obtener_conversaciones(self) -> list[Conversacion]:
        ...
