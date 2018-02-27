import datetime

from dotenv_config import Config

load = Config()

config = {
    'ACCESS_TOKEN_EXPIRES': datetime.timedelta(days=30),
    'ALLOW_ORIGIN': load('ALLOW_ORIGIN', default='https://app.yafas.org'),
    'BCRYPT_ROUNDS': load('BCRYPT_ROUNDS', int),
    'DATABASE_URI': load('DATABASE_URI', default='sqlite:///yafas.db'),
    'SECRET_KEY': load('SECRET_KEY'),
    'SENTRY_DSN': load('YAFAS_SERVER_SENTRY_DSN', default=None),
}
