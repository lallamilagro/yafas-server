import falcon
from sqlalchemy import create_engine

from yafas import config, db, orm

from .auth import models  # noqa


class YafasApp:

    def __init__(self):
        self.api = falcon.API(middleware=self.middlewares())

        self.init_resources()

        self.init_db()

    def init_db(self):
        self.engine = create_engine(
            config.get('DATABASE_URI', 'sqlite:///yafas.db'))

        db.session.configure(bind=self.engine)
        db.Base.metadata.create_all(self.engine)

    def init_resources(self):
        for uri, resource in self.resources():
            self.api.add_route(uri, resource)

    def resources(self) -> []:
        return []

    def middlewares(self) -> []:
        return [
            orm.SQLAlchemySessionMiddleware(),
        ]
