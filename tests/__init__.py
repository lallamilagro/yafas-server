from sqlalchemy import event
from sqlalchemy.engine import Engine

from tests.test_tools.factory import Factory

__all__ = [
    'Factory',
]


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
