from fastapi import Depends
from app.persistence.config.session import get_session
from app.application.controller.auth_controller import AuthControler
from app.persistence.repositories.auth_repository import AuthRepository
from app.application.service.auth_service import AuthService
from app.application.controller.auth_controller import AuthControler


def get_auth_controller(session = Depends(get_session)) -> AuthControler:
    repository = AuthRepository(session)
    service = AuthService(repository)
    controller = AuthControler(service)

    return controller