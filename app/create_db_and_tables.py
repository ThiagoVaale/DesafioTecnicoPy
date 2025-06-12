from sqlmodel import SQLModel
from app.db.session import engine
from app.domine.models.category import Category
from app.domine.models.client import Client
from app.domine.models.employee import Employee
from app.domine.models.order import Order
from app.domine.models.orderItem import OrderItem
from app.domine.models.product import Product
from app.domine.models.role import Role



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()