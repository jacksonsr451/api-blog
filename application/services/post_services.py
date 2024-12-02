from typing import Optional

from application.dtos.author_dto import AuthorDTO
from application.dtos.post_dto import PostDTO
from application.interfaces.base_service_interface import BaseServiceInterface
from application.interfaces.post_repository_interface import PostRepositoryInterface
from domain.src.post_entity import PostEntity
from infrastructure.models.author_model import AuthorModel
from infrastructure.models.post_model import PostModel


class PostServices(BaseServiceInterface):
    def __init__(self, repository: PostRepositoryInterface):
        self._repository = repository
        self._post_entity: Optional[PostEntity] = None
        self._action: Optional[str] = None
        self._post_model: Optional[PostModel] = None

    def init_new_post(self, data: PostDTO) -> "PostServices":
        self._post_entity = PostEntity(**data.model_dump())
        return self

    def create_a_new_post(self, data: PostDTO) -> "PostServices":
        self._post_entity = PostEntity(title=data.title)
        self._post_entity.create_a_new_post(
            description=data.description, body=data.body
        )
        self._action = "create"
        return self

    def set_post_data(self, data: PostDTO) -> "PostServices":
        author = AuthorDTO(
            id=data.author.id,
            firstname=data.author.firstname,
            lastname=data.author.lastname,
            description=data.author.description,
            resume=data.author.resume,
        )

        self._post_entity.set_post_data(
            title=data.title,
            description=data.description,
            body=data.body,
            slug=data.slug,
            author=author,
            status=data.status,
            thumbnail=data.thumbnail,
        )
        return self

    def update_a_post(self, id: str) -> "PostServices":
        self._post_entity = PostEntity(id=id)
        self._action = "update"
        return self

    def delete_a_post(self, id: str) -> "PostServices":
        self._post_entity = PostEntity(id=id)
        self._action = "delete"
        return self

    def view_a_post(self, id: str) -> "PostServices":
        self._post_entity = PostEntity(id=id)
        self._action = "view"
        return self

    def list_all_posts(self) -> "PostServices":
        self._action = "list"
        return self

    async def execute(
        self,
    ) -> Optional[PostDTO] | Optional[list[PostDTO]] | None:
        if not self._action:
            raise ValueError("No action specified.")

        self._post_model = self.convert_entity_to_model(self._post_entity)

        match self._action:
            case "create":
                await self._repository.create(self._post_model)
                return self._post_model

            case "update":
                await self._repository.update(self._post_entity.id, self._post_model)
                return self._post_model

            case "delete":
                await self._repository.delete(self._post_entity.id)
                return None

            case "view":
                model = await self._repository.view(self._post_entity.id)
                return self.convert_model_to_dto(model) if model else None

            case "list":
                models = await self._repository.list()
                return [self.convert_model_to_dto(model) for model in models]

            case _:
                raise ValueError(f"Unknown action: {self._action}")

    def convert_model_to_dto(self, model: PostModel) -> PostDTO:
        author_dto = (
            AuthorDTO(
                id=str(model.author.id),
                firstname=str(model.author.firstname),
                lastname=str(model.author.lastname),
                description=str(model.author.description),
                resume=str(model.author.resume),
            )
            if model.author
            else None
        )

        return PostDTO(
            id=str(model.id),
            title=str(model.title),
            description=str(model.description),
            body=str(model.body),
            slug=str(model.slug),
            author=author_dto,
            author_id=str(model.author.id) if model.author else None,
            status=bool(model.status),
            thumbnail=str(model.thumbnail),
        )

    def convert_entity_to_model(self, entity: PostEntity) -> PostModel:
        author_entity = None
        if entity.author:
            author_entity = AuthorModel(
                id=entity.author.id,
                firstname=entity.author.firstname,
                lastname=entity.author.lastname,
                description=entity.author.description,
                resume=entity.author.resume,
            )

        return PostModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            body=entity.body,
            slug=entity.slug,
            status=entity.status,
            thumbnail=entity.thumbnail,
            author=author_entity,
        )

    def convert_dto_to_model(self, post_dto: PostDTO) -> PostModel:
        author_entity = None
        if post_dto.author:
            author_entity = AuthorModel(
                id=post_dto.author.id,
                firstname=post_dto.author.firstname,
                lastname=post_dto.author.lastname,
                description=post_dto.author.description,
                resume=post_dto.author.resume,
            )
        return PostModel(
            id=post_dto.id,
            title=post_dto.title,
            description=post_dto.description,
            body=post_dto.body,
            slug=post_dto.slug,
            status=post_dto.status,
            thumbnail=post_dto.thumbnail,
            author=author_entity,
        )
