import argparse

from openeeprom.chip import \
        microchip25lc320, \
        at28c256
from openeeprom.transport.serial import SerialTransport
from openeeprom.client import OpenEEPROMClient

DESCRIPTION = '''
A tool for accessing EEPROM and flash chips.
'''

SUPPORTED_DEVICES = {
        '25LC320': microchip25lc320.MC25LC320(),
        'AT28C256': at28c256.AT28C256(),
}


def parse_args():
    parser = argparse.ArgumentParser(prog='openeeprom', description=DESCRIPTION, usage='%(prog)s <command> [options]')
    parser.add_argument('command', help='read, write, erase, verify, list')
    parser.add_argument('--chip', help="run command 'list' to view supported chips")
    parser.add_argument('--serial', type=str)
    parser.add_argument('--offset', type=str, default=0)
    parser.add_argument('--count', type=str)
    parser.add_argument('--file', type=str)
    args = parser.parse_args()
    return args 


def main():
    args = parse_args()
    
    if args.command == 'list':
        chips = SUPPORTED_DEVICES.keys()
        print('Supported chips:')
        print()
        for chip in chips:
            print(chip, '\t', SUPPORTED_DEVICES[chip].description)
        return

    if args.serial:
        port, baud_rate = args.serial.split(':')
        baud_rate = int(baud_rate)
        transport = SerialTransport(port, baud_rate)

    chip = SUPPORTED_DEVICES[args.chip]
    client = OpenEEPROMClient(transport)
    chip.connect(client)

    if args.command == 'read':
        offset = int(args.offset)
        count = int(args.count) if args.count else chip.size
        data = chip.read(offset, count)
        
        if args.file:
            with open(args.file, 'wb') as f:
                f.write(bytes(data))
        else:
            print(data)

    if args.command == 'write':
        offset = int(args.offset)
        
        with open(args.file, 'rb') as f:
            data = list(f.read())

        chip.write(offset, data)
         
    if args.command == 'erase':
        chip.erase()
        print('Chip erase complete.')

    if args.command == 'verify':
        with open(args.file, 'rb') as f:
            data = list(f.read())

        chip_contents = chip.read(0, len(data))

        for idx, pair in enumerate(zip(data, chip_contents)):
            if pair[0] != pair[1]:
                print(f'Difference at offset {idx}. {pair[0]} (file) != {pair[1]} (chip).')

        print('Contents are equivalent.')


if __name__ == '__main__':
    main()
None
