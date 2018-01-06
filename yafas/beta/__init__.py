from flask import Blueprint
from flask_restful import Api
from flask_restful.utils import cors

from .resources import Registration

bp = Blueprint('beta', __name__)

api = Api(bp)
api.decorators = [
    cors.crossdomain(
        origin='*', headers=['Content-Type']),
]

api.add_resource(Registration, '/register/')
