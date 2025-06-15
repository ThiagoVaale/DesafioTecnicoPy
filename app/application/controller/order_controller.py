from app.persistence.repositories.order_repository import OrderRepository
from app.application.service.order_service import OrderService
from app.presentation.schemas.order_schema import CreateOrder, OrderResponse, UpdateOrder
from uuid import UUID
from typing import List
from app.persistence.repositories.client_repository import ClientRepository
from app.persistence.repositories.product_repository import ProductRepository
from app.persistence.repositories.employee_repository import EmployeeRepository


class OrderController:
    def __init__(self, order_repository: OrderRepository, client_repository: ClientRepository, product_repository: ProductRepository, employee_repository: EmployeeRepository):
        self.service = OrderService(order_repository, client_repository, product_repository, employee_repository)

    def create_order(self, create_order: CreateOrder) -> OrderResponse:
        return self.service.create_order(create_order)
    
    def get_order_with_id(self, id_order: UUID) -> OrderResponse:
        return self.service.get_order_with_id(id_order)
    
    def get_order_client(self, id_client: UUID) -> List[OrderResponse]:
        return self.service.get_order_client(id_client)
    
    def get_order_employee(self, id_employee: UUID) -> OrderResponse:
        return self.service.get_order_employee(id_employee)
    
    def get_all_order(self) -> List[OrderResponse]:
        return self.service.get_all_order()
    
    def update_order(self, id_order: UUID, update_order: UpdateOrder) -> OrderResponse:
        return self.service.update_order(id_order, update_order)
    
    def cancel_order(self, id_order: UUID) -> OrderResponse:
        return self.service.delete_order(id_order)