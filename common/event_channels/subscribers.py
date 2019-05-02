from common.event_channels import choices
from common.event_channels.events import Event
from common.message_marshaller.marshaller import MessageMarshaller
from common.request_reply.requestor import request


class Subscriber:
    def __init__(self, event_bus, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_bus = event_bus

    def subscribe(self, event: Event):
        raise NotImplementedError()

    def unsubscribe(self, event: Event):
        raise NotImplementedError()

    def inform(self, event: Event, obj):
        raise NotImplementedError()


class AddressSubscriber(Subscriber):
    marshaller = MessageMarshaller()

    def __init__(self, event_bus, address_key, web_handler, *args, **kwargs):
        super().__init__(event_bus, *args, **kwargs)
        self._address_key = address_key
        self._web_handler = web_handler

    def subscribe(self, event: Event):
        self.event_bus.subscribe(type(event), self)

    def unsubscribe(self, event: Event):
        self.event_bus.unsubscribe(type(event), self)

    def inform(self, event: Event, message):
        address = self._web_handler.get_address(self._address_key)

        message.pubsub = choices.INFORM
        bytes_message = self.marshaller.marshal(message)

        response = request(address, bytes_message)

        return response

    def __eq__(self, other):
        return isinstance(other, AddressSubscriber) and other.address_key == self.address_key

    def __hash__(self):
        # TODO: find a better hash
        return hash(self.address_key) * 2 + 10

    @property
    def address_key(self):
        return self._address_key
