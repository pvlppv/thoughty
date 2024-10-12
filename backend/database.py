from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import get_settings


cfg = get_settings()

print(f"Connecting to database with URL: {cfg.database_url}")

engine = create_engine(
    cfg.database_url,
    pool_size=20,
    max_overflow=30,
    client_encoding='utf8',
    connect_args={"options": "-c timezone=Europe/Moscow"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
