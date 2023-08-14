Getting Started
===============

OpenEEPROM is a universal programmer for EEPROMs and flash chips. It consists of 
three components:

    1. OpenEEPROM protocol - a set of commands for programming parallel and SPI chips (and I2C eventually).
    2. Programmer - a device running firmware that implements the OpenEEPROM protocol and interfaces directly with the memory chip.
    3. Host - software that sends commands to the programmer and reads back the responses.

This project includes a firmware implementation that can be ported to new MCUs without significant modifications
and a Python host for communicating with it.

One of the primary objectives of OpenEEPROM is to enable a user to turn any MCU into 
a programmer. 

The protocol command set provides control of timing and digital signals, 
allowing you to write high-level drivers on the host side.

Installation
------------

Clone the repository:

.. code-block:: bash

   $ git clone --recursive https://github.com/davidday99/open-eeprom.git && cd open-eeprom

Install the dependencies:

.. code-block:: bash

   $ pip install -r requirements.txt

Program an MCU with the `OpenEEPROM firmware <https://github.com/davidday99/open-eeprom-fw.git>`_. 
After that, you're good to go.

           
Examples
--------

You can call OpenEEPROM from the command line. 

.. code-block:: bash 

    $ python -m openeeprom.cli list

This will list all the supported chips. 

Now let's assume our programmer is connected to the host over a serial port. 
Here is how you would write to a 25LC320 SPI EEPROM:

.. code-block:: bash 

    $ python -m openeeprom.cli write --file input.txt --chip 25LC320 --serial /dev/ttyACM0:115200


Or read the contents of an Atmel 28C256 parallel EEPROM:

.. code-block:: bash 

    $ python -m openeeprom.cli read --file output.bin --chip AT28C256 --serial /dev/ttyACM0:115200


You can also import OpenEEPROM directly:

.. code-block:: python

    from openeeprom.transport import SerialTransport
    from openeeprom.client import OpenEEPROMClient
    from openeeprom.chip import AT28C256

    client = OpenEEPROMClient(SerialTransport(port='/dev/ttyACM0', baud_rate=115200))
    chip = AT28C256()
    chip.connect(client)

    contents = chip.read(0, chip.size)

Why Should I use OpenEEPROM?
----------------------------

OpenEEPROM is a free and open source alternative to products like the 
`MiniPRO TL866xx <https://www.amazon.com/Universal-Programmer-TL866II-MiniPro-Adapter/dp/B091TPHW1M>`_
series of programmers.

If OpenEEPROM doesn't support a chip, it's easy to create and test a host-side driver that will enable
reading, writing, and erasing, as well as any chip-specific features. See :ref:`new chip support` for details.

