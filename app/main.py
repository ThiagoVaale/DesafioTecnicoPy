from fastapi import FastAPI
from app.application.controller import authorizatonController, loginController

app = FastAPI()

app.include_router(authorizatonController.router)
app.include_router(loginController.router)

@app.get('/')
async def root():
    return {'message' : 'API funcionando!'}