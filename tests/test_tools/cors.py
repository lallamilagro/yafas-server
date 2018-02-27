from yafas import config


def cors_callback(client, response):
    assert response.headers[
        'Access-Control-Allow-Origin'] == config['ALLOW_ORIGIN']
    assert response.headers['Access-Control-Allow-Credentials'] == 'true'
    assert 'Content-Type' in response.headers['Access-Control-Allow-Headers']
