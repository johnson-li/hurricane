import hurricane.config.webrpc_config
import hurricane.utils.exceptions
import hurricane.webrpc.api.user

webrpc_client = hurricane.config.webrpc_config.get_client()


def ping():
    return 'pang'


def login(user_id, password):
    user = hurricane.webrpc.api.user.get_user(webrpc_client, user_id=user_id)[0]
    print user
    if not user:
        raise hurricane.utils.exceptions.UserNotFoundException()
    if user['password'] != password:
        raise hurricane.utils.exceptions.InvalidPasswordException()
    return user
