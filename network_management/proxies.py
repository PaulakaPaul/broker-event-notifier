from common.request_reply.proxies import BaseClientProxySubscriber, BaseClientProxyPublisher
from common.event_channels.events import Event


MEDIATOR_NAME = 'mediator'


class MediatorClientProxySubscriber(BaseClientProxySubscriber):
    def subscribe(self, event: Event):
        return super().subscribe(MEDIATOR_NAME, event)

    def unsubscribe(self, event: Event):
        return super().unsubscribe(MEDIATOR_NAME, event)


class MediatorClientProxyPublisher(BaseClientProxyPublisher):
    def publish(self, event: Event):
        return super().publish(MEDIATOR_NAME, event)
