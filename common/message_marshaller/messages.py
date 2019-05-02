from common.event_channels import choices


class BaseMessage:
    to_str = ['addr', 'event']

    def __init__(self, addr, event):
        self._addr = addr
        self._event = event

    @property
    def addr(self):
        return self._addr

    @property
    def event(self):
        return self._event

    @property
    def class_name(self):
        return self.__class__.__name__

    def __str__(self):
        repr = ''
        for attr in self.to_str:
            repr += f'{getattr(self, attr)}:'

        # Delete the last ':'
        repr = repr[:-1]

        return repr


class MetaMessage(BaseMessage):
    """
    Message with extra meta str info
    """
    to_str = BaseMessage.to_str + ['pubsub', 'address_key']

    def __init__(self, addr, event, pubsub: str, address_key: str):
        super().__init__(addr, event)
        self._pubsub = pubsub
        self._address_key = address_key

    @property
    def pubsub(self):
        return self._pubsub

    @pubsub.setter
    def pubsub(self, value):
        if value not in choices.choices:
            raise TypeError()

        self._pubsub = value

    @property
    def address_key(self):
        return self._address_key


class BrokerMessage(BaseMessage):
    """
        Message with info for broker
    """
    to_str = BaseMessage.to_str + ['address_key', 'requested_address_key']

    def __init__(self, addr, event, address_key, requested_address_key):
        super().__init__(addr, event)
        self._address_key = address_key
        self._requested_address_key = requested_address_key

    @property
    def requested_address_key(self):
        return self._requested_address_key

    @property
    def address_key(self):
        return self._address_key
