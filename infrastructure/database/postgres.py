from api.config.settings import settings

from sqlmodel import create_engine, Session


engine = create_engine(settings.POSTGRES_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


session: Session = get_session()
