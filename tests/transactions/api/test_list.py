URL = '/api/v1/transactions/'


def test_list(client, factory):
    user = factory.user()
    factory.cycle(5).transaction(user_id=user.id)

    got = client.get(URL, user=user)

    assert len(got) == 5


def test_has_required_fields(client, factory):
    user = factory.user()
    factory.cycle(5).transaction(user_id=user.id)

    got = client.get(URL, user=user)

    for field in ('id', 'created_at', 'value'):
        for el in got:
            assert field in el


def test_list_for_current_user_only(client, user_and_transaction):
    user0, transaction0 = user_and_transaction()
    user1, transaction1 = user_and_transaction()

    got = client.get(URL, user=user1)

    assert len(got) == 1
    assert got[0]['id'] == transaction1.id
