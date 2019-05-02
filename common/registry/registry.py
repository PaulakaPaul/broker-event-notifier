from multiprocessing import Lock


class Registry:

    def __init__(self):
        self.entities = dict()
        self.lock = Lock()

    def put(self, key: str, address):
        try:
            self.lock.acquire(True)

            self.entities[key] = address
        finally:
            self.lock.release()

    def get(self, key: str):
        try:
            self.lock.acquire(True)

            return self.entities.get(key)
        finally:
            self.lock.release()

    def keys(self):
        try:
            self.lock.acquire(True)

            return self.entities.keys()
        finally:
            self.lock.release()
