import importlib

import hurricane.config

webrpc_conf = hurricane.config.conf.get('webrpc', None)


def get_client():
    module_str = webrpc_conf['client_module']
    class_str = webrpc_conf['client_class']

    if not module_str.startswith('hurricane.webrpc.impl.'):
        raise AttributeError('webrpc client should be located in hurricane.webrpc.impl: ' + module_str)

    module = importlib.import_module(module_str)
    cls = getattr(module, class_str)
    return cls()
