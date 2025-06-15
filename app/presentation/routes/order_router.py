from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.application.controller.order_controller import OrderController
from app.persistence.config.session import get_session
from app.presentation.schemas.order_schema import OrderResponse, CreateOrder, UpdateOrder
from uuid import UUID
from typing import List
from app.persistence.repositories.product_repository import ProductRepository
from app.persistence.repositories.employee_repository import EmployeeRepository
from app.persistence.repositories.client_repository import ClientRepository
from app.persistence.repositories.order_repository import OrderRepository



router = APIRouter(prefix='orders', tags=['orders'])

def get_controller(session: Session = Depends(get_session)) -> OrderController:
    order_repository = OrderRepository(session)
    client_repository = ClientRepository(session)
    product_repository = ProductRepository(session)
    employee_repository = EmployeeRepository(session)

    return OrderController(order_repository, client_repository, product_repository, employee_repository)


@router.post('/', response_model=OrderResponse, status_code=201)
def create_order(create_order: CreateOrder, controller: OrderController = Depends(get_controller)):
    return controller.create_order(create_order)

@router.get('/{order_id}', response_model=OrderResponse, status_code=200)
def get_order_wirth_id(
    order_id: UUID,
    controller: OrderController = Depends(get_controller)):
    return controller.get_order_with_id(order_id)

@router.get('/client/{client_id}', response_model=List[OrderResponse], status_code=200)
def get_order_employee(
    client_id: UUID,
    controller: OrderController = Depends(get_controller)):
    return controller.get_order_client(client_id)


@router.get('/employee/{employee_id}', response_model=OrderResponse, status_code=200)
def get_order_employee(
    employee_id: UUID,
    controller: OrderController = Depends(get_controller)):
    return controller.get_order_employee(employee_id)


@router.get('/', response_model=List[OrderResponse], status_code=200)
def get_all_order(controller: OrderController = Depends(get_controller)):
    return controller.get_all_order()

@router.put('/{order_id}', response_model=OrderResponse, status_code=200)
def update_order(
    update_order: UpdateOrder,
    order_id: UUID,
    controller: OrderController = Depends(get_controller)):
    return controller.update_order(order_id, update_order)

@router.delete('/{order_id}', response_model=OrderResponse, status_code=200)
def cancel_order(
    order_id: UUID = Query(default=None),
    controller: OrderController = Depends(get_controller)):
    return controller.cancel_order(order_id)