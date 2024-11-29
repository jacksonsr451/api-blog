from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from application.dtos.author_dto import AuthorDTO
from application.dtos.post_dto import PostDTO
from infrastructure.models.author_model import AuthorModel
from infrastructure.models.post_model import PostModel
from infrastructure.repositories.post_repository import PostRepository


@pytest.fixture
def data_post() -> PostDTO:
    author_dto = AuthorDTO(
        id=str(uuid4()),
        firstname='John',
        lastname='Doe',
        description='Author description',
        resume='Author resume',
    )
    return PostDTO(
        id=str(uuid4()),
        title='Test Post',
        description='A post for testing',
        body='This is the body of the post',
        slug='test-post',
        author=author_dto,
        status=True,
        thumbnail='http://example.com/thumbnail.jpg',
    )


@pytest.fixture
async def setup_database(test_engine: AsyncEngine):
    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.create_all)
        await conn.run_sync(AuthorModel.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.drop_all)
        await conn.run_sync(AuthorModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_post(
    test_engine, test_session: AsyncSession, data_post: PostDTO
):
    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.create_all)
        await conn.run_sync(AuthorModel.metadata.create_all)

    async for session in test_session:
        post_repo = PostRepository(session, PostModel)
        await post_repo.create(data_post)

        post = await post_repo.view(data_post.id)
        assert post.title == data_post.title
        assert post.body == data_post.body

    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.drop_all)
        await conn.run_sync(AuthorModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_view_post(
    test_engine, test_session: AsyncSession, data_post: PostDTO
):
    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.create_all)
        await conn.run_sync(AuthorModel.metadata.create_all)

    async for session in test_session:
        post_repo = PostRepository(session, PostModel)
        await post_repo.create(data_post)

        post = await post_repo.view(data_post.id)
        assert post.title == data_post.title
        assert post.body == data_post.body

    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.drop_all)
        await conn.run_sync(AuthorModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_update_post(
    test_engine, test_session: AsyncSession, data_post: PostDTO
):
    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.create_all)
        await conn.run_sync(AuthorModel.metadata.create_all)

    async for session in test_session:
        post_repo = PostRepository(session, PostModel)
        await post_repo.create(data_post)
        updated_data = data_post
        updated_data.title = 'Updated Post'
        updated_data.body = 'Updated content'

        await post_repo.update(data_post.id, updated_data)
        post = await post_repo.view(data_post.id)

        assert post.title == 'Updated Post'
        assert post.body == 'Updated content'
    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.drop_all)
        await conn.run_sync(AuthorModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_list_posts(
    test_engine, test_session: AsyncSession, data_post: PostDTO
):
    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.create_all)
        await conn.run_sync(AuthorModel.metadata.create_all)

    async for session in test_session:
        post_repo = PostRepository(session, PostModel)
        await post_repo.create(data_post)

        posts = await post_repo.list()
        assert type(posts)
        assert len(posts) > 0

    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.drop_all)
        await conn.run_sync(AuthorModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_delete_post(
    test_engine, test_session: AsyncSession, data_post: PostDTO
):
    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.create_all)
        await conn.run_sync(AuthorModel.metadata.create_all)

    async for session in test_session:
        post_repo = PostRepository(session, PostModel)
        await post_repo.create(data_post)

        await post_repo.delete(data_post.id)

        with pytest.raises(ValueError):
            await post_repo.view(data_post.id)

    async with test_engine.begin() as conn:
        await conn.run_sync(PostModel.metadata.drop_all)
        await conn.run_sync(AuthorModel.metadata.drop_all)
