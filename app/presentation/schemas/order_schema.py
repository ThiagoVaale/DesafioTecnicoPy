from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class OrderResponse(BaseModel):
    id: UUID
    total_amount: float
    status: str
    shipping_addres: str
    payment_method: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True