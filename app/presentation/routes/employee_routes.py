from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.persistence.config.session import get_session
from app.application.controller.employee_controller import EmployeeController
from app.persistence.repositories.employee_repository import EmployeeRepository
from app.presentation.schemas.employee_schema import EmployeeResponse, EmployeeCreate, EmployeesOrdersResponse, EmployeeUpdate
from typing import List

router = APIRouter(prefix='employees', tags=['employees'])

def get_controller(session: Session = Depends(get_session)) -> EmployeeController:
    repository = EmployeeRepository(session)
    return EmployeeController(repository)


@router.post('/', response_model=EmployeeResponse , status_code=201)
def create_employee(employee_create: EmployeeCreate, controller: EmployeeController = Depends(get_controller)):
    return controller.create_employee(employee_create)

@router.get('/orders/{username_employee}', response_model=EmployeesOrdersResponse, status_code=200)
def get_employee_with_order(username_employee: str, controller: EmployeeController = Depends(get_controller)):
    return controller.get_employee_with_order(username_employee)

@router.get('/orders', response_model=List[EmployeesOrdersResponse], status_code=200)
def get_employees_with_order(controller: EmployeeController = Depends(get_controller)):
    return controller.get_employees_with_order()

@router.put('/{username_employee}', response_model=EmployeeResponse, status_code=200)
def update_employee(username_employee: str, update_employee: EmployeeUpdate, controller: EmployeeController = Depends(get_controller)):
    return controller.update_employee(username_employee, update_employee)

@router.patch('/{username_employee}/salary', response_model=EmployeeResponse, status_code=200)
def update_employee_admin(username_employee: str, new_salary: float, controller: EmployeeController = Depends(get_controller)):
    return controller.update_employee_admin(username_employee, new_salary)


@router.delete('/{username_employee}', response_model=EmployeeResponse, status_code=200)
def delete_employee(username_employee: str, controller: EmployeeController = Depends(get_controller)):
    return controller.delete_employee(username_employee)