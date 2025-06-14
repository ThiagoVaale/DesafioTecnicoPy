from sqlmodel import Session, select
from app.domine.models.category import Category
from typing import Optional
from sqlalchemy.orm import selectinload

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, name_category: str) -> Category:
        new_category = Category(name=name_category)
        self.session.add(new_category)
        self.session.commit()
        self.session.refresh(new_category)
        return new_category

    def get_category(self, name_category: str) -> Optional[Category]:
        category = select(Category).where(Category.name == name_category)
        first_category = self.session.exec(category).first()
        return first_category

    def get_category_products(self, name_category: str) -> Optional[Category]:
        category = select(Category).where(Category.name == name_category).options(selectinload(Category.products))
        get_category = self.session.exec(category).first()

        if get_category:
            get_category.products = [p for p in get_category.products if p.is_active]
        
        return get_category
    
    def update_category(self, name_category: str, new_category: str) -> Optional[Category]:
        category = select(Category).where(Category.name == name_category)
        first_category = self.session.exec(category).first()

        first_category.name = new_category

        self.session.add(first_category)
        self.session.commit()
        self.session.refresh(first_category)

        return first_category
    

    def delete_category(self, name_category: str) -> Optional[Category]:
        category = self.get_category(name_category)

        category.is_active = False

        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)

        return category

        

