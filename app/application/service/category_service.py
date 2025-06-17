from app.persistence.repositories.category_repository import CategoryRepository
from app.presentation.schemas.category_schema import CategoryCreate, CategoryResponse, ProductCategoryResponse, CategoryUpdate
from typing import List
from fastapi import HTTPException
from app.domine.models.category import Category

class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create_category(self, name_category: str) -> CategoryResponse:
        category_exists = self.repository.get_category(name_category)

        if category_exists:
            raise HTTPException(status_code=409, detail=f'Category {name_category} already exists.')
        
        created_category = self.repository.create_category(name_category)
        return CategoryResponse.model_validate(created_category)
    
    def get_category(self, name_category: str) -> List[CategoryResponse]:
        category = self.repository.get_category(name_category)

        if not category:
            raise HTTPException(status_code=404, detail='There are no active categories')

        return CategoryResponse.model_validate(category)
    
    def get_category_products(self, name_category: str) -> List[ProductCategoryResponse]:
        category = self.repository.get_category_products(name_category)

        if category is None or not category.products:
            raise HTTPException(status_code=404, detail=f'There are no products with category: {name_category}')
        
        list_products = []

        for product in category.products:
            product_orm = ProductCategoryResponse.model_validate(product)
            list_products.append(product_orm)

        return list_products
    
    def update_category(self, name_category: str, new_category: CategoryUpdate) -> CategoryResponse:
        if name_category == new_category.new_name:
            raise HTTPException(status_code=400, detail='Cannot update category with the same name')
        
        category_exists = self.repository.get_category(name_category)

        if not category_exists:
            raise HTTPException(status_code=404, detail=f'The category {name_category} does not exist')
        
        updated_category = self.repository.update_category(name_category, new_category)
        return CategoryResponse.model_validate(updated_category)
        

    def delete_category(self, name_category: str) -> CategoryResponse:
        category = self.repository.get_category(name_category)

        if category is None:
            raise HTTPException(status_code=404, detail=f'The category {name_category} does not exist. It could not be deleted.')
        
        if category.is_active == False:
            raise HTTPException(status_code=409, detail=f'The category {name_category} has already been deleted')
        
        deleted_category = self.repository.delete_category(category)
        return CategoryResponse.model_validate(deleted_category)
        


