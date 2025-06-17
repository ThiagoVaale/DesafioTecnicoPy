from typing import Optional
from datetime import timedelta, timezone, datetime
from jose import jwt, JWTError
from app.presentation.schemas.auth_schema import TokenData
from fastapi import HTTPException, status


SECRET_KEY = "snfjskhcscklsnclsnj49490749841dvcvcw221dda"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minute=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({ 'exp' : expire })
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def verify_acces_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        username: str = payload.get('sub')
        role: str = payload.get('role')

        if username is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
        
        return TokenData(username=username, role=role)
    
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='It has no permission')