from abc import ABC, abstractmethod
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal


class FileSelectorWidget(ABC):
    @abstractmethod
    def selected_a_file() -> pyqtSignal: ...

    @abstractmethod
    def get_path() -> Path: ...
