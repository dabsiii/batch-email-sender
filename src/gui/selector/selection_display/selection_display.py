from abc import ABC, abstractmethod
from pathlib import Path


class SelectionDisplay(ABC):
    @abstractmethod
    def show_selection(self, path: Path, iconpath: str = None) -> None: ...

    @abstractmethod
    def show_no_selection(self) -> None: ...
