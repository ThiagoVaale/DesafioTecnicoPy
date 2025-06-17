from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.persistence.config.session import get_session
from app.application.controller.category_controller import CategoryController
from app.persistence.repositories.category_repository import CategoryRepository
from app.presentation.schemas.category_schema import CategoryResponse, ProductCategoryResponse, CategoryCreate, CategoryUpdate
from typing import List, Optional
from app.secutiry.dependencies import admin_required, employee_required
from app.presentation.schemas.auth_schema import TokenData


router = APIRouter(prefix='/categories', tags=['categories'])

def get_controller(session: Session = Depends(get_session)) -> CategoryController:
    repository = CategoryRepository(session)
    return CategoryController(repository)


@router.post('/', response_model=CategoryResponse, status_code=201)
def create_category(create_category: str, controller: CategoryController = Depends(get_controller), 
                current_admin: TokenData = Depends(admin_required), current_employee: TokenData = Depends(employee_required)):
    return controller.create_category(create_category)

@router.get('/{name_category}', response_model=CategoryResponse, status_code=202)
def get_category(name_category: str, controller: CategoryController = Depends(get_controller)):
    return controller.get_category(name_category)

@router.get('/{name_category_product}/products', response_model=List[ProductCategoryResponse], status_code=200)
def get_category_products(name_category_product: str, controller: CategoryController = Depends(get_controller)):
    return controller.get_category_products(name_category_product)

@router.put('/{name_category}', response_model=CategoryResponse, status_code=200)
def update_category(name_category: str, category_update: CategoryUpdate, controller: CategoryController = Depends(get_controller), 
                    current_admin: TokenData = Depends(admin_required), current_employee: TokenData = Depends(employee_required)):
    return controller.update_category(name_category, category_update)

@router.delete('/{name_category}', response_model=CategoryResponse, status_code=200)
def delete_category(name_category: str, controller: CategoryController = Depends(get_controller), 
                    current_admin: TokenData = Depends(admin_required), current_employee: TokenData = Depends(employee_required)):
    return controller.delete_category(name_category)