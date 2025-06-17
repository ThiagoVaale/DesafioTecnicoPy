from pydantic import BaseModel, EmailStr
from uuid import UUID

class AuthLoginRequest(BaseModel):
    username: str
    password: str

class AuthLoginReponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenData(BaseModel):
    username: str
    role: str

class AuthUser(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: str