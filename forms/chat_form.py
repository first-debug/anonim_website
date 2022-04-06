from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    text = StringField('Type message', validators=[DataRequired()])
    submit = SubmitField('send')
