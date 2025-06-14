from app.persistence.repositories.employee_repository import EmployeeRepository
from app.presentation.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeesOrdersResponse, EmployeeUpdate
from app.domine.models.employee import Employee
from typing import Optional, List
from fastapi import HTTPException

class EmployeeService: 
    def __init__(self, reposiory: EmployeeRepository):
        self.repository = reposiory

    def create_employee(self, employee_create: EmployeeCreate) -> EmployeeResponse:
        object_rol = self.repository.get_role_by_name(employee_create.role)

        employee = Employee(
            username=employee_create.username,
            password=employee_create.password,
            email=employee_create.email,
            salary=employee_create.salary,
            role_id=object_rol.id
        )

        created_employee = self.repository.create_employee(employee)
        return EmployeeResponse.model_validate(created_employee)
    
    def get_employee_with_order(self, username_employee: str) -> EmployeesOrdersResponse:
        employee = self.repository.get_employee_with_order(username_employee)

        if not employee:
            raise HTTPException(status_code=404, detail=f'El empleado con nombre {username_employee} no existe')
        
        return EmployeesOrdersResponse.model_validate(employee)
    
    def get_employees_with_order(self) -> List[EmployeesOrdersResponse]:
        employees = self.repository.get_employees_with_order()

        if not employees:
            raise HTTPException(status_code=404, detail=f'No existen empleados')
        

        list_employees = []

        for employee in employees:
            dto_employee = EmployeesOrdersResponse.model_validate(employee)
            list_employees.append(dto_employee)

        return list_employees

    def update_employee(self, username_employee: str, update_employee: EmployeeUpdate) -> EmployeeResponse:
        employee = self.repository.get_employee(username_employee)

        if not employee:
            raise HTTPException(status_code=400, detail=f'El usuario {username_employee} ya existe')
        
        employee.username = update_employee.username
        employee.password = update_employee.password
        employee.email = update_employee.email


        updated_employee = self.repository.update_employee(employee)
        return EmployeeResponse.model_validate(updated_employee)
    

    def update_employee_admin(self, username_employee: str, new_salary: float) -> EmployeeResponse:
        employee_exists = self.repository.get_employee(username_employee)

        if not employee_exists:
            raise HTTPException(status_code=400, detail=f'El usuario {username_employee} no existe')
    
        updated_salary_employee = self.repository.update_employee_admin(username_employee, new_salary)
        return EmployeeResponse.model_validate(updated_salary_employee)
         

    def delete_employee(self, username: str) -> EmployeeResponse:
        employee = self.repository.get_employee(username)

        if not employee:
            raise HTTPException(status_code=400, detail=F'El usuario {employee.username} no existe. No se pudo eliminar')
        
        if employee.is_active == False:
            raise HTTPException(status_code=409, detail=f'El usuario {employee.username} ya esta eliminado')
        
        deleted_employee = self.repository.delete_employee(employee)
        return EmployeeResponse.model_validate(deleted_employee)