from flask_wtf import FlaskForm
from wtforms import SubmitField


class MainForm(FlaskForm):
    submit = SubmitField('Создать чат')