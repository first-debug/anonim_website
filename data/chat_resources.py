from flask_restful import Resource, abort
from flask import jsonify
from . import db_session
from .messages import Messages
from sqlalchemy import insert


def get_message_or_abort(chat_id):
    session = db_session.create_session()
    chat = session.query(Messages).filter(Messages.chat_id == chat_id)
    if not chat:
        abort(404, message=f"Message {chat_id} not found")
    return chat, session


class MessageResources(Resource):
    def get(self, chat_id):
        chat, session = get_message_or_abort(chat_id)
        return jsonify({'messages': [item.to_dict(
            only=('id', 'message')) for item in chat]})

    def delete(self, message_id):
        chat, session = get_message_or_abort(message_id)
        session.delete(chat)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self, chat_id, message):
        session = db_session.create_session()
        last_id = session.query(Messages).filter(chat_id).last()
        new_data = (insert(Messages).values(id=str(last_id + 1), message=message, chat_id=chat_id))
        print(new_data)
        session.commit()


