import time
import unittest
from multiprocessing import Process

import hurricane.webrpc.api.user
import hurricane.webrpc.impl.flask.client
import hurricane.webrpc.impl.flask.server
import hurricane.webrpc.impl.gevent.client
import hurricane.webrpc.impl.gevent.server


def server_thread():
    hurricane.webrpc.impl.flask.server.run()


def gevent_server_thread():
    hurricane.webrpc.impl.gevent.server.run()


class TestFlaskWebrpc(unittest.TestCase):
    def __init__(self, method_name='runTest'):
        super(TestFlaskWebrpc, self).__init__(method_name)
        self.client = hurricane.webrpc.impl.flask.client.Client()
        self.gevent_client = hurricane.webrpc.impl.gevent.client.Client()

    def testConnection(self):
        process = Process(target=server_thread)
        process.start()
        time.sleep(0.5)
        info = hurricane.webrpc.api.user.create_user(self.client, 'johnson', '1@j.com', 'password')
        user = hurricane.webrpc.api.user.get_user(self.client, info['user_id'])
        self.assertEqual(user['name'], 'johnson')
        process.terminate()

    def testGevent(self):
        process = Process(target=gevent_server_thread)
        process.start()
        time.sleep(0.5)
        info = hurricane.webrpc.api.user.create_user(self.gevent_client, 'johnson', '1@j.com', 'password')
        user = hurricane.webrpc.api.user.get_user(self.client, info['user_id'])
        self.assertEqual(user['name'], 'johnson')
        process.terminate()
