import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite+aiosqlite:///:memory:'

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_factory = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope='function')
def test_engine():
    return engine


@pytest.fixture(scope='function')
async def test_session():
    async with async_session_factory() as session:
        yield session
