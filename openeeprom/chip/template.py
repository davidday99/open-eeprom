from enum import Enum
from typing import List
import struct
import time

from openeeprom.chip.basechip import BaseChip
from openeeprom.client import OpenEEPROMClient


class _Template(BaseChip):
    def __init__(self):
        super().__init__('Chip Name', 0)
        self.description = '''Template'''

    def connect(self, client: OpenEEPROMClient):
        self.client = client

    def disconnect(self):
        self.client.sync()
        self.client = None

    def read(self, address: int, byte_count: int) -> List[int]:
        if address + byte_count > self.size or address < 0:
            raise ValueError('Address out of range.')
        result = []
        return result  

    def write(self, address: int, byte_list: List[int]) -> int:
        if address + byte_count > self.size or address < 0:
            raise ValueError('Address out of range.')
        return len(byte_list)

    def erase(self) -> None:
        self.write(0, [0xFF] * self.size)

