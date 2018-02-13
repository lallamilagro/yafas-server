def cors_callback(client, response):
    assert response.headers.get('Access-Control-Allow-Origin') == '*'
    for required_header in ('CONTENT-TYPE', 'Authorization'):
        assert required_header in response.headers.get(
            'Access-Control-Allow-Headers')
