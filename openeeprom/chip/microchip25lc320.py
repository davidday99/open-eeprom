from enum import Enum
from typing import List
import struct
import time

from openeeprom.chip.basechip import BaseChip
from openeeprom.client import OpenEEPROMClient


class MC25LC320Commands(Enum):
    READ = 3
    WRITE = 2
    WRDI = 4
    WREN = 6
    RDSR = 5
    WRSR = 1


class MC25LC320(BaseChip):
    def __init__(self, client: OpenEEPROMClient):
        super().__init__('25LC320', 4096, client)
        self.client.set_spi_mode(0)
        self.client.set_spi_clock_freq(2000000)

    def read(self, address: int, byte_count: int) -> List[int]:
        if address + byte_count > self.size or address < 0:
            raise ValueError('Address out of range.')

        result = []
        while byte_count > 0:
            read_count = min(byte_count, self.client.max_spi_transmit_count - 3)  # account for the 3 control bytes
            nops = [0] * read_count
            addr_bytes = list(struct.pack('>H', address))  # address is interpreted big-endian by the chip
            cmd = [MC25LC320Commands.READ.value, *addr_bytes, *nops]
            # throw away first 3 bytes corresponding to the read command and address bytes
            result.extend(self.client.spi_transmit(cmd)[3:]) 
            byte_count -= read_count
            address += read_count
        return result  

    def write(self, address: int, byte_list: List[int]) -> int:
        byte_count = len(byte_list)
        if address + byte_count > self.size or address < 0:
            raise ValueError('Address out of range.')

        offset = 0
        while byte_count > 0:
            # set write latch to enable writing
            cmd = [MC25LC320Commands.WREN.value]
            self.client.spi_transmit(cmd)
            
            addr_bytes = list(struct.pack('>H', address))  
            remaining_bytes_in_page = 32 - (address % 32)
            write_count = min(byte_count, remaining_bytes_in_page, self.client.max_spi_transmit_count - 3)

            cmd = [MC25LC320Commands.WRITE.value, *addr_bytes, *byte_list[offset:offset + write_count]]
            self.client.spi_transmit(cmd)
            time.sleep(0.005)  # 5ms write cycle

            byte_count -= write_count 
            offset += write_count
            address += write_count

        return len(byte_list)

    def erase(self) -> None:
        self.write(0, [0xFF] * self.size)

