import serial

from .basetransport import BaseTransport


class SerialTransport(BaseTransport):
    def __init__(self, serial_port, baud_rate):
        self.serial = serial.Serial(serial_port, baud_rate)

    def send(self, byte_array: bytes) -> None:
        self.serial.write(byte_array)   

    def receive(self, byte_count: int) -> bytes:
        data = self.serial.read(byte_count)
        return data

