from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from uuid import UUID, uuid4
from app.domine.enums.role_enum import RoleEnum

class Role(SQLModel, table=True):
    id: int = Field(default_factory=uuid4, primary_key=True)
    name: RoleEnum = Field(unique=True)

    clients: List['Client'] = Relationship(back_populates='role')
    employees: List['Employee'] = Relationship(back_populates='role')