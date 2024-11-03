import sqlalchemy

from data.db_session import SqlAlchemyBase


class ConnectPerson(SqlAlchemyBase):
    __tablename__ = 'connect_person'

    id_first = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_second = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    type = sqlalchemy.Column(sqlalchemy.String)
