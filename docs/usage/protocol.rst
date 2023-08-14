OpenEEPROM Protocol
===================

This page specifies the OpenEEPROM protocol *version 1.0.0*. It is a byte-stream oriented protocol
with a set of commands. Each command takes zero or more parameters and responds 
with a status byte followed by zero or more bytes. Data is always represented in
little-endian.


A command will return one of two status bytes:

- ACK: 0x05
- NAK: 0x06

Command Set 
***********

.. list-table:: OpenEEPROM Command Set
    :header-rows: 1

    * - Command
      - Encoding
      - Description
      - Parameters 
      - Response

    * - NOP
      - 0x00
      - Do nothing except return an ACK.
      - None
      - <ACK>

    * - SYNC
      - 0x01
      - Flush any data waiting in the transport layer.
      - None
      - <ACK>

    * - Get interface version
      - 0x02
      - Get the version of the firmware running on the programmer.
      - None
      - <ACK> <16-bit version>

    * - Get max RX size
      - 0x03
      - Get the max number of bytes the programmer can receive in a single command.
      - None
      - <ACK> <32-bit RX buffer size>
   
    * - Get max TX size
      - 0x04
      - Get the max number of bytes the programmer can send in a single response.
      - None
      - <ACK> <32-bit TX buffer size>

    * - Toggle IO
      - 0x05
      - Enable Disable all IO lines coming out of the programmer.
      - <8-bit mode> (0 to disable, else enable)
      - <ACK> <8-bit set mode>

    * - Get supported bus types
      - 0x06
      - Get the bus types that the programmer supports
      - None
      - <ACK> <8-bit mask of supported bus types>

    * - Set address bus width
      - 0x07
      - Set the address bus width for parallel chips.
      - <8-bit address bus width>
      - <ACK> <8-bit set address bus width> / <NAK>


    * - Set address hold time
      - 0x08
      - Set the time to wait, in nanoseconds, after the address bus is set
      - <32-bit nanosecond count>
      - <ACK> <32-bit set nanosecond count> / <NAK> 

    * - Set pulse width time
      - 0x09
      - Set the chip enable pulse width in nanoseconds for parallel chips.
      - <32-bit nanosecond count>
      - <ACK> <32-bit set nanosecond count> / <NAK> 

    * - Parallel Read
      - 0x0A
      - Read N bytes starting from address A of a parallel chip. 
      - <32-bit address A> <32-bit count N>
      - <ACK> <N bytes> / <NAK>

    * - Parallel Write
      - 0x0B
      - Write N bytes starting at address A of a parallel chip.
      - <32-bit address A> <32-bit count N> < N bytes>
      - <ACK> / <NAK>

    * - Set SPI clock frequency
      - 0x0C
      - Set the frequency in Hz of the SPI clock.
      - <32-bit frequency>
      - <ACK> / <NAK>


    * - Set SPI mode
      - 0x0D
      - Set the SPI mode
      - <8-bit mode> (0, 1, 2, or 3)
      - <ACK> <8-bit set mode> / <NAK>

    * - Get supported SPI modes
      - 0x0E
      - Get the SPI modes that the programmer supports.
      - None
      - <ACK> <8-bit mask of supported SPI modes>

    * - SPI transmit
      - 0x0F
      - Transmit and receive N bytes over SPI.
      - <32-bit count N> <N bytes>
      - <ACK> <N bytes> / <NAK>  

Command Details
***************

#. ``Get supported bus types`` returns a bit mask:

    - 1: Parallel 
    - 2: SPI
    - 4: I2C

#. ``Set address bus width`` will return NAK if the programmer does not support the requested bus width.

#. ``Set address hold time`` and ``Set pulse width time`` will return NAK if
   an unsupported time is used. This can happen if you try to use a count
   smaller than the programmer can support. 

#. ``Parallel read`` and ``Parallel write`` will return NAK if the either of the 
   command length or the response length would exceed the RX or TX buffers, respectively.

#. ``Set SPI clock frequency`` will return NAK if the programmer does not support the 
   requested frequency.

#. ``Set SPI mode`` will return NAK if the programmer does not support the requested mode.

#. ``Get supported SPI modes`` returns a bit mask:
   - 1: SPI mode 0
   - 2: SPI mode 1
   - 4: SPI mode 2
   - 8: SPI mode 3
#. ``SPI transmit`` will return NAK if either of the command length or response length
    would exceed the RX or TX buffers, respectively.

