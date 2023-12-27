from typing import Generator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import config

##############################################
# BLOCK FOR COMMON INTERACTION WITH DATABASE #
##############################################

# create async engine for interaction with database
# engine = create_async_engine(config.REAL_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False,
#                             autoflush=False, bind=engine)

engine = create_async_engine(
    config.REAL_DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)


# create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False,
                             class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
