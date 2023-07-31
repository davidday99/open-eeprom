from abc import ABC, abstractmethod
from typing import List

from openeeprom.client import OpenEEPROMClient


class BaseChip(ABC):
    def __init__(self, name: str, size: int, description: str=None):
        self.name = name
        self.size = size
        self.client = None
        self.description = description

    @abstractmethod
    def connect(self, client: OpenEEPROMClient):
        pass

    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def read(self, address: int, byte_count: int) -> List[int]:
        pass

    @abstractmethod
    def write(self, address: int, byte_list: List[int]) -> int:
        pass

    @abstractmethod
    def erase(self) -> None:
        pass

