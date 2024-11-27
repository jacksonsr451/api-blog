from uuid import uuid4

import pytest

from domain.src.author_entity import AuthorEntity
from domain.src.post_entity import PostEntity


@pytest.fixture
def author_entity():
    return AuthorEntity(
        id=str(uuid4()),
        firstname='Test',
        lastname='Author',
        description='A sample author',
        resume='Experienced in writing.',
    )


def test_create_post_entity_with_valid_data():
    title = 'Test Post'
    post = PostEntity(title=title)

    assert post.id is not None
    assert post.title == title
    assert post.description is None
    assert post.body is None
    assert post.slug is None
    assert post.author is None
    assert not post.status
    assert post.thumbnail is None


def test_set_post_data(author_entity):
    post = PostEntity(title='Initial Title')
    post.set_post_data(
        title='Updated Title',
        description='Updated Description',
        body='Updated Body',
        slug='updated-title',
        author=author_entity,
        status=True,
        thumbnail='http://example.com/thumbnail.jpg',
    )

    assert post.title == 'Updated Title'
    assert post.description == 'Updated Description'
    assert post.body == 'Updated Body'
    assert post.slug == 'updated-title'
    assert post.author == author_entity
    assert post.status
    assert post.thumbnail == 'http://example.com/thumbnail.jpg'


def test_create_a_new_post_generates_slug():
    post = PostEntity(title='My New Post')
    post.create_a_new_post(description='Test Description', body='Test Body')

    assert post.description == 'Test Description'
    assert post.body == 'Test Body'
    assert post.slug == 'my-new-post'


def test_create_a_new_post_without_description_raises_error():
    post = PostEntity(title='My New Post')
    with pytest.raises(ValueError, match='Description is required.'):
        post.create_a_new_post(description=None, body='Test Body')


def test_create_a_new_post_without_body_raises_error():
    post = PostEntity(title='My New Post')
    with pytest.raises(ValueError, match='Body is required.'):
        post.create_a_new_post(description='Test Description', body=None)


def test_publish_post():
    post = PostEntity(title='Publish Test')
    post.create_a_new_post(description='Test Description', body='Test Body')
    post.publish()

    assert post.status


def test_publish_post_without_description_or_body_raises_error():
    post = PostEntity(title='Incomplete Post')
    with pytest.raises(
        ValueError,
        match='Post must have a description and body before being published.',
    ):
        post.publish()


def test_thumbnail_setter():
    post = PostEntity(title='Test Post')
    post.thumbnail = 'http://example.com/image.jpg'

    assert post.thumbnail == 'http://example.com/image.jpg'


def test_generate_slug():
    post = PostEntity(title='Complex Title: With Special Characters!')
    post.create_a_new_post(description='Test Description', body='Test Body')

    assert post.slug == 'complex-title-with-special-characters'


def test_repr_method():
    post = PostEntity(title='Test Repr')
    post.create_a_new_post(description='Test Description', body='Test Body')
    assert (
        repr(post)
        == f'<PostEntity(id={post.id}, title=Test Repr, status=draft)>'
    )
    post.publish()
    assert (
        repr(post)
        == f'<PostEntity(id={post.id}, title=Test Repr, status=published)>'
    )
