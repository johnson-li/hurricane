def get_user(client, db_filter):
    return client.db_func_get_user(db_filter)


def update_user(client, update_data, db_filter=None):
    return client.db_func_update_user(update_data, db_filter)


def create_user(client, insert_data):
    return {'user_id': client.db_func_create_user(insert_data)}
