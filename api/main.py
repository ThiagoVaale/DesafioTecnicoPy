from fastapi import FastAPI

app = FastAPI()

@app.get('/saludo/dethiago')
async def root():
    return 'Hola Thiago'