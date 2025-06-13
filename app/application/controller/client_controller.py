from app.application.service.client_service import ClientService
from app.persistence.repositories.client_repository import ClientRepository
from app.presentation.schemas.client_schema import ClientCreate, ClientResponse, ClientUpdate
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID

class ClientController:
    def __init__(self, repository: ClientRepository):
        self.service = ClientService(repository)

    def create_client(self, client_create: ClientCreate) -> ClientResponse:
        return self.service.create_client(client_create)
    
    def get_all_clients(self) -> List[ClientResponse]:
        return self.service.get_all_clients()
    
    def get_client_with_username(self, username: str) -> ClientResponse:
        return self.service.get_client_with_username(username)
    
    def update_client(self, username: str, update_client: ClientUpdate) -> ClientResponse:
        return self.service.update_client(username, update_client)
    
    def delete_client(self, username: str) -> ClientResponse:
        return self.service.delete_client(username)