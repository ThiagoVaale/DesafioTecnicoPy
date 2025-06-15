from enum import Enum

class StatusOrderEnum(str, Enum):
    PAID = 'PAID'
    PENDING = 'PENDING'
    CANCELED = 'CANCELED'