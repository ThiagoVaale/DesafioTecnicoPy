from pydantic import BaseModel
from uuid import UUID

class ClientCreate(BaseModel):
    username: str
    password: str
    email: str
    address: str
    phone: str

class ClientResponse(BaseModel):
    id: UUID
    username: str
    email: str
    address: str
    phone: str


class ClientUpdate(BaseModel):
    username: str
    email: str
    address: str
    phone: str


