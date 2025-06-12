from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str
    address: str
    phone: str
    role_id: int = Field(foreign_key='role.id')

    orders: List['Order'] = Relationship(back_populates='client')