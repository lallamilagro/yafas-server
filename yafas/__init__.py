import importlib

from flask import Blueprint, Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from yafas.tools import JsonResponse, apply_cors

db = SQLAlchemy()


class YafasApp(Flask):

    response_class = JsonResponse

    blueprint_module_names = (
        'auth',
    )

    def __init__(self, import_name: str, config: dict, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)

        self.config.update(config)

        self.init_db()
        self.init_migrations()

        self.apply_cors()

        self.init_blueprints()

    def init_db(self):
        db.init_app(self)

    def init_migrations(self) -> Migrate:
        return Migrate(self, db, directory=self.config.get('MIGRATIONS_DIR'))

    def init_blueprints(self):
        for bp_name in self.blueprint_module_names:
            self.register_blueprint(
                self._import_blueprint(bp_name),
                url_prefix=f'/api/v1/{bp_name}')

    def _import_blueprint(self, bp_module_name: str) -> Blueprint:
        bp_module = importlib.import_module(f'{__name__}.{bp_module_name}')
        return bp_module.bp

    def apply_cors(self):
        self.after_request(apply_cors)
