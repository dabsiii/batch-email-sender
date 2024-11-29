from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

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

    @abstractmethod
    def update_variables(self, variables: List[str]) -> None: ...

    @abstractmethod
    def get_email_body_html(self) -> str: ...

    @abstractmethod
    def get_email_subject(self) -> str: ...

    @abstractmethod
    def disable_send_email(self) -> None: ...

    @abstractmethod
    def enable_send_email(self) -> None: ...

    @abstractmethod
    def log(self, message: str) -> None: ...
