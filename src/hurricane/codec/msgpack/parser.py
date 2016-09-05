import msgpack


class Parser:
    def __init__(self):
        pass

    def encode(self, m):
        return msgpack.dumps(m)

    def decode(self, c):
        return msgpack.loads(c)
