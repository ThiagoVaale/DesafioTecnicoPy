from pydantic import BaseModel
from uuid import UUID


class OrderItemReponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int
    unit_price: int
    subtotal: int

    class Config:
        orm_mode = True
    

class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: int


    