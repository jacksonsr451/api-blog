from typing import List
from abc import ABC, abstractmethod

from fastapi import Request
from pydantic import BaseModel

from application.interfaces.base_service_interface import BaseServiceInterface


class AbstractControllerInterface(ABC):
    def __init__(self, service: BaseServiceInterface):
        super().__init__()

    @abstractmethod
    async def post(self, request: type[Request], *args, **kargs) -> str:
        pass

    @abstractmethod
    async def put(self, id: str, request: type[Request], *args, **kargs) -> str:
        pass

    @abstractmethod
    async def delete(self, id: str, *args, **kargs) -> str:
        pass

    @abstractmethod
    async def show(self, id: str, request: type[Request], *args, **kargs) -> BaseModel:
        pass

    @abstractmethod
    async def view(self, request: type[Request], *args, **kargs) -> List[BaseModel]:
        pass
