from pydantic import BaseModel
from uuid import UUID
from app.presentation.schemas.product_schema import ProductResponse
from typing import List

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True

class ProductCategoryResponse(BaseModel):
    id: UUID
    name: str
    products: List[ProductResponse]

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    new_name: str