from sqlmodel import Session, select, or_
from typing import List, Optional
from app.domine.models.client import Client
from uuid import UUID

class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_client(self, clientCreate: Client) -> Client:
        statement = select(Client).where(or_(Client.username == clientCreate.username, Client.password == clientCreate.password, Client.email == clientCreate.email))
        client_is_unique = self.session.exec(statement).first()

        if client_is_unique:
            return None

        self.session.add(clientCreate)
        self.session.commit()
        self.session.refresh(clientCreate)
        return clientCreate
    
    def get_all_clients(self) -> List[Client]:
        statement = select(Client)
        result = self.session.exec(statement)
        return result.all()
    
    def get_client_with_id(self, client_id: UUID) -> Optional[Client]:
        return self.session.get(Client, client_id)
    
    def update_client(self, client_id: UUID, client_update: Client) -> Client:
        client_db = self.session.get(Client, client_id)

        if not client_db:
            return None
        
        client_db.username = client_update.username
        client_db.email = client_update.email
        client_db.address = client_update.address
        client_db.phone = client_update.phone

        self.session.add(client_db)
        self.session.commit()
        self.session.refresh(client_db)

        return client_db
    
    def delete_client(self, client_id: UUID) -> Optional[Client]:
        client_db = self.session.get(Client, client_id)        
        client_db.is_active = False
        self.session.commit()
        return client_db

