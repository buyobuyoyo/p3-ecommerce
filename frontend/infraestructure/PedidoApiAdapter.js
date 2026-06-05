import { Pedido } from './Pedido.js';

export class PedidoApiAdapter {
    constructor(baseUrl) { this.baseUrl = baseUrl; }

    async misPedidos(token) {
        const res = await fetch(`${this.baseUrl}/pedido/mis-pedidos`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Error al obtener pedidos");
        const data = await res.json();
        return (data.data || []).map(item => new Pedido(item));
    }

    async todos(token) {
        const res = await fetch(`${this.baseUrl}/pedido/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("No autorizado");
        const data = await res.json();
        return (data.data || []).map(item => new Pedido(item));
    }

    async crear(datos, token) {
        const params = new URLSearchParams(datos);
        const res = await fetch(`${this.baseUrl}/pedido/?${params}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Error al crear pedido");
        return await res.json();
    }

    async actualizarEstado(id, estado, token) {
        const res = await fetch(`${this.baseUrl}/pedido/${id}?estado=${estado}`, {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Error al actualizar pedido");
        return await res.json();
    }
}