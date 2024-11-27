from uuid import uuid4

import pytest

from domain.src.author_entity import AuthorEntity


@pytest.fixture
def author_entity():
    return AuthorEntity(
        id=str(uuid4()),
        firstname='John',
        lastname='Doe',
        description='A passionate writer.',
        resume='Experienced in creative writing.',
    )


def test_author_creation():
    author = AuthorEntity(
        firstname='Jane',
        lastname='Smith',
        description='A tech writer.',
        resume='Writes about software development.',
    )

    assert author.firstname == 'Jane'
    assert author.lastname == 'Smith'
    assert author.description == 'A tech writer.'
    assert author.resume == 'Writes about software development.'
    assert isinstance(author.id, str)


def test_missing_firstname():
    with pytest.raises(ValueError, match='Firstname is required.'):
        AuthorEntity(firstname='', lastname='Doe')


def test_missing_lastname():
    with pytest.raises(ValueError, match='Lastname is required.'):
        AuthorEntity(firstname='John', lastname='')


def test_update_author_data(author_entity):
    author_entity.update_author_data(
        firstname='James',
        lastname='Bond',
        description='A secret agent.',
        resume='Highly skilled in espionage.',
    )

    assert author_entity.firstname == 'James'
    assert author_entity.lastname == 'Bond'
    assert author_entity.description == 'A secret agent.'
    assert author_entity.resume == 'Highly skilled in espionage.'


def test_author_id(author_entity):
    assert isinstance(author_entity.id, str)


def test_author_firstname(author_entity):
    assert author_entity.firstname == 'John'


def test_author_lastname(author_entity):
    assert author_entity.lastname == 'Doe'


def test_author_description(author_entity):
    assert author_entity.description == 'A passionate writer.'


def test_author_resume(author_entity):
    assert author_entity.resume == 'Experienced in creative writing.'


def test_author_repr(author_entity):
    expected_repr = f'<AuthorEntity(id={author_entity.id}, name=John Doe)>'
    assert repr(author_entity) == expected_repr
