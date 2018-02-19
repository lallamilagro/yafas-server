from .auth import resources as auth_resources

routes = (
    ('auth/check-email/{email}', auth_resources.CheckEmail()),
    ('auth/register', auth_resources.Register()),
    ('auth/login', auth_resources.Login()),
    ('auth/refresh', auth_resources.Refresh()),
)
