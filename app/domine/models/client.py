from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4

class Client(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True)
    password: str
    email: str = Field(unique=True)
    address: str
    phone: str
    is_active: bool = Field(default=True)
    role_id: UUID = Field(foreign_key='role.id')

    orders: List['Order'] = Relationship(back_populates='client')
    role: Optional['Role'] = Relationship(back_populates='clients')