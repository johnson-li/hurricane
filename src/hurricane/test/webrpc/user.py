import unittest

import hurricane.webrpc.api.user
import hurricane.webrpc.impl.local.client


class TestUserLogic(unittest.TestCase):
    def __init__(self, method_name='runTest'):
        super(TestUserLogic, self).__init__(method_name)
        self.client = hurricane.webrpc.impl.local.client.Client()

    def test_user(self):
        info = hurricane.webrpc.api.user.create_user(self.client, 'johnson', '1@j.com', 'password')
        user = hurricane.webrpc.api.user.get_user(self.client, info['user_id'])[0]
        self.assertEqual(user['name'], 'johnson')
