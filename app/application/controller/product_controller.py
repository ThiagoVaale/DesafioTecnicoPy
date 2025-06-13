from app.persistence.repositories.product_repository import ProductRepository
from app.application.service.product_service import ProductService
from app.presentation.schemas.product_schema import ProductCreate, ProductResponse
from typing import List


class ProductController:
    def __init__(self, repository: ProductRepository):
        self.service = ProductService(repository)

    def create_product(self, create_product:  ProductCreate) -> ProductResponse:
        self.service.create_product(create_product)

    def get_product(self, product_name: str) -> ProductResponse:
        self.service.get_product(product_name)

    def get_products(self) -> List[ProductResponse]:
        self.service.get_products()

    def get_product_category(self, category: str) -> List[ProductResponse]:
        self.service.get_product_category(category)

    def update_product(self, product_name: str, product_update: ProductCreate) -> ProductResponse:
        self.service.update_product(product_name, product_update)

    def delete_product(self, product_name: str) -> ProductResponse:
        self.service.delete_product(product_name)
