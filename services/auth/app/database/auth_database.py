from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from services.auth.app.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=NullPool)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

Base = declarative_base()

async def get_database():
    db = sessionLocal()
    try:
        yield await db
    finally:
        await db.close()