from common.event_channels.events import Event
from common.message_marshaller.messages import MetaMessage


class Publisher:
    def __init__(self, event_bus, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_bus = event_bus

    def publish(self, event: Event, message: MetaMessage):
        self.event_bus.publish(event, message)
