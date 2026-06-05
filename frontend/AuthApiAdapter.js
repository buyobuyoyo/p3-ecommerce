export class AuthApiAdapter {
    constructor(baseUrl) { this.baseUrl = baseUrl; }

    getLoginUrl() {
        return `${this.baseUrl}/auth/login/github`;
    }

    async register(token) {
        const res = await fetch(`${this.baseUrl}/auth/register`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Error al registrar perfil");
        return await res.json();
    }

    async getMe(token) {
        const res = await fetch(`${this.baseUrl}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Token inválido");
        return await res.json();
    }

    async logout(token) {
        await fetch(`${this.baseUrl}/auth/logout`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        localStorage.removeItem('token');
        window.location.href = 'login.html';
    }
}
