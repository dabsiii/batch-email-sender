from abc import ABC, abstractmethod
from pathlib import Path

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

    @abstractmethod
    def get_credentials_path(self) -> Path: ...

    @abstractmethod
    def get_data_path(self) -> Path: ...

    @abstractmethod
    def get_attachment_folder_path(self) -> Path: ...
