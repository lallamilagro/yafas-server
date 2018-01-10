from flask import Blueprint

from .resources import Registration

bp = Blueprint('beta', __name__)

registration = Registration.as_view('registration')
bp.add_url_rule('/register/', view_func=registration, methods=['POST'])
