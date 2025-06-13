from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class ClientCreate(BaseModel):
    username: str = Field(min_length=5, max_length=25)
    password: str
    email: EmailStr
    address: str
    phone: str

class ClientResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    address: str
    phone: str

    class Config:
        orm_mode = True

class ClientUpdate(BaseModel):
    username: str
    email: EmailStr
    address: str
    phone: str



