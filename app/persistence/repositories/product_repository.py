from sqlmodel import Session, select
from app.domine.models.product import Product
from app.domine.models.category import Category
from typing import Optional, List
from uuid import UUID
from app.presentation.schemas.product_schema import ProductCreate
from sqlalchemy.orm import selectinload


class ProductRepository: 
    def __init__(self, session: Session):
        self.session = session

    def create_product(self, create_product: ProductCreate) -> Product:
        product = Product(**create_product.model_dump())
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product
    
    def get_product(self, product_name: str) -> Optional[Product]:
        product = select(Product).where(Product.name == product_name)
        return self.session.exec(product).first()
    
    def get_product_id(self, id_product: UUID) -> Optional[Product]:
        return self.session.exec(select(Product).where(Product.id == id_product)).first()
    
    def get_products(self) -> List[Product]:
        return self.session.exec(select(Product).where(Product.is_active == True).options(selectinload(Product.category))).all()
    
    def get_product_category(self, category: str) -> List[Product]:
        products_category = select(Product).join(Category).where(Category.name == category, Product.is_active == True)
        return self.session.exec(products_category).all()
    
    def update_product(self, product_update: Product) -> Product:
        self.session.add(product_update)
        self.session.commit()
        self.session.refresh(product_update)
        return product_update
    
    def reduce_stock(self, id_product: UUID, quantity_product: int) -> Product:
        product = self.get_product_id(id_product)

        product.stock -= quantity_product

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
    
    def delete_product(self, product: Product) -> Product:
        product.is_active = False
        deleted_product = self.update_product(product)
        return deleted_product

 