from raven import Client
from raven.middleware import Sentry

from yafas import config
from yafas.app import YafasApp

app = YafasApp()

SENTRY_DSN = config['SENTRY_DSN']

api = Sentry(app.api, Client(SENTRY_DSN)) if SENTRY_DSN else app.api
