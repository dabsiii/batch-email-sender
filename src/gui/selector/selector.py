from abc import ABC, abstractmethod
from pathlib import Path

from PyQt5.QtCore import pyqtSignal


class Selector(ABC):
    @abstractmethod
    def selected() -> pyqtSignal: ...

    @abstractmethod
    def get_path() -> Path: ...
