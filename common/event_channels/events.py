from multiprocessing import Lock


class Event:
    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__


class EventMapper:
    def __init__(self):
        self.events = dict()
        self.lock = Lock()

    def get_event_class(self, event_name):
        try:
            self.lock.acquire(True)

            return self.events[event_name]
        except KeyError:
            event_class = type(event_name, (Event, ), {})
            self.events[event_name] = event_class
            return self.events[event_name]
        finally:
            self.lock.release()

    def add_event(self, event_name, event_class):
        try:
            self.lock.acquire(True)

            self.events[event_name] = event_class
        finally:
            self.lock.release()


class AggregateEvent:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self):
        EventMapper.add_event(self.cls.__name__, self.cls)
