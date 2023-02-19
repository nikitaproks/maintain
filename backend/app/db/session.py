from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # noqa

DATABASE_URL = "postgresql://myuser:password@localhost/fastapi_database"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


test_engine = create_engine(
    f"{settings.SQLALCHEMY_DATABASE_URI}_test", pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)
