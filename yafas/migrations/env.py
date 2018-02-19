import os
import sys
from logging.config import fileConfig

from alembic import context

sys.path.append(os.getcwd())

from yafas.app import YafasApp  # noqa # isort:skip
from yafas import db  # noqa # isort:skip


fileConfig(context.config.config_file_name)

YafasApp()


with db.engine.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=db.Base.metadata,
    )

    with context.begin_transaction():
        context.run_migrations()
