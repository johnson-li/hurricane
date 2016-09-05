import functools
import inspect
import json

from flask import Flask, request

import hurricane.www.logic.user

app = Flask(__name__)

WWW_MODULES = [hurricane.www.logic.user]


def wrapper(func):
    @functools.wraps(func)
    def wrapped():
        args = {}
        args.update({key: val for key, val in request.args.iteritems()})
        if request.data:
            args.update(json.loads(request.data))
        res = func(**args)
        if isinstance(res, dict):
            return json.dumps(res)
        return 'Unknown response type: ' + type(res)

    return wrapped


def init_app():
    for module in WWW_MODULES:
        module_name = module.__name__.split('.')[-1]
        for func_name in [para_name for para_name in dir(module) if not para_name.startswith('_')]:
            func = getattr(module, func_name)
            if inspect.isfunction(func):
                app.route('/api/{}/{}'.format(module_name, func_name), methods=['GET'])(wrapper(func))


def run():
    init_app()
    app.run()


if __name__ == '__main__':
    run()
