System Architecture
===================

The OpenEEPROM protocol requires two separate systems: a host and a programmer.

.. image:: ../_static/architecture.png
   :align: center

Host
****

The host is the interface that the user interacts with. 
It is responsible for sending OpenEEPROM commands to the programmer and 
interpreting the responses. The host communicates with the programmer using the
transport layer that the programmer supports. This could be a USB peripheral, a USB-serial port,
or a TCP socket if the programmer has a protocol stack. Regardless of the medium, 
the structure of the OpenEEPROM commands are the same, as defined by the OpenEEPROM Protocol.


Programmer
**********

The programmer is the physical device that interfaces with the memory chip.
It is responsible for sending and receiving digital signals to and from the chip.
It must also support a transport medium for receiving commands and sending responses.
The medium used will depend on what peripherals are available on the device. 

The type of transport used will affect overall speeds. For example, a USB peripheral has 
much higher throughput than a 9600 baud UART.

The `OpenEEPROM Portable Programmer <https://github.com/davidday99/open-eeprom-fw>`_ 
is a firmware implementation of the OpenEEPROM protocol. It is designed to be easily 
portable to new devices. New devices need only implement the `transport` and `programmer` 
interfaces that enable host-device and device-chip communication, respectively.

