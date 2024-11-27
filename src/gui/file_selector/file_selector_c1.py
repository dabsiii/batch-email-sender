import sys
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from gui.file_selector.selection_display.selection_display import SelectionDisplay

from src.gui.file_selector.file_selector import FileSelectorWidget


class FileSelectorWidgetC1(FileSelectorWidget, QWidget):
    """
    INFO TEX
    SELECTION DISPLAY WIDGET
    SELECT FILE BUTTON


    Events:
    .selected_file()

    Getters:
    .get_filepath()->Path
    """

    def __init__(
        self,
        info_text: str,
        icon_path: path,
    ):
        super().__init__()
        self._init_ui()
        self._info_text = info_text
        self._icon_path = icon_path

    def _init_ui(self):

        # Layout for the widget
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._frame = QFrame()
        self._frame.setFrameShape(QFrame.Box)
        self._frame.setFrameShadow(QFrame.Raised)
        self._layout.addWidget(self._frame)

        self._frame_layout = QVBoxLayout()
        self._frame.setLayout(self._frame_layout)
        # Info
        self._info = QLabel(text="Select a file .json")
        self._frame_layout.addWidget(self._info)

        # Text box to display the file path
        self._selection_display = SelectionDisplay()
        self._frame_layout.addWidget(self._selection_display)

        # Button to open file dialog
        self.select_button = QPushButton(text="Select File")
        self.select_button.clicked.connect(self._open_file_dialog)
        self._frame_layout.addWidget(self.select_button)

    def _open_file_dialog(self):
        # Open file dialog and get selected file path
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a File", "", "All Files (*)"
        )
        if file_path:
            self._selection_display.show_selection(
                Path(file_path), icon_path="sample icon path"
            )
        else:
            self._selection_display.show_no_selection()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = FileSelectorWidget()
    widget.show()
    sys.exit(app.exec_())
