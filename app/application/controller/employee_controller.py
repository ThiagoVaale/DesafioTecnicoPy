from app.persistence.repositories.employee_repository import EmployeeRepository
from app.application.service.employee_service import EmployeeService
from app.presentation.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeesOrdersResponse, EmployeeUpdate
from typing import List
class EmployeeController:
    def __init__(self, repository: EmployeeRepository):
        self.service = EmployeeService(repository)

    def create_employee(self, employee_create: EmployeeCreate) -> EmployeeResponse:
        return self.service.create_employee(employee_create)
    
    def get_employee_with_order(self, username_employee: str) -> EmployeesOrdersResponse:
        return self.service.get_employee_with_order(username_employee)
    
    def get_employees_with_order(self) -> List[EmployeesOrdersResponse]:
        return self.service.get_employees_with_order()
    
    def update_employee(self, update_employee: EmployeeUpdate) -> EmployeeResponse:
        return self.service.update_employee(update_employee)
    
    def update_employee_admin(self, username_employee: str, new_salary: float) -> EmployeeResponse:
        return self.service.update_employee_admin(username_employee, new_salary)
    
    def delete_employee(self, username_employee: str) -> EmployeeResponse:
        return self.service.delete_employee(username_employee)