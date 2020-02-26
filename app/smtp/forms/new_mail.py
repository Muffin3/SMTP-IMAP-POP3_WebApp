from flask_wtf import FlaskForm
from wtforms import MultipleFileField, TextAreaField, validators, StringField, SubmitField


class NewMail(FlaskForm):
    to = StringField(validators=[validators.DataRequired(), validators.Email(message='Неверный адрес почты!')],
                     render_kw={'placeholder': 'Введите email получателя', 'required': '',
                                'multiple': '', 'type': 'email'})
    subject = StringField(validators=[validators.Optional()], render_kw={'placeholder': 'Введите тему сообщения'})
    mail_body = TextAreaField(validators=[validators.Optional()], render_kw={'placeholder': 'Туть Ваше сообщенько...',
                                                                             'rows': '20', 'cols': '80'})
    attachments = MultipleFileField(render_kw={'data-multiple-caption': '{count} файла выбрано!',
                                               'class': 'file', 'multiple': ''})
    submit = SubmitField(label='Отправить', render_kw={'class': 'submit'})
