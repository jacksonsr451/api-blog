from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.config.settings import settings

engine = create_async_engine(settings.POSTGRES_URL, echo=True)

async_session_factory = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
    async with async_session_factory() as session:
        yield session


session: AsyncSession = get_session()
