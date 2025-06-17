from app.persistence.repositories.employee_repository import EmployeeRepository
from app.presentation.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeesOrdersResponse, EmployeeUpdate
from app.domine.models.employee import Employee
from typing import Optional, List
from fastapi import HTTPException
from datetime import datetime 
from app.domine.enums.role_enum import RoleEnum
from app.presentation.schemas.employee_schema import OrderResponse
from app.presentation.schemas.orderItem_schema import OrderItemReponse
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class EmployeeService: 
    def __init__(self, reposiory: EmployeeRepository):
        self.repository = reposiory

    def create_employee(self, employee_create: EmployeeCreate) -> EmployeeResponse:
        employee_exists = self.repository.get_employee(employee_create.username)
        hashed_password = pwd_context.hash(employee_create.password)

        if employee_exists:
            raise HTTPException(status_code=400, detail=f'The employee {employee_exists.username} already exists')
        
        role = self.repository.get_role_by_name(employee_create.role)

        if not role:
            raise HTTPException(status_code=404, detail=f'The role {employee_create.role.value} does not exist')
        
        employee = Employee(
            username=employee_create.username,
            password=hashed_password,
            email=employee_create.email,
            salary=employee_create.salary,
            role_id=role.id
        )
        employee.role = role

        employee_created = self.repository.create_employee(employee)    
        return EmployeeResponse(
            id=employee_created.id,
            username=employee_created.username,
            email=employee_created.email,
            hire_date=employee_created.hire_date,
            role=employee_create.role,
            is_active=employee_created.is_active
        )


    def get_employee_with_order(self, username_employee: str) -> EmployeesOrdersResponse:
        employee = self.repository.get_employee_with_order(username_employee)

        if not employee:
            raise HTTPException(status_code=404, detail=f'The employee named {username_employee} does not exist')
        
        employee_orders = []

        for order in employee.orders:
            order_response = OrderResponse(
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
               )
            employee_orders.append(order_response)

        dto = EmployeesOrdersResponse(
            id=employee.id,
            username=employee.username,
            email=employee.email,
            hire_date=employee.hire_date,
            salary=employee.salary,
            is_active=employee.is_active,
            orders=employee_orders
        )

        employee_orders.append(dto)

        return dto

        
    def get_employees_with_order(self) -> List[EmployeesOrdersResponse]:
        employees = self.repository.get_employees_with_order()

        if not employees:
            raise HTTPException(status_code=404, detail='There are no employees')
        
        list_employees = []

        for employee in employees:
           orders = []

           for order in employee.orders:
               order_response = OrderResponse(
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
               orders.append(order_response)

           dto = EmployeesOrdersResponse(
               id=employee.id,
               username=employee.username,
               email=employee.email,
               hire_date=employee.hire_date,
               salary=employee.salary,
               is_active=employee.is_active,
               orders=orders
           )

           list_employees.append(dto)

        return list_employees

    def update_employee(self, username_employee: str, update_employee: EmployeeUpdate) -> EmployeeResponse:
        employee = self.repository.get_employee(username_employee)

        if not employee:
            raise HTTPException(status_code=400, detail=f'The user {username_employee} does not exist')
        
        employee.username = update_employee.username
        employee.password = update_employee.password
        employee.email = update_employee.email


        updated_employee = self.repository.update_employee(employee)

        role = self.repository.get_role_by_id(updated_employee.role_id)

        return EmployeeResponse(
            id=updated_employee.id,
            username=updated_employee.username,
            email=updated_employee.email,
            hire_date=updated_employee.hire_date,
            role=role.name,
            is_active=updated_employee.is_active
        )
    

    def update_employee_admin(self, username_employee: str, new_salary: float) -> EmployeeResponse:
        employee_exists = self.repository.get_employee(username_employee)

        if not employee_exists:
            raise HTTPException(status_code=400, detail=f'The user {username_employee} does not exist')
    
        updated_salary_employee = self.repository.update_employee_admin(username_employee, new_salary)
        role = self.repository.get_role_by_id(updated_salary_employee.role_id)

        return EmployeeResponse(
            id=updated_salary_employee.id,
            username=updated_salary_employee.username,
            email=updated_salary_employee.email,
            hire_date=updated_salary_employee.hire_date,
            role=role.name,
            is_active=updated_salary_employee.is_active
        )
         

    def delete_employee(self, username: str) -> EmployeeResponse:
        employee = self.repository.get_employee(username)

        if not employee:
            raise HTTPException(status_code=400, detail=F'The user {employee.username} does not exist. It could not be deleted.')
        
        if employee.is_active == False:
            raise HTTPException(status_code=409, detail=f'The user {employee.username} has already been deleted.')
        
        deleted_employee = self.repository.delete_employee(employee)
        
        role = self.repository.get_role_by_id(deleted_employee.role_id)

        return EmployeeResponse(
            id=deleted_employee.id,
            username=deleted_employee.username,
            email=deleted_employee.email,
            hire_date=deleted_employee.hire_date,
            role=role.name,
            is_active=deleted_employee.is_active
        )
