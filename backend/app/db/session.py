from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # noqa


def get_url():
    from app.core.config import settings

    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    host = settings.POSTGRES_HOST
    port = settings.POSTGRES_PORT
    db = (
        settings.POSTGRES_DB
        if settings.ENVIRONMENT in ["prod", "dev"]
        else f"{settings.POSTGRES_DB}_test"
    )

    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


DATABASE_URL = get_url()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


test_engine = create_engine(
    f"{settings.SQLALCHEMY_DATABASE_URI}_test", pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)
