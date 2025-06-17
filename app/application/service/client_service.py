from app.persistence.repositories.client_repository import ClientRepository
from app.presentation.schemas.client_schema import ClientCreate, ClientResponse, ClientUpdate
from app.domine.models.client import Client
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ClientService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def create_client(self, create_client: ClientCreate) -> ClientResponse:
        existing_client = self.repository.get_client_with_username(create_client.username)
        hashed_password = pwd_context.hash(create_client.password)

        if existing_client:
            raise HTTPException(status_code=400, detail='The user already exists')
        
        client = Client(
            username=create_client.username,
            password=hashed_password,
            email=create_client.email,
            address=create_client.address,
            phone=create_client.phone,
            role_id=2
        )

        created_client = self.repository.create_client(client)
        return ClientResponse.model_validate(created_client)
            
    def get_all_clients(self) -> List[ClientResponse]:
        clients = self.repository.get_all_clients()

        if clients == []:
            raise HTTPException(status_code=404, detail='There are no clients')
        
        list_clients = []
        
        for client in clients:
            client_orm = ClientResponse.model_validate(client)
            list_clients.append(client_orm)
        return list_clients
    
    def get_client_with_username(self, username:str) -> ClientResponse:
        client_find = self.repository.get_client_with_username(username)

        if client_find is None:
            raise HTTPException(
                status_code=404, detail=f'Client {username} not found'
            )
        
        return ClientResponse.model_validate(client_find)
    
    def update_client(self, username: str, update_client: ClientUpdate) -> ClientResponse:
        client_find = self.repository.get_client_with_username(username)
        
        if client_find is None:
            raise HTTPException(
                status_code=404, detail='The client could not be updated'
            )
        
        username_exists = self.repository.get_client_with_username(update_client.username)
        if username_exists and username_exists.id != client_find.id:
            raise HTTPException(status_code=400, detail=f'El usuario {update_client.username} ya existe')
        

        password_exists = self.repository.get_client_with_password(update_client.password)
        if password_exists and password_exists.id != client_find.id:
            raise HTTPException(status_code=400, detail='A user with that password already exists.')
        
        client_find.username = update_client.username
        client_find.email = update_client.email
        client_find.address = update_client.address
        client_find.phone = update_client.phone

        updated = self.repository.update_client(client_find)
        return ClientResponse.model_validate(updated)
    
    def delete_client(self, username: str) -> ClientResponse:
        client = self.repository.get_client_with_username(username)

        if client.is_active == False:
            raise HTTPException(status_code=400, detail=f'The user {client.username} is already inactive')
        if client is None:
            raise HTTPException(
            status_code=400, detail=f'The client {username} was not found'
        )

        deleted_client = self.repository.delete_client(client)
        return ClientResponse.model_validate(deleted_client)
        
        