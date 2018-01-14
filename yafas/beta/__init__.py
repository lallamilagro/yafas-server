from flask import Blueprint

bp = Blueprint('beta', __name__)

from . import resources  # noqa  # isort:skip
