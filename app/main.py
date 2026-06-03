from fastapi import FastAPI
# from fastapi import FastAPI trae el framework FastAPI

from app.routers import profile, product, pedido

# from app.routers import profile, product, pedido importa los 3 archivos de endpoints

app = FastAPI(
    title="P3 E-commerce - Renta de Películas",
    description="API REST para renta de películas",
    version="1.0.0"
)

# app = FastAPI(...) crea la aplicación con nombre y descripción (lo que aparece en Swagger)

# prefix="/profile" es la URL base, por eso todos los endpoints de profile empiezan con /profile/

# app.include_router(...) dice a la app que use los endpoints de cada archivo

app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(product.router, prefix="/product", tags=["Product"])
app.include_router(pedido.router, prefix="/pedido", tags=["Pedido"])

# tags cajas de colores en Swagger para agrupar endpoints

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a P3 E-commerce"}

# @app.get("/") endpoint de bienvenida a 127.0.0.1:8000

from app.routers import profile, product, pedido, auth

app.include_router(auth.router, prefix="/auth", tags=["Auth"])









