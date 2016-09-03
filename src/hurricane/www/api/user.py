def ping(client):
    return client.ping()


def login(client, user_id, password):
    return client.login(user_id=user_id, password=password)
