from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4

class Client(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    password: str
    email: str
    address: str
    phone: str
    is_active: bool
    role_id: UUID = Field(foreign_key='role.id')

    orders: List['Order'] = Relationship(back_populates='client')
    role: Optional['Role'] = Relationship(back_populates='clients')