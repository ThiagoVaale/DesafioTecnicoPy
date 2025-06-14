from app.persistence.repositories.client_repository import ClientRepository
from app.presentation.schemas.client_schema import ClientCreate, ClientResponse, ClientUpdate
from app.domine.models.client import Client
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID

class ClientService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def create_client(self, create_client: ClientCreate) -> ClientResponse:
        existing_client = self.repository.get_client_with_username(create_client.username)

        if existing_client:
            raise HTTPException(status_code=400, detail=f'El usuario ya existe')
        
        client = Client(**create_client.model_dump())
        created = self.repository.create_client(client)
        return ClientResponse.model_validate(created)
            
    def get_all_clients(self) -> List[ClientResponse]:
        clients = self.repository.get_all_clients()
        if not clients:
            raise HTTPException(status_code=404, detail='No existen clientes')
        
        list_clients = []
        
        for client in clients:
            client_orm = ClientResponse.model_validate(client)
            list_clients.append(client_orm)
        return list_clients
    
    def get_client_with_username(self, username:str) -> ClientResponse:
        client_find = self.repository.get_client_with_username(username)

        if client_find is None:
            raise HTTPException(
                status_code=404, detail=f'Cliente no encontrado'
            )
        
        return ClientResponse.model_validate(client_find)
    
    def update_client(self, username: str, update_client: ClientUpdate) -> ClientResponse:
        client_find = self.repository.get_client_with_username(username)
        
        if client_find is None:
            raise HTTPException(
                status_code=400, detail='El cliente no se pudo actualizar'
            )
        
        client_find.username = update_client.username
        client_find.email = update_client.email
        client_find.address = update_client.address
        client_find.phone = update_client.phone

        updated = self.repository.update_client(client_find)
        return ClientResponse.model_validate(updated)
    
    def delete_client(self, username: str) -> ClientResponse:
        client = self.repository.get_client_with_username(username)

        if client is None:
            raise HTTPException(
            status_code=400, detail=f'El cliente no se encontró'
        )

        deleted_client = self.repository.delete_client(client)
        return ClientResponse.model_validate(deleted_client)
        
        