from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from uuid import UUID
from app.presentation.schemas.client_schema import ClientCreate, ClientResponse, ClientUpdate
from sqlmodel import Session
from app.persistence.config.session import get_session
from app.application.controller.client_controller import ClientController
from app.persistence.repositories.client_repository import ClientRepository


router = APIRouter(prefix='/clients', tags=['clients'])

def get_controller(session: Session = Depends(get_session)) -> ClientController:
    repository = ClientRepository(session)
    return ClientController(repository)

@router.post('/', response_model=ClientResponse, status_code=201)
def create_client(create_client: ClientCreate, controller: ClientController = Depends(get_controller)):
    return controller.create_client(create_client)

@router.get('/', response_model=List[ClientResponse],status_code=200)
def get_all_client(controller: ClientController = Depends(get_controller)):
    return controller.get_all_clients()

@router.get('/{username}', response_model=ClientResponse, status_code=200)
def get_client_with_username(username: UUID, controller: ClientController = Depends(get_controller())):
    return controller.get_client_with_username(username)

@router.put('/{username}', response_model=ClientResponse, status_code=200)
def update_client(username: str, updateClient: ClientUpdate, controller: ClientController = Depends(get_controller())):
     return controller.update_client(username, updateClient)

@router.delete('/{username}', status_code=200)
def delete_client(username: str, controller: ClientController = Depends(get_controller())):
    return controller.delete_client(username)