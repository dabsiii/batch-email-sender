from abc import ABC, abstractmethod
from pathlib import Path

from PyQt5.QtCore import pyqtSignal

from src.event.event import Event


class Selector(ABC):
    @abstractmethod
    def selected() -> Event: ...

    @abstractmethod
    def get_path() -> Event: ...
