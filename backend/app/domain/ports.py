

from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities import Mensaje, Conversacion


class RespuestaAutomaticaPort(ABC):


    @abstractmethod
    def obtener_respuesta(self, texto: str) -> Optional[str]:
        ...


class ChatRepositoryPort(ABC):

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
