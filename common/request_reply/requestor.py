import socket

from common.settings import BUFFER_SIZE, TIMEOUT_TIME


def request(address, byte_message: bytes):
    s = socket.socket()
    s.settimeout(TIMEOUT_TIME)

    try:
        # Send message
        s.connect((address.id, address.port)),
        s.send(byte_message)

        # Wait for response
        return s.recv(BUFFER_SIZE)
    finally:
        s.close()
