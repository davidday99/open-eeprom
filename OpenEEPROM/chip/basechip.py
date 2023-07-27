from abc import ABC, abstractmethod
from typing import List

from OpenEEPROM.client import OpenEEPROMClient


class BaseChip(ABC):
    def __init__(self, name: str, size: int, client: OpenEEPROMClient):
        self.name = name
        self.size = size
        self.client = client
    
    @abstractmethod
    def read(self, address: int, byte_count: int) -> List[int]:
        pass

    @abstractmethod
    def write(self, address: int, byte_list: List[int]) -> int:
        pass

    @abstractmethod
    def erase(self) -> None:
        pass

