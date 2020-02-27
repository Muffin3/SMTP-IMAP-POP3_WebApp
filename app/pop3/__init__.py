from flask import Blueprint


pop3_blueprint = Blueprint('pop3', __name__, template_folder='templates')

from . import views
