from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.persistence.config.session import get_session
from app.application.controller.product_controller import ProductController
from app.persistence.repositories.product_repository import ProductRepository
from app.presentation.schemas.product_schema import ProductResponse, ProductCreate, ProductUpdate
from typing import List, Optional
from app.secutiry.dependencies import admin_required, employee_required
from app.presentation.schemas.auth_schema import TokenData

router = APIRouter(prefix='/products', tags=['products'])

def get_controller(session: Session = Depends(get_session)) -> ProductController:
    repository = ProductRepository(session)
    return ProductController(repository)

@router.post('/', response_model=ProductResponse, status_code=201)
def create_product(create_product: ProductCreate, controller: ProductController = Depends(get_controller), 
                   current_admin: TokenData = Depends(admin_required), current_employee: TokenData = Depends(employee_required)):
    return controller.create_product(create_product)

@router.get('/', response_model=List[ProductResponse], status_code=200)
def get_products(controller: ProductController = Depends(get_controller)):
    return controller.get_products()

@router.get('/{product_name}', response_model=ProductResponse, status_code=200)
def get_product(product_name: str, controller: ProductController = Depends(get_controller)):
    return controller.get_product(product_name)

@router.get('/{product_category}', response_model=List[ProductResponse], status_code=202)
def get_products_category(
    product_category: Optional[str],
    controller: ProductController = Depends(get_controller)):
    return controller.get_product_category(product_category)


@router.put('/{product_name}', response_model=ProductResponse, status_code=200)
def update_product(product_name: str, product_update: ProductUpdate, controller: ProductController = Depends(get_controller), 
                   current_admin: TokenData = Depends(admin_required), current_employee: TokenData = Depends(employee_required)):
    return controller.update_product(product_name, product_update)


@router.delete('/{product_name}', response_model=ProductResponse, status_code=200)
def delete_product(product_name: str, controller: ProductController = Depends(get_controller), 
                   current_admin: TokenData = Depends(admin_required), current_employee: TokenData = Depends(employee_required)):
    return controller.delete_product(product_name)