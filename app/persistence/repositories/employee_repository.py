from sqlmodel import Session, select
from app.presentation.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeesOrdersResponse, EmployeeUpdate, EmployeeUpdateAdmin
from app.domine.models.employee import Employee
from typing import Optional, List
from app.domine.models.role import Role
from sqlalchemy.orm import selectinload
from uuid import UUID

class EmployeeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_employee(self, employee_create: EmployeeCreate, role_id: UUID) -> Employee:
        employee = Employee(**employee_create.model_dump(exclude={'role'}), role_id=role_id)
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)

        return employee
    
    def get_role_by_name(self, role_name: str) -> Optional[Role]:
        object_rol = select(Role).where(Role.name == role_name)
        return self.session.exec(object_rol).first()
    
    def get_employee(self, username_employee: str) -> Optional[Employee]:
        find_employee = select(Employee).where(Employee.username == username_employee)
        return self.session.exec(find_employee).first()


    def get_employee_id(self, id_employee: UUID) -> Optional[Employee]:
        return self.session.exec(select(Employee).where(Employee.id == id_employee)).first()
    

    def get_employee_with_order(self, username_employee: str) -> Optional[Employee]:
        each_employee = select(Employee).where(Employee.username == username_employee).options(selectinload(Employee.orders))
        get_employee = self.session.exec(each_employee).first()
        return get_employee
    
    def get_employees_with_order(self) -> List[EmployeesOrdersResponse]:
        each_employee_with_orders = select(Employee).options(selectinload(Employee.orders))
        get_employees_with_orders = self.session.exec(each_employee_with_orders).all()
        return get_employees_with_orders
    
    def update_employee(self, update_employee: Employee) -> Optional[Employee]:
        self.session.add(update_employee)
        self.session.commit()
        self.session.refresh(update_employee)

        return update_employee
    
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

