import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

from src.gui.email_bot_gui import EmailBotGui
from src.gui.email_editor.email_editor_c1 import EmailEditorC1
from src.gui.selector.file_selector import FileSelector
from src.gui.selector.folder_selector import FolderSelector


class EmailBotGuiC1(EmailBotGui):
    """
    A. Selectors
    B. Gmail Editor
    C. Send Email
    """

    def __init__(self):
        pass

    def _init_gui(self) -> None:
        self._widget = QWidget()
        self._layout = QVBoxLayout()
        self._widget.setLayout(self._layout)

    def show(self) -> None:
        app = QApplication(sys.argv)
        self._init_gui()
        self._widget.show()
        sys.exit(app.exec_())
