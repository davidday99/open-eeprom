from .basetransport import BaseTransport

ACK = 0x05

class DummyTransport(BaseTransport):
    def __init__(self):
        self.txfifo = bytes()

    def send(self, byte_array: bytes) -> None:
        self.txfifo = byte_array

    def receive(self, byte_count: int) -> bytes:
        return bytes([ACK]) + bytes(byte_count - 1)

