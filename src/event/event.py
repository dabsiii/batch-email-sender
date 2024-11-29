from abc import ABC, abstractmethod

class Event(ABC):
    @abstractmethod
    def subscribe(self, function)->None:...

    @abstractmethod
    def publish(self)->None:...
        