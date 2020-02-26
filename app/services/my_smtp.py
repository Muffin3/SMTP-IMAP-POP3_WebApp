from email.message import EmailMessage
import smtplib
import socket


class MySMTP:
    def __init__(self, address, password):
        self.address = address
        self.password = password
        self.server_name = 'smtp.' + self.address[self.address.find('@') + 1:]
        self.errors = None

    def send(self, mail_form):
        msg = EmailMessage()
        msg['To'], msg['From'], msg['Subject'] = mail_form.to.data, self.address, mail_form.subject.data
        msg.set_content(mail_form.mail_body.data)
        for file in mail_form.attachments.data:
            msg.add_attachment(file.read(), maintype='application', subtype='octet-stream', filename=file.filename)
        try:
            with smtplib.SMTP_SSL(self.server_name, 465) as smtp:
                smtp.login(self.address, self.password)
                smtp.send_message(msg)
                return True
        except smtplib.SMTPAuthenticationError:
            self.errors = ('Авторизация невозможна! Логин или пароль некорректны!',)
        except socket.gaierror:
            self.errors = ('Включите пожалуйста интернет!',)
