import falcon
from sqlalchemy import create_engine

from yafas import orm

from .auth import models  # noqa


class YafasApp:

    def __init__(self, config: dict):
        self.config = config

        self.api = falcon.API(middleware=self.middlewares())

        self.init_resources()

        self.init_db()

    def init_db(self):
        self.engine = create_engine(
            self.config.get('DATABASE_URI', 'sqlite:///yafas.db'))

        orm.db.session.configure(bind=self.engine)
        orm.db.Base.metadata.create_all(self.engine)

    def init_resources(self):
        for uri, resource in self.resources():
            self.api.add_route(uri, resource)

    def resources(self) -> []:
        return []

    def middlewares(self) -> []:
        return [
            orm.SQLAlchemySessionMiddleware(),
        ]
