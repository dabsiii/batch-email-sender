from abc import ABC, abstractmethod

from PyQt5.QtCore import pyqtSignal


class Toolbar(ABC):
    @abstractmethod
    def bold_action_triggered(self) -> pyqtSignal: ...

    @abstractmethod
    def italic_action_triggered(self) -> pyqtSignal: ...

    @abstractmethod
    def underline_action_triggered(self) -> pyqtSignal: ...

    @abstractmethod
    def change_font_size_triggered(self) -> pyqtSignal: ...
