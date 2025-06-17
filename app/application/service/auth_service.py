from app.persistence.repositories.auth_repository import AuthRepository
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.presentation.schemas.auth_schema import AuthLoginReponse, AuthLoginRequest
from helpers.auth import create_access_token

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def authenticate_user(self, login_request: AuthLoginRequest) -> AuthLoginReponse:
        user = self.repository.get_user_by_username(login_request.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El usuario está inhabilitado")

        if not self.pwd_context.verify(login_request.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

        token_data = {
            "sub": user.username,
            "role": user.role.name
        }
        access_token = create_access_token(token_data, timedelta(minutes=60))

        return AuthLoginReponse(access_token=access_token)
