from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: UUID


class ProductCategory(BaseModel):
    id: UUID
    name: str

    model_config = {
        'from_attributes': True
    }

class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    stock: int
    is_active: bool
    category: Optional[ProductCategory]

    model_config = {
        'from_attributes': True
    }

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    is_active: bool