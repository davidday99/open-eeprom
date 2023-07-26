from .basechip import BaseChip


class X28C256(BaseChip):
    def __init__(self):
        super().__init__('x28c256', 32768)


    def read(self, address, byte_count): 
        # verify address and byte_count
        # if address + byte_count > size
        #   raise Exception
        # send OpenEEPROM commands
        # client.set_parallel_timings
        # byte_list = client.parallel_read(address, byte_count)
        # return byte_list
