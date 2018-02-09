from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


class db:
    Base = declarative_base()

    session = scoped_session(sessionmaker())


class SQLAlchemySessionMiddleware:

    def process_resource(self, req, res, resource, params):
        resource.session = db.session()

    def process_response(self, req, res, resource, req_succeeded):
        if hasattr(resource, 'session'):
            if not req_succeeded:
                resource.session.rollback()
            db.session.remove()
