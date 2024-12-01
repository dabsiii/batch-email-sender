import sys
from pathlib import Path
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import src.resources_rc
from src.event.event import Event
from src.event.event_ import Event_
from src.gui.email_bot_gui import EmailBotGui
from src.gui.email_editor.email_editor_c1 import EmailEditorC1
from src.gui.selector.file_selector import FileSelector
from src.gui.selector.folder_selector import FolderSelector
from src.gui.toolbar.toolbar import ToolBar


class EmailBotGuiC1(EmailBotGui):
    """
    INPUTS FRAME
        A. Selectors
            A.1 Credentials
            A.2 Data
            A.3 Attachment folder
        B. Gmail Editor
        C. Send Email
    DROPDOWNS
        A. Email column
        B. Attachment column
    OUTPUTS FRAME
        E. SEND EMAIL
        D. Logger
    """

    def __init__(self):
        self._selected_credentials = Event_()
        self._selected_data = Event_()
        self._selected_folder = Event_()
        self._send_email_clicked = Event_()
        self._selected_email_column = Event_()
        self._selected_attachments_column = Event_()

    def _init_gui(self) -> None:
        self._widget = QWidget()
        self._widget.setWindowTitle("PS Batch Email Sender V1.0.1")
        logo_path = ":/images/icons/app-logo.ico"
        self._widget.setWindowIcon(QIcon(logo_path))
        self._widget.setMinimumSize(1000, 800)
        self._widget_layout = QVBoxLayout()
        self._widget.setLayout(self._widget_layout)

        # Toolbar
        self._tool_bar = ToolBar()
        self._widget_layout.addWidget(self._tool_bar.widget)

        # INPUTS FRAME
        self._input_frame = QFrame()

        # self._input_frame.setStyleSheet("QFrame {background-color: red;}")
        # self._input_frame.setFixedHeight(600)
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
            icon_path=":/images/icons/json-icon.png",
            filter="JSON Files (*.json);;All Files (*)",
        )
        self._credential_selector.selected
        self._selectors_frame_layout.addWidget(
            self._credential_selector.widget, stretch=0, alignment=Qt.AlignHCenter
        )

        # A.2 Data
        self._data_selector = FileSelector(
            info_text="Select Data File (.xlsx file)",
            icon_path=":/images/icons/xlsx-icon.png",
            filter="Excel Files (*.xls *.xlsx);;All Files (*)",
        )
        self._selectors_frame_layout.addWidget(
            self._data_selector.widget, stretch=0, alignment=Qt.AlignHCenter
        )

        # 3 Attachment Folder
        self._attachment_folder_selector = FolderSelector(
            info_text="Select Attachments Folder",
            icon_path=":/images/icons/folder-icon.jpg",
        )
        self._selectors_frame_layout.addWidget(
            self._attachment_folder_selector.widget,
            stretch=0,
            alignment=Qt.AlignHCenter,
        )

        # B. Gmail Editor
        self._email_editor = EmailEditorC1()
        self._input_frame_layout.addWidget(self._email_editor.widget)

        # DROPDOWNS
        self._dropdowns_container = QWidget()
        dropdown_layout = QFormLayout()
        self._dropdowns_container.setLayout(dropdown_layout)

        # Email Column dropdown
        self._email_column_menu = QComboBox()
        self._email_column_menu.setMinimumWidth(100)
        self._email_column_menu.setCursor(Qt.OpenHandCursor)
        self._email_column_menu.currentIndexChanged.connect(
            self._selected_email_column.publish
        )
        dropdown_layout.addRow("Email Address Column:", self._email_column_menu)
        self._selectors_frame_layout.addWidget(
            self._dropdowns_container,
            # alignment=Qt.AlignHCenter
        )

        # Email Column dropdown
        self._attachments_column_menu = QComboBox()
        self._attachments_column_menu.setMinimumWidth(100)
        self._attachments_column_menu.setCursor(Qt.OpenHandCursor)
        self._attachments_column_menu.currentIndexChanged.connect(
            self._selected_attachments_column.publish
        )
        dropdown_layout.addRow("Attachments Column:", self._attachments_column_menu)
        self._selectors_frame_layout.addWidget(
            self._dropdowns_container,
            # alignment=Qt.AlignHCenter
        )

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

    @property
    def selected_email_column(self) -> Event:
        return self._selected_email_column

    @property
    def selected_attachments_column(self) -> Event:
        return self._selected_attachments_column

    def get_credentials_path(self) -> Path:
        return self._credential_selector.get_path()

    def get_data_path(self) -> Path:
        return self._data_selector.get_path()

    def get_attachment_folder_path(self) -> Path:
        return self._attachment_folder_selector.get_path()

    def update_variables(self, variables: List[str]) -> None:
        self._email_editor.set_variables(variables)
        self._set_email_columns_options(variables)
        self._set_attachments_columns_options(variables)

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

    def _set_email_columns_options(self, options: List[str]) -> None:
        self._email_column_menu.clear()
        self._email_column_menu.addItems(options)
        self._email_column_menu.setCurrentIndex(-1)

    def _set_attachments_columns_options(self, options: List[str]) -> None:
        self._attachments_column_menu.clear()
        self._attachments_column_menu.addItems(options)
        self._attachments_column_menu.setCurrentIndex(-1)

    def get_email_column(self) -> str:
        return self._email_column_menu.currentText()

    def get_attachments_column(self) -> str:
        return self._attachments_column_menu.currentText()

    def log(self, message: str) -> None:
        self._logger.append(message)
        self._logger.moveCursor(QTextCursor.End)
