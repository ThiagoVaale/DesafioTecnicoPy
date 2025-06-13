from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from uuid import UUID
from app.presentation.schemas.client_schema import ClientCreate, ClientResponse, ClientUpdate
from sqlmodel import Session
from app.persistence.config.session import get_session
from app.application.controller.client_controller import ClientController
router = APIRouter(prefix='/clients', tags='clients')


@router.post('/', response_model=ClientResponse)
def create_client(create_client: ClientCreate, session: Session = Depends(get_session)):
    controller = ClientController(session)
    created_client = controller.create_client(create_client)

    if create_client:
        return {'status': 201, 'message': f'El usuario se creo exitosamente' }
  
    return {'status': 400, 'message': 'El usuario ya existe' }

@router.get('/', response_model=List[ClientResponse])
def get_all_client(session: Session):
    controller = ClientController(session)
    get_clients = controller.get_all_clients()

    if get_clients:
        return {'status': 200, 'message': f'{get_clients}' }
    
    return {'status': 404, 'message': 'No existen usuarios' } 

@router.get('/{client_id}', response_model=Optional[ClientResponse])
def get_client_with_id(session: Session, client_id: UUID):
    controller = ClientController(session)
    try:
        get_client = controller.get_client_with_id(client_id)
        return get_client
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put('/', response_model=ClientResponse)
def update_client(session: Session, updateClient: ClientUpdate):
     controller = ClientController(session)
     try:
        updatedClient = controller.update_client(update_client)
        return updatedClient
     except ValueError as e:
         raise HTTPException(status_code=400, detail=str(e))

@router.delete('/{client_id}')
def delete_client(session: Session, client_id: UUID):
    return 