from flask import request
from flask_jwt_extended import jwt_refresh_token_required

from . import bp, jwt, schemas
from .models import User


@jwt.invalid_token_loader
def invalid_token(reason):
    return {'message': [reason]}, 422


@jwt.expired_token_loader
def token_expired():
    return {'message': ['Token has expired.']}, 401


@bp.route('/check-email/<email>/', methods=['GET'])
def check_email(email: str):
    _, errors = schemas.EmailSchema().load({'email': email})
    return (errors, 400) if errors else ({}, 200)


@bp.route('/login/', methods=['POST'])
def login():
    tokens, errors = schemas.LoginSchema().load(request.json)
    return (errors, 400) if errors else (tokens, 201)


@bp.route('/register/', methods=['POST'])
def register():
    _, errors = schemas.RegistrationSchema().load(request.json)
    return (errors, 400) if errors else ({}, 201)


@bp.route('/refresh/', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    user = User.jwt_retrieve()
    return {
        'access_token': user.create_access_token(),
        'refresh_token': user.create_refresh_token(),
    }, 201
