
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Mensaje:
    contenido: str
    remitente: str          # "cliente" | "asistente"
    conversacion_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    id: Optional[str] = None


@dataclass
class Conversacion:
    id: str
    user_id: str
    estado: str = "abierta"   # "abierta" | "cerrada"
    creada_en: datetime = field(default_factory=datetime.utcnow)
