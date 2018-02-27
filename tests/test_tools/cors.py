def cors_callback(client, response):
    assert response.headers.get('Access-Control-Allow-Origin') == '*'
    assert 'Content-Type' in response.headers['Access-Control-Allow-Headers']
