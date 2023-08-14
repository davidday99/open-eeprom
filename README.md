# OpenEEPROM

OpenEEPROM is a universal programmer for EEPROMs and flash chips. 
It consists of a host and programmer that communicate using the 
OpenEEPROM protocol.

## Installation

1. Recursively clone the repository. Program an MCU with the firmware located 
in the submodule `open-eeprom-fw`.

2. Run `pip install -r requirements.txt` to install Python dependencies.

3. Run `make html` inside `docs/` to view more detailed documentation.

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

## Organization 

`openeeprom` is a Python client implementation that can be called as in the above examples.

`open-eeprom-fw` is a reference implementation of an OpenEEPROM server.

See `docs` for a more detailed and development-oriented view of the project.

## License

GPLv3 (See LICENSE).

## Contact

You can reach me at david.day2017@gmail.com.

