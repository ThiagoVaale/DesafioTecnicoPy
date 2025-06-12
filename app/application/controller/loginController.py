from fastapi import APIRouter

router = APIRouter()

@router.get('/login')
async def authenticate():
    return 'Estas autenticado!'