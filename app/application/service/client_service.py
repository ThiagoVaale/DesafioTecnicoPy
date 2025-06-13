from app.persistence.repositories.client_repository import ClientRepository
from app.presentation.schemas.client_schema import ClientCreate, ClientResponse, ClientUpdate
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID

class ClientService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def create_client(self, create_client: ClientCreate) -> ClientResponse:
        client_is_unique = self.repository.create_client(create_client)

        if client_is_unique is None:
            raise HTTPException(
                status_code=400, detail=f'El usuario ya existe'
            )
        
        return client_is_unique
            
    def get_all_clients(self) -> List[ClientResponse]:
        clients = self.repository.get_all_clients()

        if not clients:
            raise HTTPException(
                status_code=404, detail='No existen usuarios'
            )

        return clients
    
    def get_client_with_id(self, client_id:UUID) -> Optional[ClientResponse]:
        client_find = self.repository.get_client_with_id(client_id)

        if client_find is None:
            raise HTTPException(
                status_code=404, detail=f'El id de usuario: {client_id} no se encontro'
            )
        
        return client_find
    
    def update_client(self, update_client: ClientUpdate) -> ClientResponse:
        update_client = self.repository.update_client(update_client)

        if update_client is None:
            raise HTTPException(
                status_code=400, detail='El cliente no se pudo actualizar'
            )
        
        return update_client
    
    def delete_client(self, client_id: UUID) -> Optional[ClientResponse]:
        find_client = self.repository.get_client_with_id(client_id)

        try:
            if find_client is not None:
                deleted_client = self.repository.delete_client(client_id)
                return deleted_client
        except:
            raise HTTPException(
                status_code=400, detail=f'El id de usuario: {client_id} no se encontro y no se pudo eliminar'
            )