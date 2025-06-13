from sqlmodel import Session, select, or_
from typing import List, Optional
from app.domine.models.client import Client
from uuid import UUID

class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_client(self, clientCreate: Client) -> Client:
        self.session.add(clientCreate)
        self.session.commit()
        self.session.refresh(clientCreate)
        return clientCreate
    
    def get_all_clients(self) -> List[Client]:
        return self.session.exec(select(Client)).all()
    
    def get_client_with_username(self, username: str) -> Optional[Client]:
        return self.session.get(Client, username)
    
    def update_client(self, client_update: Client) -> Optional[Client]:
        self.session.add(client_update)
        self.session.commit()
        self.session.refresh(client_update)

        return client_update
    
    def delete_client(self, deleteClient: Client) -> Client:
        deleteClient.is_active = False
        deleted_client = self.update_client(deleteClient)
        return deleted_client

