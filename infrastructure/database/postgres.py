from sqlmodel import Session, create_engine

from api.config.settings import settings

engine = create_engine(settings.POSTGRES_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


session: Session = get_session()
