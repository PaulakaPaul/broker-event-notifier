class Address:
    def __init__(self, _id, _port):
        self._id = _id
        self._port = _port

    @property
    def id(self):
        return self._id

    @property
    def port(self):
        return self._port

    def __str__(self):
        return f'({self.id},{self.port})'
