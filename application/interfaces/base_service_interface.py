from abc import ABC

from application.interfaces.base_repository_interface import BaseRepositoryInterface


class BaseServiceInterface(ABC):
    def __init__(self, repository: BaseRepositoryInterface):
        self._repository = repository
