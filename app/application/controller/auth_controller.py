from app.application.service.auth_service import AuthService
from app.presentation.schemas.auth_schema import AuthLoginReponse, AuthLoginRequest

class AuthControler:
    def __init__(self, service: AuthService):
        self.service = service

    def login(self, login_request: AuthLoginRequest) -> AuthLoginReponse:
        return self.service.authenticate_user(login_request)