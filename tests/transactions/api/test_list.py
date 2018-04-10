def test_list(client, factory, url):
    user = factory.user()
    factory.cycle(5).transaction(user_id=user.id)

    got = client.get(url(), user=user)

    assert len(got) == 5


def test_has_required_fields(client, factory, url):
    user = factory.user()
    factory.cycle(5).transaction(user_id=user.id)

    got = client.get(url(), user=user)

    for field in ('id', 'on_date', 'value'):
        for el in got:
            assert field in el


def test_list_for_current_user_only(client, url, user_and_transaction):
    user0, transaction0 = user_and_transaction()
    user1, transaction1 = user_and_transaction()

    got = client.get(url(), user=user1)

    assert len(got) == 1
    assert got[0]['id'] == transaction1.id
