from application.interfaces.post_repository_interface import PostRepositoryInterface
from application.interfaces.post_service_interface import (
    PostServiceIniterface,
)
from application.services.post_services import PostServices
from infrastructure.models.post_model import PostModel
from interfaces.controllers.post_controller import PostController
from interfaces.interfaces.post_controller_interface import PostControllerInterface
from tests.unit.test_post_services import PostRepository
from .config.container import DependencyContainer

container = DependencyContainer()

container.register(PostModel, PostModel)
container.register(
    PostRepositoryInterface, lambda: PostRepository(container.resolve(PostModel))
)
container.register(
    PostServiceIniterface,
    lambda: PostServices(container.resolve(PostRepositoryInterface)),
)
container.register(
    PostControllerInterface,
    lambda: PostController(container.resolve(PostServiceIniterface)),
)
