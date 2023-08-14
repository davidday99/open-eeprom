.. _new chip support:

Adding Support for New Chips
============================

Chip drivers are located in ``openeeprom/chip/``. All drivers
should inherit the ``BaseChip`` class from ``openeeprom.chip.basechip`` and 
implement all of its methods.

All chips must support read, write, and erase functionality, the methods for 
which are included in ``BaseChip``. Additionally, ``connect`` and ``disconnect``
methods should be implemented for initial setup and proper cleanup.

``openeeprom/chip/template.py`` can be used as a template for new drivers.

Let's write a driver for the Microchip 25LC320 SPI EEPROM as an example.

Class Initialization
********************

I've started by copying ``openeeprom/chip/template.py`` to my new file
``openeeprom/chip/microchip25lc320.py`` and changing the class name. 
Inside of the class ``__init__`` method I'll specify the name of the device, 
its size, and a description.

.. code-block:: python

    class MC25LC320(BaseChip):
        def __init__(self):
            super().__init__('25LC320', 4096)
            self.description = '''Microchip 4KB SPI EEPROM'''


Connect and Disconnect
**********************

The ``connect`` and ``disconnect`` methods will setup the initial 
connection and clean up afterward.

``connect`` should always start by initializing ``self.client`` with
the ``client`` parameter. This attribute will be used by driver for 
sending OpenEEPROM protocol commands. After assigning ``self.client = client``,
all initial setup commands should be sent to the programmer. This includes
things like setting the SPI clock and mode or setting the address bus width in the
case of a parallel chip.

.. code-block:: python


    def connect(self, client: OpenEEPROMClient):
        self.client = client
        self.client.set_spi_mode(0)
        self.client.set_spi_clock_freq(2000000)

I've set the SPI mode to Mode 0 and the frequency to 2 MHz based on information 
specified in the chip's datasheet.

For ``disconnect``, I'll call ``flush`` to ensure any potentially leftover
data has been sent out, and then I'll set ``self.client`` to ``None`` to ensure
any subsequent attempts to access the chip without first reconnecting will fail.

.. code-block:: python

    def disconnect(self):
        self.client.sync()
        self.client = None

Read
****

To read data, the 25LC320 expects the READ command (0x03) followed by 2 bytes for the 
address. 


I'll add a class to represent the SPI commands that the 25LC320 accepts, simply for readability:

.. code-block:: python 

    class MC25LC320Commands(Enum):
        READ = 3
        WRITE = 2
        WRDI = 4
        WREN = 6
        RDSR = 5
        WRSR = 1


The address is interpreted big-endian and the top four bits are ignored. After 
sending those three bytes, I can continue to read as many bytes as I want by pulsing the 
SPI clock with the CS line held low. Pulsing the SPI clock requires that I transmit a byte.
The value doesn't matter, so I'll transmit 0 for as many bytes as I want to read. 

However, I may not be able to send the three starting bytes followed by *n* dummy bytes in
a single command, as this may exceed programmer's RX buffer. So instead, I'll use the attribute
``self.client.max_spi_transmit_count`` to send only as many bytes in a single command as the
programmer can handle.

.. code-block:: python

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

For each iteration of the loop, I read as many bytes as the programmer will allow and append that to a running list. The 
first three bytes that the chip sends out correspond to the READ command and the address, so those should be ignored.

Notice that I also check whether ``address`` is valid.

Write
*****

To write data, the 25LC320 requires that I first send the WREN command (0x06) and raise the CS line
before attempting to write. I'll send that first, after again validating the address.

.. code-block:: python

    def write(self, address: int, byte_list: List[int]) -> int:
        byte_count = len(byte_list)
        if address + byte_count > self.size or address < 0:
            raise ValueError('Address out of range.')

        offset = 0
        while byte_count > 0:
            # set write latch to enable writing
            cmd = [MC25LC320Commands.WREN.value]
            self.client.spi_transmit(cmd)
        ...

After sending that, I can actually start writing data. The 25LC320 can write up to 32 bytes in a single cycle and
takes up to 5ms to complete the write cycle. I'll account for the 32 bytes when I determine the max number of bytes 
I can transmit at one time, again using ``self.client.max_spi_transmit_count`` to ensure I don't exceed the 
amount the programmer can handle. It's unlikely that the programmer's buffer is less than 32 bytes, 
but it's better not to assume. 

Picking up where I left off:

.. code-block:: python

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

In each iteration I start by sending the WREN command, as is required by the chip. 
        
Erase
*****

The easiest method is often ``erase`` because one option is to simply use 
``self.write`` to fill the memory space with ``0xFF``. That is what I'll do here:

.. code-block:: python

    def erase(self) -> None:
        self.write(0, [0xFF] * self.size)

Some chips may support a specific command for erasing which will almost certainly
be more performant, but the given approach is tried and true.

Chip-Specific Functions
***********************

All chips are required to implement RWE functions, but some
chips may also support extra functions. For example, the 25LC320
provides software-enabled protection. Such methods can be optionally be added to the 
class.

Testing
*******

``tests/integration/test_chip.py`` can be used to test a new chip driver.
Just modify the ``chip`` fixture to return the new driver and run the test suite.

.. code-block:: python


    @pytest.fixture
    def chip() -> BaseChip:
        s = SerialTransport('/dev/ttyACM0', 115200)
        client = OpenEEPROMClient(s)
        device = MC25LC320()
        device.connect(client)
        return device 

Adding to the Application
*************************

Once the new driver is complete, the last step is to add it 
to the main CLI driver in ``openeeprom/cli/__main__.py``.

.. code-block:: python

    SUPPORTED_DEVICES = {
            '25LC320': microchip25lc320.MC25LC320(),
            'AT28C256': at28c256.AT28C256(),
    }

Run ``python -m openeeprom.cli list`` and see that the chip is now listed.

