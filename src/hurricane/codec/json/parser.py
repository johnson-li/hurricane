import json


class Parser(object):
    def encode(self, m):
        return json.dumps(m)

    def decode(self, c):
        return json.loads(c)
