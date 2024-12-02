from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.dtos.post_dto import PostDTO
from application.interfaces.base_repository_interface import (
    BaseRepositoryInterface,
)
from application.services.post_services import PostServices
from infrastructure.models.author_model import AuthorModel
from infrastructure.models.post_model import PostModel


class PostRepository(BaseRepositoryInterface):
    def __init__(self, model: PostModel, *args, **kargs):
        super().__init__(model, *args, **kargs)


@pytest.fixture
def mock_values():
    return dict(
        id=str(uuid4()),
        title="Test Post",
        description="A post for testing",
        body="This is the body of the post",
        slug="test-post",
        author=dict(
            id=str(uuid4()),
            firstname="John",
            lastname="Doe",
            description="Author description",
            resume="Author resume",
        ),
        status=True,
        thumbnail="http://example.com/thumbnail.jpg",
    )


@pytest.fixture
def mock_repository(mock_values):
    mock_repo = MagicMock(spec=PostRepository)

    mock_values_copy = mock_values.copy()
    author_data = mock_values_copy.pop("author")
    author_instance = AuthorModel(**author_data)

    expected_post_entity = PostModel(author=author_instance, **mock_values_copy)

    mock_repo.create.return_value = expected_post_entity
    mock_repo.view.return_value = expected_post_entity
    mock_repo.list.return_value = [expected_post_entity]

    return mock_repo


@pytest.fixture
def post_data(mock_values):
    return PostDTO(**mock_values)


@pytest.mark.asyncio
async def test_execute_create(mock_repository: PostRepository, post_data: PostDTO):
    service = PostServices(mock_repository)
    service.create_a_new_post(post_data)

    result = await service.execute()
    result_dto = service.convert_dto_to_model(result)

    assert result.title == post_data.title
    assert result.id != None
    mock_repository.create.assert_called_once_with(result_dto)


@pytest.mark.asyncio
async def test_execute_update(mock_repository: PostRepository, post_data: PostDTO):
    service = PostServices(mock_repository)
    post_data.title = "Updated Title"

    service.update_a_post(post_data.id)
    service.set_post_data(post_data)
    post_model = service.convert_dto_to_model(post_data)
    result = await service.execute()

    assert result.title == "Updated Title"
    mock_repository.update.assert_called_once_with(post_data.id, post_model)


@pytest.mark.asyncio
async def test_execute_delete(mock_repository: PostRepository, post_data: PostDTO):
    service = PostServices(mock_repository)
    service.create_a_new_post(post_data)
    service.delete_a_post(post_data.id)

    result = await service.execute()
    assert result is None
    mock_repository.delete.assert_called_once_with(post_data.id)


@pytest.mark.asyncio
async def test_execute_view(mock_repository: PostRepository, post_data: PostDTO):
    service = PostServices(mock_repository)
    service.create_a_new_post(post_data)

    service.view_a_post(post_data.id)
    result = await service.execute()

    assert result is not None
    assert result.id == post_data.id
    mock_repository.view.assert_called_once_with(result.id)


@pytest.mark.asyncio
async def test_list_all_posts(mock_repository: PostRepository, post_data: PostDTO):
    service = PostServices(mock_repository)
    service.create_a_new_post(post_data)
    service.list_all_posts()

    result = await service.execute()

    assert isinstance(result, list)
    mock_repository.list.assert_called_once()
