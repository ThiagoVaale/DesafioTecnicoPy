from fastapi import APIRouter

router = APIRouter()

@router.post('/authorization')
async def authorization():
    return 'Hola, estas autotizado!'