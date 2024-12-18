from typing import NoReturn

import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file: str) -> NoReturn:
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Need to write file of bd")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sa.create_engine(conn_str, echo=False)
    __factory = engine

    import data.__all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return Session(__factory)
