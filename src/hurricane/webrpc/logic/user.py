import hurricane.config.db_config
import hurricane.db.api.user
import hurricane.utils.logic

db_client = hurricane.config.db_config.get_client()


def get_user(user_id):
    db_filter = hurricane.utils.logic.SingleExpression('user_id', user_id, hurricane.utils.logic.Comparator.EQ)
    return hurricane.db.api.user.get_user(db_client, db_filter)


def create_user(name, email, password, bio=''):
    data = {'email': email, 'name': name, 'password': password, 'bio': bio}
    return hurricane.db.api.user.create_user(db_client, data)


def update_user(user_id, name=None, email=None, password=None, bio=None):
    data = {}
    if name is not None:
        data['name'] = name
    if email is not None:
        data['email'] = email
    if password is not None:
        data['password'] = password
    if bio is not None:
        data['bio'] = bio
    db_filter = hurricane.utils.logic.SingleExpression('user_id', user_id, hurricane.utils.logic.Comparator.EQ)
    return hurricane.db.api.user.update_user(db_client, data, db_filter=db_filter)
