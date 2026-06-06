
from fastapi import WebSocket


class WebSocketManager:


    def __init__(self):
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

        for ws in self.salas.get(conversacion_id, []):
            await ws.send_json(mensaje)


manager = WebSocketManager()
