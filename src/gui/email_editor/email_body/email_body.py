from abc import ABC, abstractmethod
from typing import List


class EmailBody(ABC):
    @abstractmethod
    def apply_bold(self): ...

    @abstractmethod
    def apply_italic(self): ...

    @abstractmethod
    def apply_underline(self): ...

    @abstractmethod
    def change_font_size(self, fontsize: str): ...

    @abstractmethod
    def highlight_variables(self, variables: List[str]): ...

    @abstractmethod
    def get_html(self): ...
