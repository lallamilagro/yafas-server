from .auth import resources as auth_resources

routes = (
    ('auth/check-email/{email}', auth_resources.CheckEmail()),
    ('auth/register', auth_resources.Register()),
    ('auth/login', auth_resources.Login()),
    ('auth/info', auth_resources.Info()),
)
