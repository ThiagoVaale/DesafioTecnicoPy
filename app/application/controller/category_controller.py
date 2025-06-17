from app.persistence.repositories.category_repository import CategoryRepository
from app.application.service.category_service import CategoryService
from app.presentation.schemas.category_schema import CategoryResponse, ProductCategoryResponse, CategoryUpdate
from typing import List, Optional


class CategoryController:
    def __init__(self, repository: CategoryRepository):
        self.service = CategoryService(repository)
    
    def create_category(self, name_category: str) -> CategoryResponse:
        return self.service.create_category(name_category)
    
    def get_category(self, name_category: str) -> Optional[CategoryResponse]:
        return self.service.get_category(name_category)
    
    def get_category_products(self, name_category:str) -> List[ProductCategoryResponse]:
        return self.service.get_category_products(name_category)
    
    def update_category(self, name_category: str, new_category: CategoryUpdate) -> CategoryResponse:
        return self.service.update_category(name_category, new_category)
    
    def delete_category(self, name_category: str) -> CategoryResponse:
        return self.service.delete_category(name_category)