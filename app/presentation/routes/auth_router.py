from fastapi import APIRouter, Depends, HTTPException
from app.presentation.schemas.auth_schema import AuthLoginReponse, AuthLoginRequest
from app.application.controller.auth_controller import AuthControler
from app.dependencies.auth_dependencies import get_auth_controller

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login', response_model=AuthLoginReponse)
def login(auth_data: AuthLoginRequest, controller: AuthControler = Depends(get_auth_controller)):
    return controller.login(auth_data)