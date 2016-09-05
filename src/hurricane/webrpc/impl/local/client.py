import inspect

import hurricane.webrpc.logic.user

func_map = {func.__name__: func for func in
            [getattr(hurricane.webrpc.logic.user, func_name) for func_name in dir(hurricane.webrpc.logic.user) if
             not func_name.startswith('_')] if inspect.isfunction(func)}


class Client(object):
    def __getattr__(self, item):
        func = func_map.get(item, None)
        if func:
            return func
        raise AttributeError('{} object has no attribute {}'.format(self.__class__, item))
