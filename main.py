from flask import Flask, render_template, make_response, jsonify
from random import sample
from flask_restful import Api
from data.chat_resources import MessageResources

from data import db_session

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/chats.db")
    api.add_resource(MessageResources, '/api/messages/<int:chat_id>')
    app.run()


if __name__ == '__main__':
    main()