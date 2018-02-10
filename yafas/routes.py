from .auth import resources as auth_resources

routes = [
    ('auth/check-email/{email}', auth_resources.CheckEmail()),
]
