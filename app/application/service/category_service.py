from app.persistence.repositories.category_repository import CategoryRepository
from app.presentation.schemas.category_schema import CategoryCreate, CategoryResponse, ProductCategoryResponse
from typing import List
from fastapi import HTTPException
from app.domine.models.category import Category

class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create_category(self, name_category: str) -> CategoryResponse:
        category_exists = self.repository.get_category(name_category)

        if category_exists:
            raise HTTPException(status_code=409, detail=f'La categoria {name_category} ya existe')
        
        new_category = Category(name=name_category)
        created_category = self.repository.create_category(new_category)
        return CategoryResponse.model_validate(created_category)
    
    def get_category(self, name_category: str) -> CategoryResponse:
        category = self.repository.get_category(name_category)

        if category is None:
            raise HTTPException(status_code=404, detail=f'La categoria {name_category} no se encontro')
        
        return CategoryResponse.model_validate(category)
    
    def get_category_products(self, name_category: str) -> ProductCategoryResponse:
        category_product = self.repository.get_category_products(name_category)

        if category_product is None:
            raise HTTPException(status_code=404, detail=f'No existen productos con categoria: {name_category}')
        
        return ProductCategoryResponse.model_validate(category_product)
    
    def update_category(self, name_category: str, new_category: str) -> CategoryResponse:
        if name_category == new_category:
            raise HTTPException(status_code=400, detail=F'No puede actualizar la categoria con el mismo nombre')
        
        category_exists = self.repository.get_category(name_category)

        if not category_exists:
            raise HTTPException(status_code=404, detail=f'La categoria {category_exists} no existe')
        
        updated_category = self.repository.update_category(name_category, new_category)
        return CategoryResponse.model_validate(updated_category)
        

    def delete_category(self, name_category: str) -> CategoryResponse:
        category = self.repository.get_category(name_category)

        if category is None:
            raise HTTPException(status_code=404, detail=f'La categoria {name_category} no existe. No se pudo eliminar')
        
        if category.is_active == False:
            raise HTTPException(status_code=409, detail=f'La categoria {name_category} ya ha sido borrada')
        
        deleted_category = self.repository.delete_category(category)
        return CategoryResponse.model_validate(deleted_category)
        


