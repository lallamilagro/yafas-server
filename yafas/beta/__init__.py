from flask import Blueprint
from flask_restful import Api

from .resources import Registration

bp = Blueprint('beta', __name__)

api = Api(bp)

api.add_resource(Registration, '/register/')
