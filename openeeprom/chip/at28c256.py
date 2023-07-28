import time
from typing import List

from .basechip import BaseChip
from openeeprom.client import OpenEEPROMClient


class AT28C256(BaseChip):
    def __init__(self):
        super().__init__('at28c256', 32768)

    def connect(self, client: OpenEEPROMClient):
        self.client = client
        self.client.set_address_bus_width(15)
        self.client.set_address_hold_time(250)
        self.client.set_pulse_width_time(250)
         
    def disconnect(self):
        #TODO: other steps to ensure clean disconnect?
        self.client.sync()
        self.client = None

    def read(self, address: int, byte_count: int) -> List[int]:
        if address + byte_count > self.size or address < 0:
            raise ValueError('Address out of range.')

        result = []
        offset = 0

        while byte_count > 0:
            read_count = min(byte_count, self.client.max_par_read_count)
            result.extend(self.client.parallel_read(address + offset, read_count))
            byte_count -= read_count
            offset += read_count

        return result

    def write(self, address: int, byte_list: List[int]) -> int:
        byte_count = len(byte_list)
        if address + byte_count > self.size or address < 0:
            raise ValueError('Address out of range.')

        offset = 0

        while byte_count > 0:
            write_count = min(byte_count, self.client.max_par_write_count, 64)
            self.client.parallel_write(address + offset, byte_list[offset:offset + write_count])
            # Technically, a write cycle is typically 5ms but could take up to 10ms, 
            # but factoring in the transport overhead, 5ms should be enough.
            # Still, you should verify the contents of the chip after to be sure.
            time.sleep(0.005)  
            byte_count -= write_count
            offset += write_count

        return len(byte_list) 
         

    def erase(self) -> None:
        self.write(0, [0xFF] * self.size)



