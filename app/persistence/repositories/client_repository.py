from sqlmodel import Session, select, or_
from typing import List, Optional
from app.domine.models.client import Client
from uuid import UUID
from app.presentation.schemas.client_schema import ClientCreate

class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_client(self, client_create: Client) -> Client:
        self.session.add(client_create)
        self.session.commit()
        self.session.refresh(client_create)
        return client_create
    
    def get_all_clients(self) -> List[Client]:
        return self.session.exec(select(Client).where(Client.is_active == True)).all()
    
    def get_client_with_username(self, username: str) -> Optional[Client]:
        return self.session.exec(select(Client).where(Client.username == username)).first()
    
    def get_client_with_password(self, passsword: str) -> Optional[Client]:
        return self.session.exec(select(Client).where(Client.password == passsword)).first()

    def get_client_with_id(self, id_client: UUID) -> Optional[Client]:
        return self.session.exec(select(Client).where(Client.id == id_client)).first()

    def update_client(self, client_update: Client) -> Optional[Client]:
        self.session.add(client_update)
        self.session.commit()
        self.session.refresh(client_update)

        return client_update
    
    def delete_client(self, deleteClient: Client) -> Client:
        deleteClient.is_active = False
        self.session.add(deleteClient)
        self.session.commit()
        self.session.refresh(deleteClient)
        return deleteClient

