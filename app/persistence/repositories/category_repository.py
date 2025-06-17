from sqlmodel import Session, select
from app.domine.models.category import Category
from typing import Optional, List
from sqlalchemy.orm import selectinload
from app.presentation.schemas.category_schema import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, new_category: str) -> Category:
        category = Category(name=new_category)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category


    def get_category(self, name_category: str) -> Optional[Category]:
        return self.session.exec(select(Category).where(Category.name == name_category)).first()
    
    def get_category_products(self, name_category: str) -> Optional[Category]:
        return self.session.exec(select(Category).where(Category.name == name_category).options(selectinload(Category.products))).first()
    
    def update_category(self, name_category: str, new_category: CategoryUpdate) -> Optional[Category]:
        category = select(Category).where(Category.name == name_category)
        first_category = self.session.exec(category).first()

        first_category.name = new_category.new_name

        self.session.add(first_category)
        self.session.commit()
        self.session.refresh(first_category)

        return first_category
    

    def delete_category(self, category_delete: Category) -> Optional[Category]:
        category = self.get_category(category_delete.name)

        category.is_active = False

        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)

        return category

        

