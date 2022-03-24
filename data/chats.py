import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Chats(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=True)