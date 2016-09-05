def get_user(client, db_filter):
    return client.get(table='user', db_filter=db_filter, unique=True)


def update_user(client, update_data, db_filter=None):
    return client.update(table='user', update_data=update_data, db_filter=db_filter)


def create_user(client, insert_data):
    return {'user_id': client.create(table='user', update_data=insert_data)}
