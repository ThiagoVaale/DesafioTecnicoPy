from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from app.presentation.schemas.client_schema import ClientCreate, ClientResponse, ClientUpdate
from sqlmodel import Session
from app.persistence.config.session import get_session
from app.application.controller.client_controller import ClientController
from app.persistence.repositories.client_repository import ClientRepository
from app.secutiry.dependencies import admin_required
from app.presentation.schemas.auth_schema import TokenData


router = APIRouter(prefix='/clients', tags=['clients'])

def get_controller(session: Session = Depends(get_session)) -> ClientController:
    repository = ClientRepository(session)
    return ClientController(repository)

@router.post('/', response_model=ClientResponse, status_code=201)
def create_client(create_client: ClientCreate, controller: ClientController = Depends(get_controller)):
    return controller.create_client(create_client)

@router.get('/', response_model=List[ClientResponse],status_code=200)
def get_all_clients(controller: ClientController = Depends(get_controller), current_admin: TokenData = Depends(admin_required)):
    return controller.get_all_clients()

@router.get('/by-username/{username}', response_model=ClientResponse, status_code=200)
def get_client_with_username(username: str, controller: ClientController = Depends(get_controller), current_admin: TokenData = Depends(admin_required)):
    return controller.get_client_with_username(username)

@router.put('/{username}', response_model=ClientResponse, status_code=200)
def update_client(username: str, update_client: ClientUpdate, controller: ClientController = Depends(get_controller)):
     return controller.update_client(username, update_client)

@router.delete('/{username}', status_code=200)
def delete_client(username: str, controller: ClientController = Depends(get_controller), current_admin: TokenData = Depends(admin_required)):
    return controller.delete_client(username)