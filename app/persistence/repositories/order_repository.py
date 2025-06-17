from sqlmodel import Session, select
from app.domine.models.order import Order
from app.domine.models.orderItem import OrderItem
from typing import List
from uuid import UUID
from sqlalchemy.orm import selectinload
from app.domine.enums.statusOrder_enum import StatusOrderEnum


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_order(self, create_order: Order, order_items: List[OrderItem]) -> Order:
        self.session.add(create_order)
        self.session.flush()

        for order_item in order_items:
            order_item.order_id = create_order.id
            self.session.add(order_item)

        self.session.commit()
        return create_order 
    
    def get_order_with_id(self, id_order: UUID) -> Order:
        return self.session.exec(select(Order).where(Order.id == id_order).options(selectinload(Order.order_items))).first()

    def get_order_client(self, id_client: UUID) -> List[Order]:
        return self.session.exec(select(Order).where(Order.client_id == id_client).options(selectinload(Order.order_items), selectinload(Order.employee))).all()
    
    def get_order_employee(self, id_employee: UUID) -> List[Order]:
        return self.session.exec(select(Order).where(Order.employee_id == id_employee).options(selectinload(Order.order_items), selectinload(Order.client))).all()
    
    def get_all_order(self) -> List[Order]:
        return self.session.exec(select(Order).options(selectinload(Order.order_items))).all()
    
    def update_order(self, update_order: Order) -> Order:
        self.session.add(update_order)
        self.session.commit()
        self.session.refresh(update_order)

        return update_order
    
    def cancel_order(self, id_order: UUID) -> Order:
        order = self.get_order_with_id(id_order)

        order.status = StatusOrderEnum.CANCELED

        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)


        return order

        