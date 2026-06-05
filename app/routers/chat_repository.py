"""
app/infrastructure/chat_repository.py
───────────────────────────────────────
Adaptador de persistencia. Implementa ChatRepositoryPort usando Supabase.
Para cambiar a otra BD: crear nueva clase que implemente ChatRepositoryPort.
"""

import uuid
from datetime import datetime
from typing import Optional

from app.domain.entities import Mensaje, Conversacion
from app.domain.ports import ChatRepositoryPort
from app.database import supabase


class SupabaseChatRepository(ChatRepositoryPort):

    def crear_conversacion(self, user_id: str) -> Conversacion:
        conv_id = str(uuid.uuid4())
        supabase.table("Conversacion").insert({
            "id_conversacion": conv_id,
            "user_id": user_id,
            "estado": "abierta",
        }).execute()
        return Conversacion(id=conv_id, user_id=user_id)

    def obtener_conversacion(self, conversacion_id: str) -> Optional[Conversacion]:
        result = (
            supabase.table("Conversacion")
            .select("*")
            .eq("id_conversacion", conversacion_id)
            .single()
            .execute()
        )
        if not result.data:
            return None
        d = result.data
        return Conversacion(
            id=d["id_conversacion"],
            user_id=d["user_id"],
            estado=d["estado"],
        )

    def obtener_conversaciones(self) -> list[Conversacion]:
        result = supabase.table("Conversacion").select("*").execute()
        return [
            Conversacion(id=d["id_conversacion"], user_id=d["user_id"], estado=d["estado"])
            for d in (result.data or [])
        ]

    def guardar_mensaje(self, mensaje: Mensaje) -> Mensaje:
        msg_id = str(uuid.uuid4())
        supabase.table("Mensaje").insert({
            "id_mensaje": msg_id,
            "conversacion_id": mensaje.conversacion_id,
            "contenido": mensaje.contenido,
            "remitente": mensaje.remitente,
            "timestamp": mensaje.timestamp.isoformat(),
        }).execute()
        mensaje.id = msg_id
        return mensaje

    def obtener_mensajes(self, conversacion_id: str) -> list[Mensaje]:
        result = (
            supabase.table("Mensaje")
            .select("*")
            .eq("conversacion_id", conversacion_id)
            .order("timestamp")
            .execute()
        )
        return [
            Mensaje(
                id=d["id_mensaje"],
                contenido=d["contenido"],
                remitente=d["remitente"],
                conversacion_id=d["conversacion_id"],
                timestamp=datetime.fromisoformat(d["timestamp"]),
            )
            for d in (result.data or [])
        ]
