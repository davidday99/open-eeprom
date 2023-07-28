# OpenEEPROM

OpenEEPROM is a universal programmer for EEPROMs and flash chips. 
It consists of a client and server that communicate using the 
OpenEEPROM protocol (see `open-eeprom-protocol.txt`). 
Typically the server will be an embedded controller, but it could 
be any device that can receive commands from a client and 
send digital signals to an attached memory chip. 

The topology goes:

CLIENT --> SERVER --> CHIP 

where a transport layer such as serial or TCP sits between CLIENT and SERVER,
and digital IO takes place between SERVER and CHIP.

Chip drivers exist on the client side and implement `read`, `write`, and `erase` commands
using primitive commands supported by the OpenEEPROM protocol.

## Examples

You can call OpenEEPROM from the command line. Here is how you would write to a 25LC320 SPI EEPROM:

```
$ python -m openeeprom.cli write --file input.txt --chip 25LC320 --serial /dev/ttyACM0:115200
```

Or to read the contents of an Atmel 28C256 parallel EEPROM:

```
$ python -m openeeprom.cli read --file output.bin --chip AT28C256 --serial /dev/ttyACM0:115200
```

You can also import OpenEEPROM directly:

```
from openeeprom.transport import SerialTransport
from openeeprom.client import OpenEEPROMClient
from openeeprom.chip import AT28C256

client = OpenEEPROMClient(SerialTransport(port='/dev/ttyACM0', baud_rate=115200))
chip = AT28C256()
chip.connect(client)

contents = chip.read(0, chip.size)
```

Both of these examples assume the programmer is connected to serial port `/dev/ttyACM0` configured
for 115200 bits/s.

## Why Should You use OpenEEPROM?

The alternative is to buy a programmer like the MiniPro for $50+. 
Rather than spending money and waiting on shipping, 
you can turn practically any MCU you have on hand into a programmer
in under an hour.

Another benefit of OpenEEPROM is its ability to integrate into a system. 
Have an embedded system that includes external memory? Run an OpenEEPROM 
server on the processor connected to the memory device.

## Organization 

`openeeprom` is a Python client implementation that can be called as in the above examples.

`open-eeprom-fw` is a reference implementation of an OpenEEPROM server.

See `docs` for a more detailed and development-oriented view of the project.

## Adding New Chips

New chips are added to `openeeprom/chip/`. See the `docs` for details on writing a driver.

## License

GPLv3 (See LICENSE).

