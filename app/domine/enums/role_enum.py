from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = 'ADMIN'
    EMPLOYEE = 'EMPLOYEE'
    CLIENT = 'CLIENT'