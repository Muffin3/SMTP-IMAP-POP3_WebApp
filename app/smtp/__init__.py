from flask import Blueprint

smtp_blueprint = Blueprint('smtp', __name__, template_folder='templates')

from . import views
