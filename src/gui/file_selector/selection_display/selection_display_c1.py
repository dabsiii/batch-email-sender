import sys
from pathlib import Path

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.gui.file_selector.selection_display.selection_display import SelectionDisplay


class SelectionDisplayC1(SelectionDisplay):
    """
    A
        A.1 ICON
        A.2 PATH Display
            A.2.1 Filename
            A.2.2 Filepath
    B. NO SELECTION DISPLAY
    """

    def __init__(self):

        self.widget = QWidget()
        # self.widget.setStyleSheet("color: red;background-color: lightblue;}")
        self.widget.setMinimumSize(200, 80)
        self._init_ui()

    def _init_ui(self) -> None:
        self._stacked_widget = QStackedWidget(parent=self.widget)
        # A
        self._display = QFrame()
        self._display_layout = QHBoxLayout()
        self._display.setLayout(self._display_layout)
        self._stacked_widget.addWidget(self._display)
        # A.1
        self._icon_label = QLabel(text=" ICON.jpg")
        self._display_layout.addWidget(self._icon_label)
        # A.2
        self._path_display_frame = QFrame()
        self._path_display_frame_layout = QVBoxLayout()
        self._path_display_frame_layout.setContentsMargins(0, 0, 0, 0)
        self._path_display_frame.setLayout(self._path_display_frame_layout)
        self._display_layout.addWidget(self._path_display_frame)
        # A.2.1
        self._file_name_line = QLineEdit()
        self._path_display_frame_layout.addWidget(self._file_name_line)

        # A.2.2
        self._file_path_line = QLineEdit()
        self._path_display_frame_layout.addWidget(self._file_path_line)

        # B
        self._no_selection = QWidget()
        self._no_selection_layout = QVBoxLayout()
        self._no_selection.setLayout(self._no_selection_layout)
        self._stacked_widget.addWidget(self._no_selection)

        self._no_selection_label = QLabel(text=" No Selection")
        self._no_selection_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._no_selection_label.setStyleSheet(
            "QLabel {background-color:lightgray; text-align: center;}"
        )

        self._no_selection_layout.addWidget(
            self._no_selection_label, alignment=Qt.AlignHCenter, stretch=1
        )

    def show_selection(self, path: Path, iconpath: Path = None) -> None:

        self._stacked_widget.setCurrentIndex(0)
        self._file_path_line.setText(path.as_posix())
        self._file_name_line.setText(path.name)

    def show_no_selection(self) -> None:
        print("layout changed to no selection")
        self._stacked_widget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SelectionDisplay()
    widget.show()
    sys.exit(app.exec_())
