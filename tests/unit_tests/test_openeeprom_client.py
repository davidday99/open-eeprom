import pytest
import struct

from OpenEEPROM.client import OpenEEPROMClient, OpenEEPROMCommands
from OpenEEPROM.transport.dummy import DummyTransport

@pytest.fixture
def dummy_client():
    client = OpenEEPROMClient(DummyTransport())
    client.max_rx_size = 1024
    client.max_tx_size = 1024
    return client


class TestOpenEEPROMClient:
    def test_nop(self, dummy_client):
        dummy_client.nop()
        assert dummy_client.io.txfifo == bytes([OpenEEPROMCommands.NOP.value])

    def test_sync(self, dummy_client):
        dummy_client.sync()
        assert dummy_client.io.txfifo == bytes([OpenEEPROMCommands.SYNC.value])

    def test_get_interface(self, dummy_client):
        dummy_client.get_interface_version()
        assert dummy_client.io.txfifo == bytes([OpenEEPROMCommands.GET_INTERFACE_VERSION.value])

    def test_get_max_rx_size(self, dummy_client):
        dummy_client.get_max_rx_size()
        assert dummy_client.io.txfifo == bytes([OpenEEPROMCommands.GET_MAX_RX_SIZE.value])


    def test_get_max_tx_size(self, dummy_client):
        dummy_client.get_max_tx_size()
        assert dummy_client.io.txfifo == bytes([OpenEEPROMCommands.GET_MAX_TX_SIZE.value])

    def test_toggle_io(self, dummy_client):
        with pytest.raises(Exception):
            dummy_client.toggle_io(0)
        assert dummy_client.io.txfifo[0:1] == bytes([OpenEEPROMCommands.TOGGLE_IO.value])
        assert dummy_client.io.txfifo[1:2] == bytes([0])

        with pytest.raises(Exception):
            dummy_client.toggle_io(1)
        assert dummy_client.io.txfifo[0:1] == bytes([OpenEEPROMCommands.TOGGLE_IO.value])
        assert dummy_client.io.txfifo[1:2] == bytes([1])

    def test_get_supported_bus_types(self, dummy_client):
        dummy_client.get_supported_bus_types()
        assert dummy_client.io.txfifo == bytes([OpenEEPROMCommands.GET_SUPPORTED_BUS_TYPES.value])

    def test_set_address_bus_width(self, dummy_client):
        with pytest.raises(Exception):
            dummy_client.set_address_bus_width(0xab)
        assert dummy_client.io.txfifo[0:1] == bytes([OpenEEPROMCommands.SET_ADDRESS_BUS_WIDTH.value])
        assert dummy_client.io.txfifo[1:2] == bytes([0xab])


    def test_set_address_hold_time(self, dummy_client):
        with pytest.raises(Exception):
            dummy_client.set_address_hold_time(0xabcdef01)
        assert dummy_client.io.txfifo[0:1] == bytes([OpenEEPROMCommands.SET_ADDRESS_HOLD_TIME.value])
        assert dummy_client.io.txfifo[1:5] == b'\x01\xef\xcd\xab' 

    def test_set_pulse_width_time(self, dummy_client):
        with pytest.raises(Exception):
            dummy_client.set_pulse_width_time(0xabcdef01)
        assert dummy_client.io.txfifo[0:1] == bytes([OpenEEPROMCommands.SET_PULSE_WIDTH_TIME.value])
        assert dummy_client.io.txfifo[1:5] == b'\x01\xef\xcd\xab' 

    def test_parallel_read(self, dummy_client):
        result = dummy_client.parallel_read(0, 64) 
        assert len(result) == 64 
        assert dummy_client.io.txfifo[0:1] == bytes([OpenEEPROMCommands.PARALLEL_READ.value])

    def test_parallel_read_exceed_length(self, dummy_client):
        with pytest.raises(Exception):
            result = dummy_client.parallel_read(0, dummy_client.max_tx_size + 1) 

    def test_parallel_write(self, dummy_client):
        write_list = [1, 2, 3, 4]
        dummy_client.parallel_write(0, write_list)
        assert dummy_client.io.txfifo[0:1] == bytes([OpenEEPROMCommands.PARALLEL_WRITE.value])
        assert dummy_client.io.txfifo[1:5] == struct.pack('<I', 0)
        assert dummy_client.io.txfifo[5:9] == struct.pack('<I', len(write_list))
        assert dummy_client.io.txfifo[9:13] == struct.pack('BBBB', *write_list)
    
    def test_parallel_write_exceed_length(self, dummy_client):
        with pytest.raises(Exception):
            result = dummy_client.parallel_write(0, dummy_client.max_rx_size + 1) 

    def test_set_clock_freq(self, dummy_client):
        with pytest.raises(Exception):
            dummy_client.set_spi_clock_freq(0xabcdef01)
        assert dummy_client.io.txfifo[0:1] == bytes([OpenEEPROMCommands.SET_SPI_CLOCK_FREQUENCY.value])
        assert dummy_client.io.txfifo[1:5] == b'\x01\xef\xcd\xab' 

    def test_get_supported_spi_modes(self, dummy_client):
        dummy_client.get_supported_spi_modes()
        assert dummy_client.io.txfifo == bytes([OpenEEPROMCommands.GET_SUPPORTED_SPI_MODES.value])


    def test_spi_transmit(self, dummy_client):
        write_list = [1, 2, 3, 4]
        dummy_client.spi_transmit(write_list) 
        assert dummy_client.io.txfifo[0:1] == bytes([OpenEEPROMCommands.SPI_TRANSMIT.value])
        assert dummy_client.io.txfifo[1:5] == struct.pack('<I', len(write_list)) 
        assert dummy_client.io.txfifo[5:9] == struct.pack('BBBB', *write_list)


