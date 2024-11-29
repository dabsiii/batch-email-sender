import sys
from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QFileDialog,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.event.event import Event
from src.event.event_ import Event_
from src.gui.selector.selection_display.selection_display_c1 import SelectionDisplayC1
from src.gui.selector.selector import Selector


class FolderSelector(Selector):
    """
    1. INFO TEX
    2. SELECTION DISPLAY WIDGET
    3. SELECT FILE BUTTON


    Events:
    .selected_file()

    Getters:
    .get_filepath()->Path
    """

    def __init__(
        self,
        info_text: str = "Select A Folder",
        icon_path: Path = None,
        button_text: str = "Browse",
        dialog_caption: str = "Select A Folder",
    ):

        self._info_text = info_text
        self._icon_path = icon_path
        self._button_text = button_text
        self._path: Path = None
        self._dialog_caption = dialog_caption
        self._selected = Event_()

        self._init_ui()

    def _init_ui(self):
        self.widget = QWidget()
        self.widget.setMinimumSize(300, 200)
        self._frame = QFrame(parent=self.widget)
        self._frame.setFrameShape(QFrame.StyledPanel)
        self._frame.setFixedSize(250, 120)

        self._frame_layout = QVBoxLayout()
        self._frame_layout.setSpacing(0)
        # self._frame_layout.setContentsMargins(0, 0, 0, 0)
        self._frame_layout.setAlignment(Qt.AlignTop)
        self._frame.setLayout(self._frame_layout)

        # 1
        self._info_label = QLabel(text=self._info_text)
        # self._info_label.setStyleSheet(
        #     """QLabel {padding: 0px;margin: 0px; color: red; background-color: darkgreen;}"""
        # )
        self._frame_layout.addWidget(self._info_label)
        # 2
        self._selection_display = SelectionDisplayC1()
        self._selection_display.show_no_selection()
        self._frame_layout.addWidget(
            self._selection_display.widget, alignment=Qt.AlignHCenter
        )

        # 3
        self._select_file_button = QPushButton(text=self._button_text)
        self._select_file_button.setCursor(Qt.PointingHandCursor)
        self._select_file_button.clicked.connect(self._open_directory)
        self._frame_layout.addWidget(self._select_file_button)

    @property
    def selected(self) -> Event:
        return self._selected

    def get_path(self) -> Path:
        return self._path

    def _open_directory(self):
        # Open a dialog to select a directory
        directory = QFileDialog.getExistingDirectory(
            parent=self.widget, caption=self._dialog_caption, directory=""
        )

        if directory:  # If the user selects a directory
            self._path = Path(directory)
            self._selection_display.show_selection(
                path=Path(directory), iconpath=self._icon_path
            )
        else:
            self._path = None
            self._selection_display.show_no_selection()
        self._selected.publish({"path": self._path})
