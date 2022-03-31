from flask import Flask, render_template, make_response, jsonify
from random import sample
from flask_restful import Api
from data.chat_resources import MessageResources
from data.chats import Chats
from data import db_session
from requests import get

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/chats/<link>')
def chats(link):
    session = db_session.create_session()
    chat = session.query(Chats).filter(Chats.link == link)
    messages = get(f'http://127.0.0.1:5000/api/messages/{str(chat[0].id)}').json()
    list_msg = []
    for elem in messages['messages']:
        list_msg.append(elem['message'])
    return render_template('chat.html', list_msg=list_msg)


def main():
    db_session.global_init("db/chats.db")
    api.add_resource(MessageResources, '/api/messages/<int:chat_id>')
    app.run()


if __name__ == '__main__':
    main()