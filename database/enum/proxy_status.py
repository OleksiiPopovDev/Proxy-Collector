from enum import Enum


class ProxyStatus(Enum):
    IN_PROGRESS: str = 'in progress'
    VALID: str = 'valid'
    INVALID: str = 'invalid'
