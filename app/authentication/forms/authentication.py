from flask_wtf import FlaskForm
from wtforms import PasswordField, validators, StringField, SubmitField


class Authentication(FlaskForm):
    mailbox = StringField(validators=[validators.DataRequired(), validators.Email(message='Неверный адрес почты!')],
                          render_kw={'class': 'auth-field', 'placeholder': 'адрес почты'})
    password = PasswordField(validators=[validators.DataRequired()],
                             render_kw={'class': 'auth-field', 'placeholder': 'пароль'})
    submit = SubmitField(label='Войти', render_kw={'class': 'auth-btn'})
