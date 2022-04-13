from flask import Flask, render_template, make_response, jsonify, redirect, request
from random import sample
from flask_restful import Api

from data.messages import Messages
from forms.chat_form import ChatForm
from forms.main_form import MainForm
from data.chat_resources import MessageResources
from data.chats import Chats
from data import db_session
from requests import get

app = Flask(__name__)
app.secret_key = 'anonim'
api = Api(app)
db_session.global_init("db/chats.db")
session = db_session.create_session()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        link = random_link()
        chat = Chats()
        chat.link = link
        session.add(chat)
        session.commit()
        return redirect(f'/chats/{link}')
    return render_template('index.html', form=form, title='Создание чата')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/chats/<link>', methods=['GET', 'POST'])
def chats(link):
    form = ChatForm()
    chat_id = session.query(Chats).filter(Chats.link == link)[0].id
    list_msg = get_messages(link, chat_id)
    if form.validate_on_submit():
        message_model = Messages()
        message_model.message = form.text.data
        message_model.chat_id = chat_id
        session.add(message_model)
        session.commit()
        form.text.data = ''
        return redirect(f'/chats/{link}')
    return render_template('chat.html', list_msg=list_msg, title='Чат инкогнито', form=form)


# Функция для создания произвольного чата
def random_link():
    chat = session.query(Chats).all()
    s = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'
    while True:
        k = 0
        link = sample(s, 8)
        for elem in chat:
            if elem.link == link:
                k += 1
        if k == 0:
            return ''.join(link)


# Функция для получения сообщений чата
def get_messages(link, chat_id):
    return [elem['message'] for elem in get(f'http://127.0.0.1:8080/api/messages/{str(chat_id)}').json()['messages']]


def main():
    api.add_resource(MessageResources, '/api/messages/<int:chat_id>')
    app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()
