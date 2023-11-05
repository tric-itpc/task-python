from enum import Enum


class ServiceStates(Enum):
    WORKS = 'работает'
    NOT_WORKS = 'не работает'
    WORKS_UNSTABLE = 'работает нестабильно'
