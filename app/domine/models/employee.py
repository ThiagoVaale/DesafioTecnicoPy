from sqlmodel import SQLModel, Field, Relationship
from typing  import Optional, List
from datetime import datetime, timezone
from uuid import UUID, uuid4

class Employee(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    password: str
    email: str
    hire_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    salary: float
    role_id: UUID = Field(foreign_key='role.id')

    role: Optional['Role'] = Relationship(back_populates='employees')
    orders: List['Order'] = Relationship(back_populates='employee')