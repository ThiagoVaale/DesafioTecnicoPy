from fastapi import FastAPI
from app.presentation.routes.client_routes import router as client_routes
from app.presentation.routes.product_routes import router as product_routes
from app.presentation.routes.category_routes import router as category_routes
from app.presentation.routes.employee_routes import router as employee_routes
from app.presentation.routes.order_router import router as order_router
from app.presentation.routes.auth_router import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(client_routes)
app.include_router(product_routes)
app.include_router(category_routes)
app.include_router(employee_routes)
app.include_router(order_router)

@app.get('/')
async def root():
    return {'message' : 'API funcionando!'}


@app.get("/healthcheck", tags=["Health"])
async def healthcheck():
    return {"status": "ok"}

API_VERSION = "1.0.0"

@app.get("/version", tags=["Info"])
async def get_version():
    return {"version": API_VERSION}