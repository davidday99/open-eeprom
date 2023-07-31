import socket

from .basetransport import BaseTransport


class TcpTransport(BaseTransport):
    def __init__(self, hostname, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, byte_array: bytes) -> None:
        self.socket.sendall(byte_array)

    def receive(self, byte_count: int) -> bytes:
        data = self.socket.recv(byte_count)
        return data

    def flush(self) -> None:
        pass 

    def close(self) -> None:
        self.socket.close()
        self.socket = None

