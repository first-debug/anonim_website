import os.path
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, make_response, jsonify, redirect, request, url_for
from random import sample
from flask_restful import Api

from data.messages import Messages
from forms.chat_form import ChatForm
from forms.main_form import MainForm
from data.chat_resources import MessageResources
from data.message_del_resource import MessageDelResources
from data.chats import Chats
from data import db_session
from requests import get

app = Flask(__name__)
app.secret_key = 'anonim'
api = Api(app)
db_session.global_init("db/chats.db")
session = db_session.create_session()
IMG_DIRECTORY = 'static/img/'


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
    message_model = Messages()
    chat_id = session.query(Chats).filter(Chats.link == link)[0].id
    list_msg = get_messages(chat_id)
    if form.validate_on_submit():
        message = form.text.data
        file = form.pic.data.read()
        if message == '' and file != b'':
            format = form.pic.data.filename[-4:]
            message_model.message = '/' + IMG_DIRECTORY + save_img(file, format)
            message_model.chat_id = chat_id
            message_model.type = 'img'
            session.add(message_model)
            session.commit()
        if message != '':
            message_model.message = message
            message_model.chat_id = chat_id
            message_model.type = 'msg'
            session.add(message_model)
            session.commit()
        return redirect(f'/chats/{link}')
    return render_template('chat.html', list_msg=list_msg, title='Чат инкогнито', form=form, chat_id=chat_id)


# Функция для создания произвольного чата
def random_link():
    chat = session.query(Chats).all()
    s = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'
    while True:
        k = 0
        link = sample(s, 8)
        for elem in chat:
            if elem.link == link:
                k = 1
                break
        if k == 0:
            return ''.join(link)


# Функция для получения сообщений чата
def get_messages(chat_id):
    return [(elem['message'], elem['type']) for elem in get(f'http://127.0.0.1:8080/api/messages/{chat_id}').json()['messages']]


# Функция для сохранения картинки из формы
def save_img(img_data, format):
    files = []
    for elem in os.listdir(IMG_DIRECTORY):
        if format in elem:
            files.append(elem)
    if len(files) == 0:
        filename = '1' + format
    else:
        filename = str(int(sorted(files)[-1][:-4]) + 1) + format
    with BytesIO(img_data) as img_buf:
        with Image.open(img_buf) as img:
            img.save(f'{IMG_DIRECTORY}{filename}')
            return filename


def main():
    api.add_resource(MessageResources, '/api/messages/<int:chat_id>')
    api.add_resource(MessageDelResources, '/api/message/<int:msg_id>')
    app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()
