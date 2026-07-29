from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from services.auth.app.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, poolclass=NullPool)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        await db.close()