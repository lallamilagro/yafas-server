from dotenv_config import Config

from yafas import YafasApp, db

conf_loader = Config()
config = dict(
    ERROR_404_HELP=False,
    JWT_SECRET_KEY=conf_loader('JWT_SECRET_KEY'),
    MIGRATIONS_DIR='yafas/migrations/',
    SECRET_KEY=conf_loader('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=conf_loader(
        'DATABASE_URI', default='sqlite:///try-flask.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

app = YafasApp(__name__, config=config)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)
