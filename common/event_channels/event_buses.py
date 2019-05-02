from multiprocessing import Lock

from common.event_channels.events import Event
from common.event_channels.subscribers import Subscriber, AddressSubscriber
from common.message_marshaller.messages import MetaMessage


class EventBus:
    def publish(self, event: Event, obj):
        raise NotImplementedError()

    def subscribe(self, event_type: type, subscriber: Subscriber):
        raise NotImplementedError()

    def unsubscribe(self, event_type: type, subscriber: Subscriber):
        raise NotImplementedError()


class EventService(EventBus):

    def __init__(self):
        self.event_subscribers = set()
        self.lock = Lock()

    def publish(self, event: Event, message: MetaMessage):
        try:
            self.lock.acquire(True)

            for event_type, subscriber in self.event_subscribers:
                if isinstance(event, event_type):
                    subscriber.inform(event, message)

        finally:
            self.lock.release()

    def subscribe(self, event_type, subscriber: AddressSubscriber):
        try:
            self.lock.acquire(True)

            # Make event - subscriber relation.
            t = (event_type, subscriber)
            self.event_subscribers.add(t)
        finally:
            self.lock.release()

    def unsubscribe(self, event_type, subscriber: AddressSubscriber):
        try:
            self.lock.acquire(True)

            # Delete event - subscriber relation.
            t = (event_type, subscriber)
            self.event_subscribers.remove(t)
        finally:
            self.lock.release()
