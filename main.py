from flask import Flask, render_template, make_response, jsonify, redirect
from random import sample
from flask_restful import Api
from forms.main_form import MainForm
from data.chat_resources import MessageResources
from data.chats import Chats
from data import db_session
from requests import get

app = Flask(__name__)
app.secret_key = 'anonim'
api = Api(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        link = random_link()
        session = db_session.create_session()
        chat = Chats()
        chat.link = link
        session.add(chat)
        session.commit()
        return redirect(f'/chats/{link}')
    return render_template('index.html', form=form, title='Создание чата')


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
    return render_template('chat.html', list_msg=list_msg, title='Чат инкогнито')


def random_link():
    session = db_session.create_session()
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


def main():
    db_session.global_init("db/chats.db")
    api.add_resource(MessageResources, '/api/messages/<int:chat_id>')
    app.run()


if __name__ == '__main__':
    main()