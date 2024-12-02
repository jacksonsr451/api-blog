from abc import ABC, abstractmethod
from typing import Optional

from application.dtos.post_dto import PostDTO
from application.interfaces.post_repository_interface import PostRepositoryInterface
from domain.src.post_entity import PostEntity
from infrastructure.models.post_model import PostModel


class PostServiceIniterface(ABC):
    def __init__(self, repository: PostRepositoryInterface):
        self._repository = repository

    @abstractmethod
    def init_new_post(self, data: PostDTO) -> "PostServiceIniterface":
        pass

    @abstractmethod
    def create_a_new_post(self, data: PostDTO) -> "PostServiceIniterface":
        pass

    @abstractmethod
    def set_post_data(self, data: PostDTO) -> "PostServiceIniterface":
        pass

    @abstractmethod
    def update_a_post(self, id: str) -> "PostServiceIniterface":
        pass

    @abstractmethod
    def delete_a_post(self, id: str) -> "PostServiceIniterface":
        pass

    @abstractmethod
    def view_a_post(self, id: str) -> "PostServiceIniterface":
        pass

    @abstractmethod
    def list_all_posts(self) -> "PostServiceIniterface":
        pass

    @abstractmethod
    async def execute(
        self,
    ) -> Optional[PostDTO] | Optional[list[PostDTO]] | None:
        pass

    @abstractmethod
    def convert_model_to_dto(self, model: PostModel) -> PostDTO:
        pass

    @abstractmethod
    def convert_entity_to_model(self, entity: PostEntity) -> PostModel:
        pass

    @abstractmethod
    def convert_dto_to_model(self, post_dto: PostDTO) -> PostModel:
        pass
