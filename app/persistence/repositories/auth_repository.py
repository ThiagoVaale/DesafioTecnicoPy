from sqlmodel import Session, select
from typing import Optional, Union
from app.domine.models.employee import Employee
from app.domine.models.client import Client
from uuid import UUID

class AuthRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_username(self, username: str) -> Optional[Union[Employee, Client]]:
        employee = self.session.exec(select(Employee).where(Employee.username == username, Employee.is_active == True)).first()
        if employee:
            return employee
        
        client = self.session.exec(select(Client).where(Client.username == username, Client.is_active == True)).first()
 
        if client:
            return client
        
        return None
    
    def get_user_by_id(self, user_id: UUID) -> Optional[Union[Employee, Client]]:
        employee = self.session.get(Employee, user_id)
        if employee and employee.is_active:
            return employee
        
        client = self.session.get(Client, user_id)

        if client and client.is_active:
            return client
        
        return None