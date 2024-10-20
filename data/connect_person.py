import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class ConnectPerson(SqlAlchemyBase):
    __tablename__ = 'connect_person'

    id_first = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_second = sqlalchemy.Column(sqlalchemy.Integer)
    type = sqlalchemy.Column(sqlalchemy.String)
