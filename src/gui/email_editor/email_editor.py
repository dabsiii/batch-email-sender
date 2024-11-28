from abc import ABC, abstractmethod
from typing import List


class EmailEditor(ABC):
    @abstractmethod
    def set_variables(self, variables: List[str]): ...

    @abstractmethod
    def get_subject(self) -> str: ...

    @abstractmethod
    def get_body_html(self) -> str: ...
