from pydantic import BaseModel
from uuid import UUID

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    stock: int
    is_active: bool

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    is_active: bool