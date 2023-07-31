from abc import ABC, abstractmethod

class BaseTransport(ABC):
    @abstractmethod
    def send(self, byte_array: bytes) -> None:
        pass

    @abstractmethod
    def receive(self, byte_count: int) -> bytes:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

