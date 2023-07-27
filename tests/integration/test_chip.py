import pytest
import random
import time

from OpenEEPROM.chip.basechip import BaseChip
from OpenEEPROM.chip.dummychip import DummyChip
from OpenEEPROM.transport.serial import SerialTransport
from OpenEEPROM.client import OpenEEPROMClient
from OpenEEPROM.chip.x28c256 import X28C256


@pytest.fixture
def chip() -> BaseChip:
    s = SerialTransport('/dev/ttyACM0', 115200)
    client = OpenEEPROMClient(s)
    device = X28C256(client)
    return device 

class TestChip:
    def test_write(self, chip):
        write_vals = [random.randint(0, 255) for i in range(chip.size)]
        
        start_time = time.time()
        write_count = chip.write(0, write_vals)
        end_time = time.time()
        assert(write_count == chip.size)
        print('---- Write time: %s seconds ----' % (end_time - start_time))

    def test_read(self, chip):
        start_time = time.time()
        read_vals = chip.read(0, chip.size)
        end_time = time.time()
        assert len(read_vals) == chip.size
        print('---- Read time: %s seconds ----' % (end_time - start_time))

    def test_erase(self, chip):
        start_time = time.time()
        chip.erase()
        end_time = time.time()
        read_vals = chip.read(0, chip.size)
        assert read_vals.count(0xFF) == chip.size
        print('---- Erase time: %s seconds ----' % (end_time - start_time))

    def test_write_read_erase(self, chip):
        write_vals = [random.randint(0, 255) for i in range(chip.size)]
        
        write_count = chip.write(0, write_vals)
        assert(write_count == chip.size)

        read_vals = chip.read(0, chip.size)
        assert write_vals == read_vals

        chip.erase()
        read_vals = chip.read(0, chip.size)
        assert read_vals.count(0xFF) == chip.size

