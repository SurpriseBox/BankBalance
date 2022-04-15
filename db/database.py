import typing as t
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm.session import sessionmaker


class Database:
    _session_class: t.Type[AsyncSession] = None
    _engine: AsyncEngine = None

    @classmethod
    def create_connection(cls, db_url: str):
        """
        Creates DB engine and stores it in this class.

        :param db_url:
        :return:
        """
        cls._engine = create_async_engine(db_url)
        cls._session_class = sessionmaker(cls._engine, class_=AsyncSession, expire_on_commit=False)

    @classmethod
    async def get_session(cls) -> AsyncSession:
        """
        Yields DB session.

        :return:
        """
        async with cls._session_class() as session:
            yield session

    @classmethod
    @asynccontextmanager
    async def get_session_manager(cls) -> AsyncSession:
        """
        Yields DB session that can be used in async context manager.

        :return:
        """
        async with cls._session_class() as session:
            yield session
