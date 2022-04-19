from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField


class ChatForm(FlaskForm):
    text = StringField('Type message')
    pic = FileField('Изображение')
    submit = SubmitField('Отправить')