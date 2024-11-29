from .base_repository_interface import BaseRepositoryInterface


class PostRepositoryInterface(BaseRepositoryInterface):
    def __init__(self, session, model, *args, **kargs):
        super().__init__(session, model, *args, **kargs)
