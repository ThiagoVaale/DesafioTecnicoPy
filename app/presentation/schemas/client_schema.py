from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class ClientCreate(BaseModel):
    username: str = Field(min_length=5, max_length=25)
    password: str
    email: EmailStr
    address: str
    phone: str
    role_id: int

class ClientResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    address: str
    phone: str
    role_id: int
    is_active: bool

    model_config = {
        'from_attributes': True
    }
        

class ClientUpdate(BaseModel):
    username: str
    password: str
    email: EmailStr
    address: str
    phone: str



