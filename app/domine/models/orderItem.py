from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4

class OrderItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key='order.id')
    product_id: UUID = Field(foreign_key='product.id')

    quantity: int
    unit_price: float
    subtotal: float

    order: Optional['Order'] = Relationship(back_populates='order_items')
    product: Optional['Product'] = Relationship(back_populates='order_items')