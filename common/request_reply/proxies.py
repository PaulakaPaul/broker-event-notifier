from colorama import Fore

from common.event_channels import choices
from common.event_channels.events import Event
from common.event_channels.publishers import Publisher
from common.event_channels.subscribers import AddressSubscriber
from common.message_marshaller.messages import MetaMessage


#
# SERVER PROXIES


class BaseServerProxySubscriber:
    def __init__(self, client_key: str, web_handler, event_service):
        self.subscriber = AddressSubscriber(event_service, client_key, web_handler)

    def subscribe(self, event: Event):
        self.subscriber.subscribe(event)

    def unsubscribe(self, event: Event):
        self.subscriber.unsubscribe(event)


class BaseServerProxyPublisher:
    def __init__(self, event_service):
        self.publisher = Publisher(event_service)

    def publish(self, event: Event, message: MetaMessage):
        self.publisher.publish(event, message)

#
# CLIENT PROXIES


class BaseClientProxy:
    def __init__(self, web_handler):
        self.web_handler = web_handler

    def _request(self, address_key, event: Event, pubsub):
        msg = self.web_handler.create_meta_message(event, pubsub)

        response = self.web_handler.request(address_key, msg)
        print(Fore.RED + f'{pubsub.upper()} on {event} with response: {response}')

        return response


class BaseClientProxySubscriber(BaseClientProxy):

    def subscribe(self, adress_key: str, event: Event):
        return self._request(adress_key, event, choices.SUBSCRIBE)

    def unsubscribe(self, adress_key: str, event: Event):
        return self._request(adress_key, event, choices.UNSUBSCRIBE)


class BaseClientProxyPublisher(BaseClientProxy):

    def publish(self, adress_key: str, event: Event):
        return self._request(adress_key, event, choices.PUBLISH)
