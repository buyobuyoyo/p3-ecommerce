export class ChatAdapter {
    constructor(wsUrl) {
        this.wsUrl = wsUrl;
        this.socket = null;
    }

    async iniciarConversacion(token, baseUrl) {
        const res = await fetch(`${baseUrl}/chat/conversacion`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("No se pudo iniciar conversación");
        const data = await res.json();
        return data.conversacion_id;
    }

    conectar(conversacionId, onMensaje, onError) {
        this.socket = new WebSocket(`${this.wsUrl}/chat/ws/${conversacionId}`);
        this.socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                onMensaje(data);
            } catch {
                onMensaje({ remitente: 'asistente', contenido: event.data });
            }
        };
        this.socket.onerror = () => onError && onError("Error de conexión");
        this.socket.onclose = () => console.log("Chat desconectado");
    }

    enviar(mensaje) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(mensaje);
        }
    }

    desconectar() {
        if (this.socket) this.socket.close();
    }
}
