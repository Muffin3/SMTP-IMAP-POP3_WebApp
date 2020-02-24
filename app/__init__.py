from flask import Flask
from config import Configuration
from .imap import imap_blueprint as imap
from .authentication import auth_blueprint as auth


app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(imap, url_prefix='/imap')
app.register_blueprint(auth, url_prefix='/auth')

from . import view
