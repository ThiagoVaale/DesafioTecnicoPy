from sqlmodel import Session, select
from app.presentation.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeesOrdersResponse
from app.domine.models.employee import Employee
from typing import Optional, List
from app.domine.models.role import Role
from sqlalchemy.orm import selectinload
from uuid import UUID
from app.domine.enums.role_enum import RoleEnum
from app.domine.models.order import Order

class EmployeeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_employee(self, employee_create: Employee) -> Employee:
        self.session.add(employee_create)
        self.session.commit()
        self.session.refresh(employee_create)

        stmt = (select(Employee).where(Employee.id == employee_create.id).options(selectinload(Employee.role)))
        return self.session.exec(stmt).first()
    
    def get_role_by_name(self, role_name: RoleEnum) -> Optional[Role]:
        return self.session.exec(select(Role).where(Role.name == role_name)).first()
    

    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        return self.session.exec(select(Role).where(Role.id == role_id)).first()
    
    
    def get_employee(self, username_employee: str) -> Optional[Employee]:
        return self.session.exec(select(Employee).where(Employee.username == username_employee).options(selectinload(Employee.role))).first()

    def get_employee_id(self, id_employee: UUID) -> Optional[Employee]:
        return self.session.exec(select(Employee).where(Employee.id == id_employee)).first()
    
    def get_employee_with_order(self, username_employee: str) -> Optional[Employee]:
        employee_with_orders = select(Employee).where(Employee.username == username_employee).options(selectinload(Employee.orders).selectinload(Order.order_items))
        result = self.session.exec(employee_with_orders).first()
        return result
        
    def get_employees_with_order(self) -> List[EmployeesOrdersResponse]:
        each_employee_with_orders = select(Employee).where(Employee.is_active == True).options(selectinload(Employee.orders))
        get_employees_with_orders = self.session.exec(each_employee_with_orders).all()
        return get_employees_with_orders
    
    def update_employee(self, update_employee: Employee) -> Optional[Employee]:
        self.session.add(update_employee)
        self.session.commit()
        
        stmt = (
        select(Employee)
        .where(Employee.id == update_employee.id)
        .options(selectinload(Employee.role))
        )

        return self.session.exec(stmt).first()
    
    def update_employee_admin(self, username_employee: str, new_salary: float ) -> Optional[Employee]:
        employee = select(Employee).where(Employee.username == username_employee)
        object_employee = self.session.exec(employee).first()

        object_employee.salary = new_salary

        self.session.add(object_employee)
        self.session.commit()
        self.session.refresh(object_employee)

        return object_employee

    def delete_employee(self, delete_employee: Employee) -> Employee:
        delete_employee.is_active = False
        self.session.add(delete_employee)
        self.session.commit()
        self.session.refresh(delete_employee)

        return delete_employee

