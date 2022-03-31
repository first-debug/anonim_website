from flask_restful import Resource, abort
from flask import jsonify
from . import db_session
from .messages import Messages


def get_message_or_abort(chat_id):
    session = db_session.create_session()
    chat = session.query(Messages).filter(Messages.chat_id == chat_id)
    if not chat:
        abort(404, message=f"Message {chat_id} not found")
    print(chat)
    return chat, session


class MessageResources(Resource):
    def get(self, chat_id):
        chat, session = get_message_or_abort(chat_id)
        return jsonify({'messsage': [item.to_dict(
            only=('id', 'message')) for item in chat]})

    def delete(self, chat_id):
        chat, session = get_message_or_abort(chat_id)
        session.delete(chat)
        session.commit()
        return jsonify({'success': 'OK'})