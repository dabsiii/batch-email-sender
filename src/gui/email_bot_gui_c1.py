import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget

from src.gui.email_bot_gui import EmailBotGui
from src.gui.email_editor.email_editor_c1 import EmailEditorC1
from src.gui.selector.file_selector import FileSelector
from src.gui.selector.folder_selector import FolderSelector


class EmailBotGuiC1(EmailBotGui):
    """
    A. Selectors
        A.1 Credentials
        A.2 Data
        A.3 Attachment folder
    B. Gmail Editor
    C. Send Email
    """

    def __init__(self):
        pass

    def _init_gui(self) -> None:
        self._widget = QWidget()
        self._widget_layout = QHBoxLayout()
        self._widget.setLayout(self._widget_layout)

        # A Selectors
        self._selectors_frame = QFrame()
        self._selectors_frame_layout = QVBoxLayout()
        self._selectors_frame.setLayout(self._selectors_frame_layout)
        self._widget_layout.addWidget(self._selectors_frame)

        # A.1 Credentials
        self._credential_selector = FileSelector(
            info_text="Import Credentials (.json file)",
            icon_path=Path("assets\\json-icon.png").resolve(),
            filter="JSON Files (*.json);;All Files (*)",
        )
        self._selectors_frame_layout.addWidget(self._credential_selector.widget)

        # A.2 Data
        self._data_selector = FileSelector(
            info_text="Select a data file (.xlsx file)",
            icon_path=Path("assets\\xlsx-icon.png").resolve(),
            filter="Excel Files (*.xls *.xlsx);;All Files (*)",
        )
        self._selectors_frame_layout.addWidget(self._data_selector.widget)

        # 3 Attachment Folder
        self._attachment_folder_selector = FolderSelector(
            info_text="Select a Folder containing the attachment",
            icon_path=Path("assets\\folder-icon.jpg").resolve(),
        )
        self._selectors_frame_layout.addWidget(self._attachment_folder_selector.widget)

        # B. Gmail Editor
        self._email_editor = EmailEditorC1()
        self._widget_layout.addWidget(self._email_editor.widget)

    def show(self) -> None:
        app = QApplication(sys.argv)
        self._init_gui()
        self._widget.show()
        sys.exit(app.exec_())
