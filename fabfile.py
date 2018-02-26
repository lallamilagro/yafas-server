from fabric.api import local


def dev():
    local('gunicorn --reload app:api -t 0')
