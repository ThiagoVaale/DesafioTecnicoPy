from app.persistence.repositories.product_repository import ProductRepository
from app.domine.models.product import Product
from fastapi import HTTPException
from app.presentation.schemas.product_schema import ProductResponse, ProductCreate, ProductUpdate
from typing import List

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository


    def create_product(self, create_product: ProductCreate) -> ProductResponse:
        product_exists = self.repository.get_product(create_product.name)

        if product_exists:
            raise HTTPException(status_code=409, detail=f'El producto ya existe')
        
        product = Product(**create_product.model_dump())
        created_product = self.repository.create_product(product)
        return ProductResponse.model_validate(created_product)
    
    def get_product(self, product_name: str) -> ProductResponse:
        product = self.repository.get_product(product_name)

        if product is None:
            raise HTTPException(status_code=404, detail=f'The product {product_name} was not found')
        
        return ProductResponse.model_validate(product)
    
    def get_products(self) -> List[ProductResponse]:
        products = self.repository.get_products()

        if not products:
            raise HTTPException(status_code=404, detail='There are no products')

        list_product = []

        for product in products: 
            product_orm = ProductResponse.model_validate(product)
            list_product.append(product_orm)
        
        return list_product
    
    def get_product_category(self, category: str) ->  List[ProductResponse]:
        product_category = self.repository.get_product_category(category)

        if not product_category:
            raise HTTPException(status_code=404, detail='There are no products in that category.')
        
        list_product_category = []

        for product in product_category:
            product_orm = ProductResponse.model_validate(product)
            list_product_category.append(product_orm)

        return list_product_category
    
    def update_product(self, product_name: str, product_update: ProductUpdate) -> ProductResponse:
        find_product = self.repository.get_product(product_name)

        if find_product is None:
            raise HTTPException(status_code=404, detail=f'The product {product_name} was not found and cannot be updated.')
        
        if product_update.stock < 0:
            raise HTTPException(status_code=416, detail='The stock cannot be less than 0')
        
        if product_update.stock == 0:
            find_product.is_active = False
        
        find_product.name = product_update.name
        find_product.description = product_update.description
        find_product.price = product_update.price
        find_product.stock = product_update.stock

        updated_prduct = self.repository.update_product(find_product)
        return ProductResponse.model_validate(updated_prduct)
        
    def delete_product(self, product_name: str) -> ProductResponse:
        product = self.repository.get_product(product_name)

        if product is None:
            raise HTTPException(status_code=404, detail=f'The product {product_name} does not exist and could not be deleted')
        
        deleted_product = self.repository.delete_product(product)
        return ProductResponse.model_validate(deleted_product)