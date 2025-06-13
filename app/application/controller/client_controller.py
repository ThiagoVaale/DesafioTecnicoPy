from app.application.service.client_service import ClientService
from app.presentation.schemas.client_schema import ClientCreate, ClientResponse, ClientUpdate
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID

class ClientController:
    def __init__(self, session: Session):
        self.service = ClientService(session)

    def create_client(self, client_create: ClientCreate) -> ClientResponse:
        return self.service.create_client(client_create)
    
    def get_all_clients(self) -> List[ClientResponse]:
        return self.service.get_all_clients()
    
    def get_client_with_id(self, client_id: UUID) -> Optional[ClientResponse]:
        return self.service.get_client_with_id(client_id)
    
    def update_client(self, update_client: ClientUpdate) -> ClientResponse:
        return self.service.update_client(update_client)
    
    def delete_client(self, client_id: UUID) -> Optional[ClientResponse]:
        return self.service.delete_client(client_id)