from gevent import monkey

monkey.patch_all()

import inspect

from flask import Flask, request

import hurricane.webrpc.logic.user
from hurricane.codec import get_parser
from hurricane.config import conf
from hurricane.logging import get_logger
from gevent import wsgi

app = Flask(__name__)
logger = get_logger(__name__)

WEBRPC_MODULES = [hurricane.webrpc.logic.user]

FUNC_MAP = {}

parser = get_parser(conf['webrpc'].get('codec', 'msgpack'))


def init_app():
    for module in WEBRPC_MODULES:
        for func_name in [para_name for para_name in dir(module) if not para_name.startswith('_')]:
            func = getattr(module, func_name)
            if inspect.isfunction(func):
                FUNC_MAP[func_name] = func
    logger.info(FUNC_MAP)
    app.route('/', methods=['POST'])(handler)


def handler():
    parameter = parser.decode(request.data)
    logger.info(parameter)
    func_name = parameter['func_name']
    func = FUNC_MAP[func_name]
    return parser.encode(func(*parameter['args'], **parameter['kwargs']))


def run():
    init_app()
    server = wsgi.WSGIServer(('localhost', 5000), app)
    server.serve_forever()


if __name__ == '__main__':
    run()
