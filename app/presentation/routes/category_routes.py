from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.persistence.config.session import get_session
from app.application.controller.category_controller import CategoryController
from app.persistence.repositories.category_repository import CategoryRepository
from app.presentation.schemas.category_schema import CategoryResponse, ProductCategoryResponse, CategoryCreate, CategoryUpdate
from typing import List


router = APIRouter(prefix='categories', tags=['categories'])

def get_controller(session: Session = Depends(get_session)) -> CategoryController:
    repository = CategoryRepository(session)
    return CategoryController(repository)


@router.post('/', response_model=CategoryResponse, status_code=201)
def create_category(create_category: CategoryCreate, controller: CategoryController = Depends(get_controller)):
    return controller.create_category(create_category)

@router.get('/name', response_model=List[CategoryResponse], status_code=202)
def get_category(name_category: str, controller: CategoryController = Depends(get_controller)):
    return controller.get_category(name_category)

@router.get('/{name_category}', response_model=ProductCategoryResponse, status_code=200)
def get_category_products(name_category: str, controller: CategoryController = Depends(get_controller)):
    return controller.get_category_products(name_category)

@router.put('/{name_category}', response_model=CategoryResponse, status_code=200)
def update_category(name_category: str, category_update: CategoryUpdate, controller: CategoryController = Depends(get_controller)):
    return controller.update_category(name_category, category_update)

@router.delete('/{name_category}', response_model=CategoryResponse, status_code=200)
def delete_category(name_category: str, controller: CategoryController = Depends(get_controller)):
    return controller.delete_category(name_category)