from threading import Thread

from colorama import Fore

from common.request_reply import events
from common.request_reply.proxies import BaseServerProxyPublisher, BaseServerProxySubscriber
from common.event_channels import choices
from common.event_channels.event_buses import EventService
from common.event_channels.events import EventMapper
from common.message_marshaller.marshaller import MessageMarshaller
from common.message_marshaller.messages import BrokerMessage, BaseMessage, MetaMessage
from common.registry import Address, Registry
from common.request_reply.replier import Replier
from common.request_reply.requestor import request
from common.settings import BROKER_ADDRESS


class BaseWebHandler(Thread):
    marshaller = MessageMarshaller()

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.run_while = True

        self.event_mapper = EventMapper()
        self.replier, self.current_addr = Replier.get_current_local_host_replier()

    def run(self):
        self.run_while = True

        while self.run_while:
            self.replier.get_message_and_reply(self._reply_handler)

    def _reply_handler(self, byte_message):
        message = self.marshaller.unmarshal(byte_message, self.event_mapper)

        response = self.process_message_handler(message)

        return response

    def process_message_handler(self, message: BaseMessage) -> bytes:
        """
            Process your message here and return a bytes_message
        """
        return b'OK'

    def listen(self):
        self.start()

    def stop(self):
        self.run_while = False

    def request(self, address_key, message: BaseMessage):
        addr = self.get_address(address_key)
        byte_message = BaseWebHandler.marshaller.marshal(message)

        return request(addr, byte_message)

    def get_address(self, requested_address_key) -> Address:
        """
            Get your address here.
        """
        return self.current_addr


class EventWebHandler(BaseWebHandler):
    proxy_publisher_class = BaseServerProxyPublisher
    proxy_subscriber_class = BaseServerProxySubscriber

    def __init__(self, name):
        super().__init__(name)
        self.event_bus = EventService()

    def process_message_handler(self, message: MetaMessage):

        if message.pubsub == choices.PUBLISH:
            proxy = self.proxy_publisher_class(self.event_bus)
            proxy.publish(message.event, message)
        elif message.pubsub == choices.SUBSCRIBE:
            proxy = self.proxy_subscriber_class(message.address_key, self, self.event_bus)
            proxy.subscribe(message.event)
        elif message.pubsub == choices.UNSUBSCRIBE:
            proxy = self.proxy_subscriber_class(message.address_key, self, self.event_bus)
            proxy.unsubscribe(message.event)
        elif not message.pubsub == choices.INFORM:
            raise Exception('Incorrect pubsub protocol.')

        return b'OK'

    def get_address(self, requested_address_key):
        msg = BrokerMessage(self.current_addr, events.REQUEST_ADDRESS, self.name, requested_address_key)
        msg = self.marshaller.marshal(msg)

        addr_response = request(BROKER_ADDRESS, msg)

        addr = self.marshaller.unmarshal(addr_response, self.event_mapper)
        addr = addr.addr

        return addr

    def persist_address(self):
        msg = BrokerMessage(self.current_addr, events.PERSIST_ADDRESS, self.name, 'x')
        msg = self.marshaller.marshal(msg)

        addr_response = request(BROKER_ADDRESS, msg)
        print(Fore.RED + f'persist_address: {addr_response}')

    def get_broker_registry(self):
        msg = BrokerMessage(self.current_addr, events.GET_REGISTRY, self.name, 'x')
        msg = self.marshaller.marshal(msg)

        addr_response = request(BROKER_ADDRESS, msg)
        return addr_response

    def create_meta_message(self, event, pubsub) -> MetaMessage:
        return MetaMessage(self.current_addr,
                           event,
                           pubsub,
                           self.name
                           )


class Broker(BaseWebHandler):
    def __init__(self):
        super().__init__('broker')
        self.registry = Registry()

    def process_message_handler(self, message: BrokerMessage):
        self._persist_address(message)

        request_address_key = message.requested_address_key
        addr = self.registry.get(request_address_key)

        if isinstance(message.event, self.event_mapper.get_event_class(events.PERSIST_ADDRESS)):
            return b'Address persisted'

        if isinstance(message.event, self.event_mapper.get_event_class(events.GET_REGISTRY)):
            registry_keys = self.registry.keys()
            return str(registry_keys).encode('utf-8')

        if addr is None:
            msg = BaseMessage(message.addr, events.NOT_FOUND_ADDRESS)
        else:
            msg = BaseMessage(addr, events.GET_ADDRESS)

        msg = self.marshaller.marshal(msg)

        return msg

    def _persist_address(self, message: BrokerMessage):
        self.registry.put(message.address_key, message.addr)

    def get_address(self, requested_address_key):
        return self.registry.get(requested_address_key)
