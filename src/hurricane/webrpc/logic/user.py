import hurricane.config.db_config
import hurricane.db.api.user
import hurricane.utils.logic

db_client = config.db_config.get_client()


def get_user(user_id):
    db_filter = hurricane.utils.logic.SingleExpression('user_id', user_id, hurricane.utils.logic.Comparator.EQ)
    return hurricane.db.api.user.get_user(db_client, db_filter)


def create_user(name, email, password, bio=''):
    data = {'email': email, 'name': name, 'password': password, 'bio': bio}
    return hurricane.db.api.user.create_user(db_client, data)
