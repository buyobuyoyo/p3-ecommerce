"""
app/realtime/websocket_manager.py
───────────────────────────────────
Maneja las conexiones WebSocket activas.
Separado del router para mantener la arquitectura limpia.
"""

from fastapi import WebSocket


class WebSocketManager:
    """
    Registro de conexiones WebSocket activas por conversación.
    Permite enviar mensajes a todos los participantes de una sala.
    """

    def __init__(self):
        # conversacion_id -> lista de websockets conectados
        self.salas: dict[str, list[WebSocket]] = {}

    async def conectar(self, websocket: WebSocket, conversacion_id: str):
        await websocket.accept()
        if conversacion_id not in self.salas:
            self.salas[conversacion_id] = []
        self.salas[conversacion_id].append(websocket)

    def desconectar(self, websocket: WebSocket, conversacion_id: str):
        if conversacion_id in self.salas:
            self.salas[conversacion_id].remove(websocket)
            if not self.salas[conversacion_id]:
                del self.salas[conversacion_id]

    async def broadcast(self, conversacion_id: str, mensaje: dict):
        """Envía un mensaje a todos los conectados en una sala."""
        for ws in self.salas.get(conversacion_id, []):
            await ws.send_json(mensaje)


# Instancia global — compartida por todos los routers
manager = WebSocketManager()
