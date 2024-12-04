from application.interfaces.author_repository_interface import AuthorRepositoryInterface


class AuthorRepository(AuthorRepositoryInterface):
    def __init__(self, session, model, *args, **kargs):
        super().__init__(session, model, *args, **kargs)

    def view(self, id):
        return super().view(id)

    def list(self, order_by: str = "created_at", filter: str = None):
        return super().list(order_by)
