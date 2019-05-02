import socket

from colorama import Fore

from common.registry import Address
from common.settings import BUFFER_SIZE, TIMEOUT_TIME


class Replier:
    STARTING_PORT = 2000

    def __init__(self, listen_address: Address):
        self.s = socket.socket()
        self._configure_socket(listen_address)

    def _configure_socket(self, listen_address):
        self.s.settimeout(TIMEOUT_TIME)
        self.s.bind((listen_address.id, listen_address.port))
        self.s.listen(5)

    def get_message_and_reply(self, reply_handler):
        """
        reply_handler: A function that takes the client byte message as an argument
                and returns the message that will be sent to the client.
        """

        c, addr = self.s.accept()

        try:
            # First get the message.
            byte_message = c.recv(BUFFER_SIZE)
            print(Fore.RED + f'Received: {byte_message}')
            byte_reply_message = reply_handler(byte_message)

            # Secondly respond.
            print(Fore.RED + f'Replying: {byte_reply_message}')
            c.send(byte_reply_message)
        finally:
            c.close()

    def __del__(self):
        self.s.close()

    @classmethod
    def get_current_local_host_replier(cls):
        for offset in range(10000):
            try:
                address = Address('127.0.0.1', cls.STARTING_PORT + offset)
                replier = Replier(address)

                print(Fore.YELLOW + f'Replier it\'s starting on socket: {address}')

                return replier, address
            except:
                pass
