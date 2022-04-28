from flask_restful import Resource, abort
from flask import jsonify
from . import db_session
from .messages import Messages


def get_message_or_abort(msg_id):
    session = db_session.create_session()
    message = session.query(Messages).get(msg_id)
    if not message:
        abort(404, message=f"Message {msg_id} not found")
    return message, session


class MessageDelResources(Resource):
    def delete(self, msg_id):
        message, session = get_message_or_abort(msg_id)
        session.delete(message)
        session.commit()
        return jsonify({'success': 'OK'})