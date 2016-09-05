import hurricane.codec
import importlib


def get_parser(name='json'):
    module = importlib.import_module('hurricane.codec.{}.parser'.format(name))
    return module.Parser()
