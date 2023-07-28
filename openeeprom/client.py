from enum import Enum
from typing import List
import struct

from .transport.basetransport import BaseTransport


class OpenEEPROMCommands(Enum):
    NOP = 0
    SYNC = 1
    GET_INTERFACE_VERSION = 2
    GET_MAX_RX_SIZE = 3
    GET_MAX_TX_SIZE = 4
    TOGGLE_IO = 5
    GET_SUPPORTED_BUS_TYPES = 6
    SET_ADDRESS_BUS_WIDTH = 7
    SET_ADDRESS_HOLD_TIME = 8
    SET_PULSE_WIDTH_TIME = 9
    PARALLEL_READ = 10
    PARALLEL_WRITE = 11 
    SET_SPI_CLOCK_FREQUENCY = 12
    SET_SPI_MODE = 13
    GET_SUPPORTED_SPI_MODES = 14
    SPI_TRANSMIT = 15


class OpenEEPROMResponseStatus:
    ACK = 0x05
    NAK = 0x06


class OpenEEPROMCommandFailedException(Exception):
    pass


class OpenEEPROMClient:
    def __init__(self, io_handle: BaseTransport):
        self.io = io_handle
        self.sync()
        self.max_rx_size = self.get_max_rx_size()
        self.max_tx_size = self.get_max_tx_size()
        self.max_par_read_count = self.max_tx_size - 1
        self.max_par_write_count = self.max_rx_size - 9
        self.max_spi_transmit_count = min(self.max_rx_size - 5, self.max_tx_size - 1)

    def nop(self):
        cmd = bytes([OpenEEPROMCommands.NOP.value])
        self.io.send(cmd)
        self._check_response_status()

    def sync(self):
        self.io.flush()
        cmd = bytes([OpenEEPROMCommands.SYNC.value])
        self.io.send(cmd)
        self._check_response_status()

    def get_interface_version(self) -> int:
        cmd = bytes([OpenEEPROMCommands.GET_INTERFACE_VERSION.value])
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(2)
        version = struct.unpack_from('<H', result)[0]
        return version

    def get_max_rx_size(self) -> int:
        cmd = bytes([OpenEEPROMCommands.GET_MAX_RX_SIZE.value])
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(4)
        sz = struct.unpack_from('<I', result)[0]
        return sz 

    def get_max_tx_size(self) -> int:
        cmd = bytes([OpenEEPROMCommands.GET_MAX_TX_SIZE.value])
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(4)
        sz = struct.unpack_from('<I', result)[0]
        return sz 

    def toggle_io(self, state: int) -> int:
        cmd = bytes([OpenEEPROMCommands.TOGGLE_IO.value, state])
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(1)
        set_state = struct.unpack_from('B', result)[0]

        if set_state != state:
            raise OpenEEPROMCommandFailedException(f'Could not set IO to state {state}')

        return set_state 

    def get_supported_bus_types(self) -> int:
        cmd = bytes([OpenEEPROMCommands.GET_SUPPORTED_BUS_TYPES.value])
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(1)
        supported_bus_types = struct.unpack_from('B', result)[0]
        return supported_bus_types

    def set_address_bus_width(self, bus_width: int) -> int:
        cmd = bytes([OpenEEPROMCommands.SET_ADDRESS_BUS_WIDTH.value, bus_width])
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(1)
        set_width = struct.unpack_from('B', result)[0]

        if set_width != bus_width:
            raise OpenEEPROMCommandFailedException(f'Could not set bus to width {bus_width}. Max width is {set_width}.')

        return set_width 

    def set_address_hold_time(self, hold_time: int) -> int:
        cmd = bytes([OpenEEPROMCommands.SET_ADDRESS_HOLD_TIME.value]) + struct.pack('<I', hold_time)
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(4)
        set_hold_time = struct.unpack('<I', result)[0]

        if set_hold_time != hold_time:
            raise OpenEEPROMCommandFailedException(f'Could not set address hold time to {100 * hold_time} ns. It is set to {100 * set_hold_time} ns.')


        return set_hold_time

    def set_pulse_width_time(self, width_time: int) -> int:
        cmd = bytes([OpenEEPROMCommands.SET_PULSE_WIDTH_TIME.value]) + struct.pack('<I', width_time)
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(4)
        set_width_time = struct.unpack('<I', result)[0]

        if set_width_time != width_time :
            raise OpenEEPROMCommandFailedException(f'Could not set pulse width time to {100 * width_time} ns. It is set to {100 * set_width_time} ns.')

        return set_width_time

    def parallel_read(self, address: int, byte_count: int) -> List[int]:
        if byte_count > self.max_par_read_count:
            raise OpenEEPROMCommandFailedException('Read count exceeds device transmit buffer size.')

        cmd = bytes([OpenEEPROMCommands.PARALLEL_READ.value]) + struct.pack('<I', address) + struct.pack('<I', byte_count)
        self.io.send(cmd)
        self._check_response_status()
        result = list(self.io.receive(byte_count))
        return result


    def parallel_write(self, address: int, byte_list: List[int]):
        byte_count = len(byte_list)

        if byte_count > self.max_par_write_count:
            raise OpenEEPROMCommandFailedException('Write count exceeds device receive buffer size.')

        cmd = bytes([OpenEEPROMCommands.PARALLEL_WRITE.value]) + struct.pack('<I', address) + struct.pack('<I', byte_count) + bytes(byte_list)
        self.io.send(cmd)
        self._check_response_status()
            
    def set_spi_clock_freq(self, freq: int) -> int:
        cmd = bytes([OpenEEPROMCommands.SET_SPI_CLOCK_FREQUENCY.value]) + struct.pack('<I', freq) 
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(4)
        set_freq = struct.unpack('<I', result)[0]

        if set_freq != freq:
            raise OpenEEPROMCommandFailedException(f'Could not set SPI clock frequency to {freq} Hz. It is set to {freq} Hz.')

        return set_freq

    def set_spi_mode(self, mode: int) -> int:
        cmd = bytes([OpenEEPROMCommands.SET_SPI_MODE.value]) + struct.pack('B', mode) 
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(1)
        set_mode = struct.unpack('B', result)[0]

        if set_mode != mode:
            raise OpenEEPROMCommandFailedException(f'Could not set to SPI mode {mode}. It is set to mode {mode}.')

        return set_mode 
        
    def get_supported_spi_modes(self) -> int:
        cmd = bytes([OpenEEPROMCommands.GET_SUPPORTED_SPI_MODES.value])
        self.io.send(cmd)
        self._check_response_status()
        result = self.io.receive(1)
        supported_modes = struct.unpack('B', result)[0]
        return supported_modes

    def spi_transmit(self, byte_list: List[int]) -> List[int]:
        byte_count = len(byte_list)   

        if byte_count > self.max_spi_transmit_count:
            raise OpenEEPROMCommandFailedException('Transmit count must fit within device receive and transmit buffers.')

        cmd = bytes([OpenEEPROMCommands.SPI_TRANSMIT.value]) + struct.pack('<I', byte_count) + bytes(byte_list)

        self.io.send(cmd)
        self._check_response_status()
        result = list(self.io.receive(byte_count))
        return result 

    def _check_response_status(self):
        status = self.io.receive(1)[0]
        if status == OpenEEPROMResponseStatus.NAK:
            raise OpenEEPROMCommandFailedException('The previous command returned NAK.')
        elif status != OpenEEPROMResponseStatus.ACK:
            raise OpenEEPROMCommandFailedException(f'The previous command returned an unknown status: {status}')

