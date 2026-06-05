import { AuthApiAdapter } from '../infrastructure/api/AuthApiAdapter.js';
import { ProductApiAdapter } from '../infrastructure/api/ProductApiAdapter.js';
import { PedidoApiAdapter } from '../infrastructure/api/PedidoApiAdapter.js';
import { ChatAdapter } from '../infrastructure/websocket/ChatAdapter.js';

export const BACKEND = 'http://localhost:8000';
export const WS_BACKEND = 'ws://localhost:8000';

export const authAdapter   = new AuthApiAdapter(BACKEND);
export const productAdapter = new ProductApiAdapter(BACKEND);
export const pedidoAdapter  = new PedidoApiAdapter(BACKEND);
export const chatAdapter    = new ChatAdapter(WS_BACKEND);

export function getToken() {
    return localStorage.getItem('token');
}

export function requireAuth() {
    const token = getToken();
    if (!token) { window.location.href = 'login.html'; return null; }
    return token;
}
