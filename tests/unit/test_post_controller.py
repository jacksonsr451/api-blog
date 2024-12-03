from uuid import uuid4

import pytest
from unittest.mock import AsyncMock, Mock
from interfaces.controllers.post_controller import PostController
from application.dtos.post_dto import PostDTO
from application.dtos.author_dto import AuthorDTO


@pytest.fixture
def mock_service():
    """Mock do PostServiceInterface"""
    service = Mock()
    service.create_a_new_post = AsyncMock()
    service.update_a_post = AsyncMock()
    service.set_post_data = AsyncMock()
    service.delete = AsyncMock()
    service.view = AsyncMock()
    service.list = AsyncMock()
    service.execute = AsyncMock(return_value="mocked_response")
    return service


@pytest.fixture
def post_controller(mock_service):
    """Instância do PostController com o mock do serviço"""
    return PostController(service=mock_service)


@pytest.fixture
def mock_post_dto():
    author_dto = AuthorDTO(
        id=str(uuid4()),
        firstname="John",
        lastname="Doe",
        description="Author description",
        resume="Author resume",
    )
    return PostDTO(
        id=str(uuid4()),
        title="Test Post",
        description="A post for testing",
        body="This is the body of the post",
        slug="test-post",
        author=author_dto,
        status=True,
        thumbnail="http://example.com/thumbnail.jpg",
    )


@pytest.mark.asyncio
async def test_post_success(post_controller, mock_service, mock_post_dto):
    response = await post_controller.post(request=mock_post_dto)
    mock_service.create_a_new_post.assert_called_once_with(mock_post_dto)
    mock_service.execute.assert_awaited_once()
    assert response == dict(message="Successful to create a new post!", status=200)


@pytest.mark.asyncio
async def test_post_error(post_controller, mock_service, mock_post_dto):
    mock_service.create_a_new_post.side_effect = Exception("Service error")
    response = await post_controller.post(request=mock_post_dto)
    assert response == dict(detail="Error to create a new post!", status=400)


@pytest.mark.asyncio
async def test_put_success(post_controller, mock_service, mock_post_dto):
    response = await post_controller.put(id="123", request=mock_post_dto)
    mock_service.set_post_data.assert_called_once_with(mock_post_dto)
    mock_service.update_a_post.assert_called_once_with("123")
    mock_service.execute.assert_awaited_once()
    assert response == dict(
        message="Updated message successfully to post by id: 123", status=200
    )


@pytest.mark.asyncio
async def test_put_error(post_controller, mock_service, mock_post_dto):
    mock_service.update_a_post.side_effect = Exception("Service error")
    response = await post_controller.put(id="123", request=mock_post_dto)
    assert response == dict(detail="Error to update a new post!", status=400)


@pytest.mark.asyncio
async def test_delete_success(post_controller, mock_service):
    response = await post_controller.delete(id="123")
    mock_service.delete.assert_called_once_with("123")
    mock_service.execute.assert_awaited_once()
    assert response == dict(message="Post deleted successfully", status=200)


@pytest.mark.asyncio
async def test_delete_error(post_controller, mock_service):
    mock_service.delete.side_effect = Exception("Service error")
    response = await post_controller.delete(id="123")
    assert response == dict(detail="Error to delete a post!", status=400)


@pytest.mark.asyncio
async def test_show_success(post_controller, mock_service):
    mock_service.execute.return_value = {"id": "123", "title": "Mock Post"}
    response = await post_controller.show(id="123", request=None)
    mock_service.view.assert_called_once_with("123")
    mock_service.execute.assert_awaited_once()
    assert response == dict(data={"id": "123", "title": "Mock Post"}, status=200)


@pytest.mark.asyncio
async def test_show_error(post_controller, mock_service):
    mock_service.view.side_effect = Exception("Service error")
    response = await post_controller.show(id="123", request=None)
    assert response == dict(
        detail="Error to show a post with id: 123, error: Service error", status=400
    )


@pytest.mark.asyncio
async def test_view_success(post_controller, mock_service):
    mock_service.execute.return_value = [{"id": "123", "title": "Mock Post"}]
    response = await post_controller.view(request=None)
    mock_service.list.assert_called_once()
    mock_service.execute.assert_awaited_once()
    assert response == dict(data=[{"id": "123", "title": "Mock Post"}], status=200)


@pytest.mark.asyncio
async def test_view_error(post_controller, mock_service):
    mock_service.list.side_effect = Exception("Service error")
    response = await post_controller.view(request=None)
    assert response == dict(detail="Error to list posts", status=400)
