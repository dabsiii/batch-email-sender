from abc import ABC, abstractmethod


class EmailBotGui(ABC):
    @abstractmethod
    def show(self) -> None: ...
