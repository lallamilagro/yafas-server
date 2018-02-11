import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


def base_model_factory(session):
    class BaseModel:

        id = sa.Column(sa.Integer, primary_key=True)

        query = session.query_property()

    return BaseModel


class db:
    # TODO: write base class with `query` property and primary_key

    session = scoped_session(sessionmaker())

    Base = declarative_base(cls=base_model_factory(session))


class SQLAlchemySessionMiddleware:

    def process_resource(self, req, res, resource, params):
        resource.session = db.session()

    def process_response(self, req, res, resource, req_succeeded):
        if hasattr(resource, 'session'):
            if not req_succeeded:
                resource.session.rollback()
            db.session.remove()
