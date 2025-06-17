from pydantic import BaseModel
from uuid import UUID
from app.presentation.schemas.product_schema import ProductResponse
from typing import List

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    is_active: bool

    model_config = {
        'from_attributes': True
    }

class ProductCategoryResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    stock: int
    is_active: bool

    model_config = {
        'from_attributes': True
    }


class CategoryUpdate(BaseModel):
    new_name: str