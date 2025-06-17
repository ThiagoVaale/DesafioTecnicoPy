from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from app.domine.enums.role_enum import RoleEnum
from app.presentation.schemas.order_schema import OrderResponse
from typing import List

class EmployeeCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    salary: float
    role: RoleEnum

class EmployeeResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    hire_date: datetime
    role: RoleEnum
    is_active: bool

    model_config = {
        'from_attributes': True
    }

class EmployeesOrdersResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    hire_date: datetime
    salary: float
    is_active: bool
    orders: List[OrderResponse]

    model_config = {
        'from_attributes': True
    }


class EmployeeUpdate(BaseModel):
    username: str
    password: str
    email: EmailStr
    


