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
from app.presentation.schemas.orderItem_schema import OrderItemReponse



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
            raise HTTPException(status_code=409, detail=f'Customer {client.username} has a disabled account or was not found. They cannot purchase.')

        if not employee or not employee.is_active:
            raise HTTPException(status_code=409, detail=f'Employee {employee.username} is not logged in or the login was invalid.')
        
        order_items = []
        total_amount = 0.0

        for item in create_order.items:
            product = self.product_repository.get_product_id(item.product_id)
            if not product or not product.is_active:
                raise HTTPException(status_code=409, detail=f'The product {product.name} is disabled')
            
            if product.stock == 0:
                raise HTTPException(status_code=404, detail=f'Out of stock for product: {product.name}, category: {product.category}')

            if product.stock < item.quantity:
                raise HTTPException(status_code=404, detail='There is not enough stock')
        
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
            total_amount=total_amount
        )

        created_order = self.order_repository.create_order(new_order, order_items)

        for each_item in create_order.items:
            self.product_repository.reduce_stock(each_item.product_id, each_item.quantity)

        return OrderResponse(
            id=created_order.id,
            client_id=created_order.client_id,
            employee=created_order.employee_id,
            total_amount=created_order.total_amount,
            status=created_order.status,
            shipping_address=created_order.shipping_address,
            payment_method=created_order.payment_method,
            created_at=created_order.created_at,
            updated_at=created_order.updated_at,
            items=[
                OrderItemReponse.model_validate(item)
                for item in created_order.order_items
            ]
        )

        
    def get_order_with_id(self, id_order: UUID) -> OrderResponse:
        order = self.order_repository.get_order_with_id(id_order)

        if not order:
            raise HTTPException(status_code=404, detail=f'The order id {id_order} was not found')
    
        return OrderResponse(
            id=order.id,
            client_id=order.client_id,
            employee=order.employee_id,
            total_amount=order.total_amount,
            status=order.status,
            shipping_address=order.shipping_address,
            payment_method=order.payment_method,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[
                OrderItemReponse.model_validate(item)
                for item in order.order_items
            ]
        )
    
    def get_order_client(self, id_client: UUID) -> List[OrderResponse]:
        orders = self.order_repository.get_order_client(id_client)

        if not orders:
            raise HTTPException(status_code=404, detail=f'There are no purchase orders with id {id_client}')
        
        order_response = []

        for order in orders:
            order_response.append(OrderResponse(
                id=order.id,
                client_id=order.client_id,
                employee_id=order.employee_id,
                total_amount=order.total_amount,
                status=order.status,
                shipping_address=order.shipping_address,
                payment_method=order.payment_method,
                created_at=order.created_at,
                updated_at=order.updated_at,
                items=[
                    OrderItemReponse.model_validate(item)
                    for item in order.order_items
            ]
        ))
        
        return order_response
    
    def get_order_employee(self, id_employee: UUID) -> List[OrderResponse]:
        orders = self.order_repository.get_order_employee(id_employee)

        if not orders:
            raise HTTPException(status_code=404, detail=f'There are no sales for the employee with id {id_employee}')
    
        order_response = []

        for order in orders:
            order_response.append(OrderResponse(
                id=order.id,
                client_id=order.client_id,
                employee_id=order.employee_id,
                total_amount=order.total_amount,
                status=order.status,
                shipping_address=order.shipping_address,
                payment_method=order.payment_method,
                created_at=order.created_at,
                updated_at=order.updated_at,
                items=[
                    OrderItemReponse.model_validate(item)
                    for item in order.order_items
            ]
        ))
        
        return order_response
    
    def get_all_order(self) -> List[OrderResponse]:
        orders = self.order_repository.get_all_order()

        if not orders:
            raise HTTPException(status_code=404, detail='There are no orders')
    
        order_responses = []

        for order in orders:
            order_responses.append(OrderResponse(
                id=order.id,
                client_id=order.client_id,
                employee=order.employee_id,
                total_amount=order.total_amount,
                status=order.status,
                shipping_address=order.shipping_address,
                payment_method=order.payment_method,
                created_at=order.created_at,
                updated_at=order.updated_at,
                items=[
                    OrderItemReponse.model_validate(item)
                    for item in order.order_items
            ]
        ))

        return order_responses
    
    def update_order(self, id_order: UUID, update_order: UpdateOrder) -> OrderResponse:
        order = self.order_repository.get_order_with_id(id_order)

        if not order:
            raise HTTPException(status_code=404, detail=f'There is no order with id {id_order}')
        
        order.shipping_address = update_order.shipping_address
        order.payment_method = update_order.payment_method
        order.status = update_order.status

        updated_order = self.order_repository.update_order(order)

        return OrderResponse(
            id=order.id,
            client_id=order.client_id,
            employee=order.employee_id,
            total_amount=order.total_amount,
            status=updated_order.status,
            shipping_address=updated_order.shipping_address,
            payment_method=updated_order.payment_method,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[
                OrderItemReponse.model_validate(item)
                for item in order.order_items
            ]
        )
    
    
    def cancel_order(self, id_orden: UUID) -> OrderResponse:
        order_exists = self.order_repository.get_order_with_id(id_orden)

        if not order_exists:
            raise HTTPException(status_code=404, detail=f'There is no order with id {id_orden}')
        
        cancel_order = self.order_repository.cancel_order(id_orden)

        return OrderResponse(
            id=order_exists.id,
            client_id=order_exists.client_id,
            employee=order_exists.employee_id,
            total_amount=order_exists.total_amount,
            status=cancel_order.status,
            shipping_address=order_exists.shipping_address,
            payment_method=order_exists.payment_method,
            created_at=order_exists.created_at,
            updated_at=order_exists.updated_at,
            items=[
                OrderItemReponse.model_validate(item)
                for item in order_exists.order_items
            ]
        )