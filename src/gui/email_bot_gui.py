from abc import ABC, abstractmethod

from src.event.event import Event


class EmailBotGui(ABC):
    @abstractmethod
    def show(self) -> None: ...

    @abstractmethod
    def selected_credentials(self) -> Event: ...

    @abstractmethod
    def selected_data(self) -> Event: ...

    @abstractmethod
    def selected_folder(self) -> Event: ...

    @abstractmethod
    def send_email_clicked(self) -> Event: ...
