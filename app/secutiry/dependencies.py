from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from app.presentation.schemas.auth_schema import TokenData
from helpers.auth import verify_acces_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    token = credentials.credentials
    return verify_acces_token(token)


def admin_required(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    if current_user.role != 'ADMIN':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No tienes permiso de administrador')
    
    return current_user


def employee_required(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    if current_user.role != 'EMPLOYEE':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Solo empleados')
    
    return current_user
