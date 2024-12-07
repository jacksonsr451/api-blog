from application.interfaces.author_repository_interface import AuthorRepositoryInterface
from infrastructure.models.author_model import AuthorModel


class AuthorRepository(AuthorRepositoryInterface):
    def __init__(self, session, model: AuthorModel, *args, **kargs):
        super().__init__(session, model, *args, **kargs)

    def view(self, id):
        return super().view(id)

    def list(self, order_by: str = "created_at", filter: str = None):
        return super().list(order_by)
