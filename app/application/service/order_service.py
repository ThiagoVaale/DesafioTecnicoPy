from app.persistence.repositories.order_repository import OrderRepository
from typing import List
from app.presentation.schemas.order_schema import CreateOrder
from app.domine.models.orderItem import OrderItem
from app.presentation.schemas.order_schema import OrderResponse, UpdateOrder
from uuid import UUID
from app.persistence.repositories.client_repository import ClientRepository
from app.persistence.repositories.product_repository import ProductRepository
from app.persistence.repositories.employee_repository import EmployeeRepository
from fastapi import HTTPException
from app.domine.models.order import Order
from app.domine.enums.statusOrder_enum import StatusOrderEnum

class OrderService:
    def __init__(self, order_repository: OrderRepository, client_repository: ClientRepository, product_repository: ProductRepository,  employee_repository: EmployeeRepository):
        self.order_repository = order_repository
        self.client_repository = client_repository
        self.product_repository = product_repository
        self.employee_repository = employee_repository

    def create_order(self, create_order: CreateOrder) -> OrderResponse:
        client = self.client_repository.get_client_with_id(create_order.client_id)
        employee = self.employee_repository.get_employee_id(create_order.employee_id)

        if not client or not client.is_active:
            raise HTTPException(status_code=409, detail=f'El cliente {client.username} tiene la cuenta deshabilitada o no fue encontrado. No puede comprar')

        if not employee or not employee.is_active:
            raise HTTPException(status_code=409, detail=f'La empleada {employee.username} no esta habilitada o el ingreso fue invalido.')
        
        order_items = []
        total_amount = 0.0

        for item in create_order.items:
            product = self.product_repository.get_product_id(create_order.product_id)
            if not product or not product.is_active:
                raise HTTPException(status_code=409, detail=f'El producto {product.name} esta deshabilitado')
            
            if product.stock == 0:
                raise HTTPException(status_code=404, detail=f'Sin existencias del producto: {product.name}, categoria: {product.category}')

            if product.stock < item.quantity:
                raise HTTPException(status_code=404, detail=f'No hay stock suficiente')
        
            subtotal = item.quantity * item.unit_price
            total_amount += subtotal

            order_items.append(OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=subtotal,
            ))

        new_order = Order(
            client_id=client.id,
            employee_id=employee.id,
            status = StatusOrderEnum.PENDING,
            shipping_address=create_order.shipping_address,
            payment_method=create_order.payment_method,
            client_id=client.id,
            employee_id=employee.id,
            total_amount=total_amount
        )

        created_order = self.order_repository.create_order(new_order, order_items)

        for each_item in create_order.items:
            self.product_repository.reduce_stock(each_item.product_id, each_item.quantity)

        return OrderResponse.model_validate(created_order)

        
    def get_order_with_id(self, id_order: UUID) -> OrderResponse:
        order = self.order_repository.get_order_with_id(id_order)

        if not order:
            raise HTTPException(status_code=404, detail=f'El id de orden {id_order} no se encontro')
    
        return OrderResponse.model_validate(order)
    
    def get_order_client(self, id_client: UUID) -> List[OrderResponse]:
        orders = self.order_repository.get_order_client(id_client)

        if not orders:
            raise HTTPException(status_code=404, detail=f'No existen ordenes de compra con id {id_client}')
        
        list_order_item = []

        for order in orders:
            order_orm = OrderResponse.model_validate(order)
            list_order_item.append(order_orm)

        return list_order_item
    
    def get_order_employee(self, id_employee: UUID) -> List[OrderResponse]:
        orders = self.order_repository.get_order_employee(id_employee)

        if not orders:
            raise HTTPException(status_code=404, detail=f'No existen ventas de la empleada con id {id_employee}')
    
        list_order_item = []

        for order in orders:
            order_orm = OrderResponse.model_validate(order)
            list_order_item.append(order_orm)

        return list_order_item
    
    def get_all_order(self) -> List[OrderResponse]:
        orders = self.order_repository.get_all_order()

        if not orders:
            raise HTTPException(status_code=404, detail=f'No existen ordenes')
    
        list_order_item = []

        for order in orders:
            order_orm = OrderResponse.model_validate(order)
            list_order_item.append(order_orm)

        return list_order_item
    
    def update_order(self, id_order: UUID, update_order: UpdateOrder) -> OrderResponse:
        order = self.order_repository.get_order_with_id(id_order)

        if not order:
            raise HTTPException(status_code=404, detail=f'No existe una orden con id {id_order}')
        
        order.shipping_address = update_order.shipping_address
        order.payment_method = update_order.payment_method
        order.status = update_order.status

        updated_order = self.order_repository.update_order(order)

        return OrderResponse.model_validate(updated_order)
    
    
    def cancel_order(self, id_orden: UUID) -> OrderResponse:
        order_exists = self.order_repository.get_order_with_id(id_orden)

        if not order_exists:
            raise HTTPException(status_code=404, detail=f'No existe una orden con id {id_orden}')
        
        cancel_order = self.order_repository.delete_order(id_orden)

        return OrderResponse.model_validate(cancel_order)