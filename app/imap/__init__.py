from flask import Blueprint


imap_blueprint = Blueprint('imap', __name__, template_folder='templates', static_folder='static')

from . import views
