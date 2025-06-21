from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import DB_NAME, DB_HOST, DB_PASS, DB_USER, DB_PORT

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
