import httplib
from functools import partial

from hurricane.codec import get_parser
from hurricane.config import conf
from hurricane.logging import get_logger

logger = get_logger(__name__)


def get_conn():
    return httplib.HTTPConnection("localhost:5000")


parser = get_parser(conf['webrpc'].get('codec', 'msgpack'))


def call(function_name, *args, **kwargs):
    parameter = {'func_name': function_name, 'args': args, 'kwargs': kwargs}
    conn = get_conn()
    conn.request('POST', '/', parser.encode(parameter))
    response = conn.getresponse()
    data = response.read()
    logger.info(data)

    return parser.decode(data)


class Client(object):
    def __getattr__(self, item):
        return partial(call, function_name=item)
