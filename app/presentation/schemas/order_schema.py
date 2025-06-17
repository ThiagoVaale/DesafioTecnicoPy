from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from app.presentation.schemas.orderItem_schema import OrderItemReponse, OrderItemCreate
from app.domine.enums.statusOrder_enum import StatusOrderEnum



class OrderResponse(BaseModel):
    id: UUID
    client_id: UUID
    employee_id: Optional[UUID]
    total_amount: float
    status: StatusOrderEnum
    shipping_address: str
    payment_method: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemReponse]

    model_config = {
        'from_attributes': True
    }


class CreateOrder(BaseModel):
    client_id: UUID
    employee_id: Optional[UUID]
    shipping_address: str
    payment_method: str
    createdAt: datetime
    items: List[OrderItemCreate]


class UpdateOrder(BaseModel):
    shipping_address: Optional[str]
    payment_method: Optional[str] 
    status: Optional[StatusOrderEnum]

