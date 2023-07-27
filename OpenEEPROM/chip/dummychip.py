from .basechip import BaseChip 
from typing import List

from OpenEEPROM.client import OpenEEPROMClient


class DummyChip(BaseChip):
    def __init__(self, client: OpenEEPROMClient):
        super().__init__('dummy', 2**16, client)
        self.memory = [0] * self.size

    def read(self, address: int, byte_count: int) -> List[int]:
        if address + byte_count > self.size or address < 0:
            raise ValueError('Address out of range.')
        
        return self.memory[address:address + byte_count]  

    def write(self, address: int, byte_list: List[int]) -> int:
        byte_count = len(byte_list)

        if address + byte_count > self.size or address < 0:
            raise ValueError('Address out of range.')

        for idx, i in enumerate(byte_list):
            self.memory[address + idx] = i

        return byte_count

    def erase(self) -> None:
        self.memory = [0xFF] * self.size


