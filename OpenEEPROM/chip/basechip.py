from abc import ABC, abstractmethod


class BaseChip(ABC):
    def __init__(self, name, size):
        self.name = name
        self.size = size
    
    @abstractmethod
    def read(self, address, byte_count):
        pass

    @abstractmethod
    def write(self, address, byte_list):
        pass

    @abstractmethod
    def erase(self):
        pass

