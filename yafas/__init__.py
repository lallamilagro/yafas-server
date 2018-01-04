from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class YafasApp(Flask):

    def __init__(self, import_name: str, config: dict, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)

        self.config.update(config)
        self.init_db()
        self.init_migrations()

    def init_db(self):
        db.init_app(self)

    def init_migrations(self) -> Migrate:
        return Migrate(self, db, directory=self.config.get('MIGRATIONS_DIR'))
