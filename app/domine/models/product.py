from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4   

class Product(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    price: float
    stock: int
    category_id: UUID = Field(foreign_key='category.id')

    category: Optional['Category'] = Relationship(back_populates='products')
    order_items: List['OrderItem'] = Relationship(back_populates='product')