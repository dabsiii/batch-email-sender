from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from src.gui.email_editor.email_editor import EmailEditor


class EmailEditorC1(EmailEditor):
    def set_variables(self, variables: List[str]): ...

    def get_body_html(self) -> str: ...

    def get_subject(self) -> str: ...

    def __init__(self):
        self._init_gui()

    def _init_gui(self):
        self.widget = QWidget()
