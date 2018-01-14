from flask import request

from . import bp
from .schemas import RegistrationSchema


@bp.route('/register/', methods=['POST'])
def register():
    beta, errors = RegistrationSchema().load(request.json)
    return (errors, 400) if errors else ({}, 201)
