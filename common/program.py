from colorama import Fore

from common.request_reply.proxies import BaseClientProxyPublisher, BaseClientProxySubscriber
from common.registry import Address


class Program:
    client_proxy_subscriber_class = BaseClientProxySubscriber
    client_proxy_publisher_class = BaseClientProxyPublisher

    def __init__(self, web_handler, events: list):
        self.web_handler = web_handler
        self.events = events

        self.client_proxy_subscriber = self.client_proxy_subscriber_class(self.web_handler)
        self.client_proxy_publisher = self.client_proxy_publisher_class(self.web_handler)

    def add_server_address(self, addr_key: str, address: Address):
        self.web_handler.persist_address(addr_key, address)

    def start(self):
        self.web_handler.listen()

        while True:
            event = input(Fore.BLUE + f'Choose an event from: {self.events} ?    ')
            event = event.strip()

            if event not in self.events:
                print(Fore.BLUE + 'Wrong event.')
                continue

            event = self.web_handler.event_mapper.get_event_class(event)()

            proxy = None

            address_key = input(Fore.BLUE + f'Choose address key from: {self.web_handler.get_broker_registry()} ?')
            address_key = address_key.strip()

            msg = None

            while proxy is None:
                msg = input(Fore.BLUE + 'Subscribe (S) / Unsubscribe (U)/ Publish (P) / Finish (F) ?     ')
                msg = msg.strip().upper()

                if msg == 'S':
                    proxy = self.client_proxy_subscriber
                    proxy.subscribe(address_key, event)
                elif msg == 'U':
                    proxy = self.client_proxy_subscriber
                    proxy.unsubscribe(address_key, event)
                elif msg == 'P':
                    proxy = self.client_proxy_publisher
                    proxy.publish(address_key, event)
                elif msg == 'F':
                    break
                else:
                    print(Fore.BLUE + 'Wrong value.')
                    continue

            if msg == 'F':
                self.web_handler.stop()
                break
