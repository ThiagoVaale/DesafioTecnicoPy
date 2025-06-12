from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    stock: int
    category_id: int = Field(foreign_key='category.id')

    category: Optional['Category'] = Relationship(back_populates='products')