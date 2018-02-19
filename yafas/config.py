import datetime

from dotenv_config import Config

load = Config()

config = {
    'BCRYPT_ROUNDS': load('BCRYPT_ROUNDS', int),
    'ACCESS_TOKEN_EXPIRES': datetime.timedelta(minutes=15),
    'REFRESH_TOKEN_EXPIRES': datetime.timedelta(days=30),
    'SECRET_KEY': load('SECRET_KEY'),
}
