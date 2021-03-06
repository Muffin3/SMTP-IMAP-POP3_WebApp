from flask import Flask
from config import Configuration
from .imap import imap_blueprint as imap
from .pop3 import pop3_blueprint as pop3
from .smtp import smtp_blueprint as smtp
from .authentication import auth_blueprint as auth


app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(imap, url_prefix='/imap')
app.register_blueprint(pop3, url_prefix='/pop3')
app.register_blueprint(smtp, url_prefix='/smtp')
app.register_blueprint(auth, url_prefix='/auth')

from . import view
