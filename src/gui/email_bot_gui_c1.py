import sys
from pathlib import Path
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.event.event import Event
from src.event.event_ import Event_
from src.gui.email_bot_gui import EmailBotGui
from src.gui.email_editor.email_editor_c1 import EmailEditorC1
from src.gui.selector.file_selector import FileSelector
from src.gui.selector.folder_selector import FolderSelector


class EmailBotGuiC1(EmailBotGui):
    """
    INPUTS FRAME
        A. Selectors
            A.1 Credentials
            A.2 Data
            A.3 Attachment folder
        B. Gmail Editor
        C. Send Email
    OUTPUTS FRAME
        D. Logger
        E. SEND EMAIL
    """

    def __init__(self):
        self._selected_credentials = Event_()
        self._selected_data = Event_()
        self._selected_folder = Event_()
        self._send_email_clicked = Event_()

    def _init_gui(self) -> None:
        self._widget = QWidget()
        self._widget.setWindowTitle("PS Batch Email Sender V1.0")
        logo_path = Path("assets\\app-logo.ico").resolve()
        self._widget.setWindowIcon(QIcon(logo_path.as_posix()))
        self._widget.setMinimumSize(1000, 400)
        self._widget_layout = QVBoxLayout()
        self._widget.setLayout(self._widget_layout)

        # INPUTS FRAME
        self._input_frame = QFrame()

        # self._input_frame.setStyleSheet("QFrame {background-color: red;}")
        self._input_frame.setFixedHeight(600)
        self._input_frame_layout = QHBoxLayout()
        self._input_frame_layout.setContentsMargins(0, 0, 0, 0)

        self._input_frame.setLayout(self._input_frame_layout)
        self._widget_layout.addWidget(self._input_frame)

        # A Selectors
        self._selectors_frame = QFrame()
        self._selectors_frame.setFixedWidth(300)
        # self._selectors_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self._selectors_frame.setStyleSheet("QFrame {background-color: blue;}")

        self._selectors_frame_layout = QVBoxLayout()
        self._selectors_frame_layout.setSpacing(0)
        # self._selectors_frame_layout.setStretch(0, 1)
        self._selectors_frame_layout.setContentsMargins(0, 0, 0, 0)
        self._selectors_frame_layout.setAlignment(Qt.AlignHCenter)
        self._selectors_frame.setLayout(self._selectors_frame_layout)
        self._input_frame_layout.addWidget(self._selectors_frame, stretch=1)

        # A.1 Credentials
        self._credential_selector = FileSelector(
            info_text="Import Sender Credentials (.json file)",
            icon_path=Path("assets\\json-icon.png").resolve(),
            filter="JSON Files (*.json);;All Files (*)",
        )
        self._credential_selector.selected
        self._selectors_frame_layout.addWidget(
            self._credential_selector.widget, stretch=0, alignment=Qt.AlignHCenter
        )

        # A.2 Data
        self._data_selector = FileSelector(
            info_text="Select Data File (.xlsx file)",
            icon_path=Path("assets\\xlsx-icon.png").resolve(),
            filter="Excel Files (*.xls *.xlsx);;All Files (*)",
        )
        self._selectors_frame_layout.addWidget(
            self._data_selector.widget, stretch=0, alignment=Qt.AlignHCenter
        )

        # 3 Attachment Folder
        self._attachment_folder_selector = FolderSelector(
            info_text="Select Attachments Folder",
            icon_path=Path("assets\\folder-icon.jpg").resolve(),
        )
        self._selectors_frame_layout.addWidget(
            self._attachment_folder_selector.widget,
            stretch=0,
            alignment=Qt.AlignHCenter,
        )

        # B. Gmail Editor
        self._email_editor = EmailEditorC1()
        self._input_frame_layout.addWidget(self._email_editor.widget)

        # OUTPUTS FRAME
        self._output_frame = QFrame()
        self._output_frame_layout = QVBoxLayout()
        self._output_frame.setLayout(self._output_frame_layout)
        self._widget_layout.addWidget(self._output_frame)

        # E. send email button
        self._send_email_button = QPushButton(text="send email")
        self._send_email_button.setDisabled(True)
        self._send_email_button.setStyleSheet("background-color: lightgray;")
        self._send_email_button.setFixedSize(300, 50)
        self._send_email_button.setCursor(Qt.PointingHandCursor)
        self._send_email_button.clicked.connect(self._send_email_clicked.publish)
        self._output_frame_layout.addWidget(
            self._send_email_button, alignment=Qt.AlignHCenter
        )
        # Logger
        self._logger = QTextEdit()
        self._logger.setStyleSheet("background-color: gray; color: lightgreen;")
        self._logger.setReadOnly(True)  # Make it read-only
        self._logger.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self._output_frame_layout.addWidget(self._logger)

        self._handle_events()

    def _handle_events(self) -> None:
        self._credential_selector.selected.subscribe(self._selected_credentials.publish)
        self._data_selector.selected.subscribe(self._selected_data.publish)
        self._attachment_folder_selector.selected.subscribe(
            self._selected_folder.publish
        )

    def show(self) -> None:
        app = QApplication(sys.argv)
        self._init_gui()
        self._widget.show()
        sys.exit(app.exec_())

    @property
    def selected_credentials(self) -> Event:
        return self._selected_credentials

    @property
    def selected_data(self) -> Event:
        return self._selected_data

    @property
    def selected_folder(self) -> Event:
        return self._selected_folder

    @property
    def send_email_clicked(self) -> Event:
        return self._send_email_clicked

    def get_credentials_path(self) -> Path:
        return self._credential_selector.get_path()

    def get_data_path(self) -> Path:
        return self._data_selector.get_path()

    def get_attachment_folder_path(self) -> Path:
        return self._attachment_folder_selector.get_path()

    def update_variables(self, variables: List[str]) -> None:
        self._email_editor.set_variables(variables)

    def get_email_body_html(self) -> str:
        return self._email_editor.get_body_html()

    def get_email_subject(self) -> str:
        return self._email_editor.get_subject()

    def disable_send_email(self) -> str:
        self._send_email_button.setDisabled(True)
        self._send_email_button.setStyleSheet("background-color: lightgray;")

    def enable_send_email(self) -> str:
        self._send_email_button.setEnabled(True)
        self._send_email_button.setStyleSheet("background-color: blue;")

    def log(self, message: str) -> None:
        self._logger.append(message)
