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

from src.gui.selector.selection_display.selection_display_c1 import SelectionDisplayC1
from src.gui.selector.selector import Selector


class FileSelector(Selector):
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
        info_text: str = "Select A File",
        icon_path: Path = None,
        filter: str = "All Files (*)",
        button_text: str = "Browse",
        dialog_caption: str = "Select A File",
    ):

        self.widget = QWidget()
        self.widget.setMinimumSize(300, 200)
        self._info_text = info_text
        self._icon_path = icon_path
        self._filter = filter
        self._button_text = button_text
        self._path: Path = None
        self._dialog_caption: str = dialog_caption
        self._init_ui()

    def _init_ui(self):
        self._frame = QFrame(parent=self.widget)
        self._frame.setFrameShape(QFrame.StyledPanel)
        self._frame.setGeometry(50, 50, 250, 140)

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
        self._frame_layout.addWidget(self._selection_display.widget)

        # 3
        self._select_file_button = QPushButton(text=self._button_text)
        self._select_file_button.setCursor(Qt.PointingHandCursor)
        self._select_file_button.clicked.connect(self._open_file_dialog)
        self._frame_layout.addWidget(self._select_file_button)

    def selected(self) -> pyqtSignal: ...

    def get_path(self) -> Path:
        return self._path()

    def _open_file_dialog(self):
        # Open file dialog and get selected file path
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self.widget,
            caption=self._dialog_caption,
            directory="",
            filter=self._filter,
        )
        if file_path:
            self._path = Path(file_path)
            self._selection_display.show_selection(
                path=Path(file_path), iconpath=self._icon_path
            )

        else:
            self._path = None
            self._selection_display.show_no_selection()