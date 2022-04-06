from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm.session import sessionmaker, Session


class Database:
    _session_class = None

    @classmethod
    def create_connection(cls, db_url: str):
        e = create_engine(db_url)
        cls.create_session_class(e)

    @classmethod
    def create_session_class(cls, engine: Engine):
        cls._session_class = sessionmaker(engine)

    @classmethod
    def get_session(cls) -> Session:
        s = cls._session_class()
        try:
            yield s
        finally:
            s.close()
