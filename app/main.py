from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import profile, product, pedido, auth

app = FastAPI(
    title="P3 E-commerce - Renta de Películas",
    description="API REST para renta de películas con OAuth 2 (GitHub via Supabase)",
    version="2.0.0"
)

# ── CORS ─────────────────────────────────────────────────────────────────────
# Necesario para que el frontend (React/Next/Vue) pueda llamar la API.
# En producción reemplaza "*" con el dominio real del frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # TODO: cambiar a ["https://tu-frontend.com"] en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router,    prefix="/auth",    tags=["Auth"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(product.router, prefix="/product", tags=["Product"])
app.include_router(pedido.router,  prefix="/pedido",  tags=["Pedido"])


@app.get("/", tags=["Root"])
def root():
    return {"mensaje": "Bienvenido a P3 E-commerce"}