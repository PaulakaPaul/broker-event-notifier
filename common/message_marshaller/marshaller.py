import importlib

from common.event_channels.events import EventMapper
from common.registry import Address


class MessageMarshaller:
    def marshal(self, message):
        stringified = f' {message.class_name}:{message}'
        message_bytes = bytearray(stringified, encoding='utf-8')

        message_bytes[0] = self._get_supported_message_length(stringified)
        return message_bytes

    def _get_supported_message_length(self, message):
        msg_length = len(message)
        msg_length = msg_length - 1  # We don't want to include the length of the meta information.
        if msg_length > 255:
            return 0

        return msg_length

    def unmarshal(self, byte_message, event_mapper: EventMapper):
        # msg_length = int(byte_message[0])
        stringified = byte_message.decode()[1:]

        message_type_name, stringified = self._extract_item(stringified)
        message_class = self._get_message_class(message_type_name)

        addr, stringified = self._extract_item(stringified)
        addr = self._parse_addr(addr)

        event_name, stringified = self._extract_item(stringified)
        event = event_mapper.get_event_class(event_name)()

        # Extract str info
        messages = []

        while True:
            try:
                message, stringified = self._extract_item(stringified)

                if message:
                    messages.append(message)

                if not stringified:
                    break

            except ValueError:
                if stringified:
                    messages.append(stringified)  # What it's left it's the last message.

                break

        message_obj = message_class(addr, event, *messages)

        return message_obj

    def _extract_item(self, stringified):
        try:
            colon_index = stringified.index(':')
            item = stringified[:colon_index]

            stringified = stringified[colon_index + 1:]

            return item, stringified
        except ValueError:
            return stringified, ''

    def _get_message_class(self, message_type):
        module = importlib.import_module('common.message_marshaller')
        message_class = getattr(module, message_type)

        return message_class

    def _parse_addr(self, addr: str) -> Address:
        addr = addr[1:-1]
        id, port = addr.split(',')

        return Address(id, int(port))
