from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
from uuid import UUID, uuid4   
from app.domine.enums.statusOrder_enum import StatusOrderEnum

class Order(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    status: StatusOrderEnum = Field(default=StatusOrderEnum.PENDING)
    shipping_address: str
    payment_method: str 
    total_amount: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    client_id: UUID = Field(foreign_key='client.id')
    employee_id: UUID = Field(foreign_key='employee.id')

    client: Optional['Client'] = Relationship(back_populates='orders')
    order_items: List['OrderItem'] = Relationship(back_populates='order')
    employee: Optional['Employee'] = Relationship(back_populates='orders')
