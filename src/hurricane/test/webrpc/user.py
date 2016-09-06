import unittest

import hurricane.webrpc.api.user
import hurricane.webrpc.impl.flask.client
import hurricane.webrpc.impl.flask.server
import hurricane.webrpc.impl.local.client


class TestUserLogic(unittest.TestCase):
    def __init__(self, method_name='runTest'):
        super(TestUserLogic, self).__init__(method_name)
        self.client = hurricane.webrpc.impl.local.client.Client()

    def test_user(self):
        info = hurricane.webrpc.api.user.create_user(self.client, 'johnson', '1@j.com', 'password')
        user = hurricane.webrpc.api.user.get_user(self.client, info['user_id'])
        self.assertEqual(user['name'], 'johnson')

    def test_update_user(self):
        info = hurricane.webrpc.api.user.create_user(self.client, 'johnson', '2@j.com', 'password')
        hurricane.webrpc.api.user.update_user(self.client, info['user_id'], name='haha')
        user = hurricane.webrpc.api.user.get_user(self.client, info['user_id'])
        self.assertEqual('haha', user['name'])
