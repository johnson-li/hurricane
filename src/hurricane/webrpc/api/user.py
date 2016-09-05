def get_user(client, user_id):
    user_id = int(user_id)
    return client.get_user(user_id=user_id)


def create_user(client, name, email, password, bio=''):
    return client.create_user(name=name, email=email, password=password, bio=bio)


def update_user(client, user_id, name=None, email=None, password=None, bio=None):
    return client.update_user(user_id=user_id, name=name, password=password, bio=bio)
