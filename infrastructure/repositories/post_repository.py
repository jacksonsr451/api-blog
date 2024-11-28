from application.interfaces.base_repository_interface import (
    BaseRepositoryInterface,
)
from infrastructure.models.post_model import PostModel


class PostRepository(BaseRepositoryInterface):
    def __init__(self, model: PostModel, *args, **kargs):
        super().__init__(model, *args, **kargs)

    def create(self, data):
        return super().create(data)

    def update(self, id, data):
        return super().update(id, data)

    def view(self, id):
        return super().view(id)

    def list(self):
        return super().list()

    def delete(self, id):
        return super().delete(id)
