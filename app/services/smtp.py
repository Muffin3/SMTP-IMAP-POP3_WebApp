import smtplib
import socket


class MySMTP:
    def __init__(self, mail, password):
        self.mail = mail
        self.password = password
        self.errors = None

    def check_mailbox(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login(self.mail, self.password)
            server.quit()
            return True
        except smtplib.SMTPAuthenticationError as e:
            self.errors = (self.get_error(e.args[0]),)
        except socket.gaierror:
            self.errors = ('Включите пожалуйста интернет!',)
        except UnicodeEncodeError:
            self.errors = ('Пароль и адрес почты должен содержать только цифры и буквы латинского алфавита!',)

    @staticmethod
    def get_error(code):
        return {535: 'Авторизация невозможна! Логин или пароль некорректны!'}.get(code)
