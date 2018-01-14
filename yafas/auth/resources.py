
from . import bp, schemas


@bp.route('/check-email/<email>/', methods=['GET'])
def check_email(email: str):
    _, errors = schemas.EmailSchema().load({'email': email})
    return (errors, 400) if errors else ({}, 200)
