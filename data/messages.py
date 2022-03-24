import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Messages(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    message = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chat_id =sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("chats.id"), nullable=True)