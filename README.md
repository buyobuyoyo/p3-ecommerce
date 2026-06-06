# 🎬 Buyos Movie Lair — P3 E-commerce

API REST para renta de películas con autenticación OAuth 2 (GitHub via Supabase).  
**Stack:** FastAPI · Supabase · HTML/CSS/JS Vanilla

---

## Requisitos previos

Antes de empezar, asegúrate de tener instalado:

- **Python 3.11+** → https://www.python.org/downloads/
- **Git** → https://git-scm.com/
- Un servidor de archivos estáticos para el frontend (se recomienda [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) en VS Code o cualquier alternativa)

---

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPO>
cd <nombre-de-la-carpeta>
```

---

## 2. Crear y activar el entorno virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

> Sabrás que está activo porque el prompt cambia a `(.venv)`.

---

## 3. Instalar dependencias del backend

Desde la raíz del proyecto, crea un archivo `requirements.txt` con el siguiente contenido:

```
fastapi
uvicorn[standard]
supabase==2.3.0
gotrue==1.3.0
```

Si el archivo `ya existe` omite este paso.

Luego instala:

```bash
pip install -r requirements.txt
```

---

## 4. Levantar el servidor backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

El servidor queda corriendo en: **http://localhost:8000**

Para explorar y probar todos los endpoints de la API, abre en tu navegador:

```
http://localhost:8000/docs
```

---

## 5. Levantar el frontend

El frontend es HTML/JS puro y necesita ser servido desde un servidor local (no se puede abrir directamente como archivo con `file://` porque usa módulos ES y fetch).

**Python:**
```bash
cd frontend
python -m http.server 3000
```

Luego abre: **http://localhost:3000**

> ⚠️ El frontend **debe** correr en el puerto `3000` porque el backend redirige el callback de OAuth a `http://localhost:3000/login.html`.

---

## 6. Flujo de autenticación (GitHub OAuth)

1. Abre **http://localhost:3000/login.html**
2. Haz clic en **"Entrar con GitHub"**.
3. Autoriza la app en GitHub.
4. Serás redirigido de vuelta al frontend con el token en la URL.
5. El sistema guarda el token automáticamente y te lleva al catálogo.

---

## Estructura del proyecto

```
├── backend/
│   └── app/
│       ├── main.py            # Punto de entrada FastAPI
│       ├── database.py        # Conexión a Supabase
│       ├── dependencies.py    # Middleware de autenticación
│       ├── routers/           # Endpoints (auth, product, pedido, chat, profile)
│       ├── application/       # Casos de uso (chat service)
│       ├── domain/            # Entidades y puertos
│       ├── infrastructure/    # Repositorios Supabase
│       └── realtime/          # WebSocket manager
└── frontend/
    ├── index.html             # Catálogo principal
    ├── login.html             # Login con GitHub
    ├── checkout.html          # Proceso de compra
    ├── historial.html         # Historial de pedidos
    ├── chat.html              # Chat con soporte
    ├── admin.html             # Panel de administración
    └── infraestructure/       # Adaptadores JS (Auth, Product, Pedido, Chat)
```

---

## Dependencias del backend (detalle)

| Paquete | Versión | Para qué sirve |
|---|---|---|
| `fastapi` | latest | Framework principal de la API REST |
| `uvicorn[standard]` | latest | Servidor ASGI para correr FastAPI |
| `supabase` | 2.3.0 | Cliente para conectarse a la base de datos y autenticación |
| `gotrue` | 1.3.0 | Manejo de tokens y sesiones OAuth (requerido por supabase-py) |

---

## Notas

- La base de datos ya está configurada en Supabase y lista para usar; no necesitas crear tablas ni configurar nada adicional.
- Si quieres probar endpoints protegidos desde `/docs`, haz login, copia el token de la URL y pégalo en el candado 🔒 de Swagger UI.
- El chat en tiempo real usa WebSockets; asegúrate de no tener bloqueados los puertos locales.
