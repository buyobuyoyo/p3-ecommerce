import { Product } from '../../core/domain/Product.js';

export class ProductApiAdapter {
    constructor(baseUrl) { this.baseUrl = baseUrl; }

    async listarTodos() {
        const res = await fetch(`${this.baseUrl}/product/`);
        const data = await res.json();
        return (data.data || []).map(item => new Product(item));
    }

    async obtener(id) {
        const res = await fetch(`${this.baseUrl}/product/${id}`);
        const data = await res.json();
        return new Product(data.data[0]);
    }

    async crear(datos, token) {
        const params = new URLSearchParams(datos);
        const res = await fetch(`${this.baseUrl}/product/?${params}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Error al crear producto");
        return await res.json();
    }

    async actualizar(id, campos, token) {
        const params = new URLSearchParams(campos);
        const res = await fetch(`${this.baseUrl}/product/${id}?${params}`, {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Error al actualizar producto");
        return await res.json();
    }

    async eliminar(id, token) {
        const res = await fetch(`${this.baseUrl}/product/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Error al eliminar producto");
        return await res.json();
    }
}
