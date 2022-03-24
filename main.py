from flask import Flask

from data import db_session

app = Flask(__name__)


@app.route('/')
def index():
    return "Привет, Аноним!"


def main():
    app.run()
    db_session.global_init("db/chats.db")


if __name__ == '__main__':
    main()