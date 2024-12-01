from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
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


class SelectionDisplayC1:
    def __init__(self):

        # self.widget.setMinimumSize(300, 80)
        # self.widget.setStyleSheet("background-color: #f9f9f9;")
        self._init_ui()

    def _init_ui(self) -> None:
        self.widget = QWidget()
        self._widget_layout = QVBoxLayout()
        self.widget.setLayout(self._widget_layout)

        self._stacked_widget = QStackedWidget()
        self._widget_layout.addWidget(self._stacked_widget)

        # A: Selection Display
        self._display = QFrame()
        self._display.setStyleSheet("background-color: white;")
        self._display_layout = QHBoxLayout()
        self._display_layout.setContentsMargins(0, 0, 0, 0)
        self._display.setLayout(self._display_layout)
        self._stacked_widget.addWidget(self._display)

        # A.1: Icon
        self._icon_label = QLabel()
        # self._icon_label.setFixedSize(48, 48)
        self._icon_label.setStyleSheet(" background-color: white; border-radius: 4px;")
        self._display_layout.addWidget(self._icon_label, stretch=0)

        # A.2: Path Display
        self._path_display_frame = QFrame()
        self._path_display_frame_layout = QVBoxLayout()
        self._path_display_frame_layout.setContentsMargins(5, 0, 0, 0)
        self._path_display_frame.setLayout(self._path_display_frame_layout)
        self._display_layout.addWidget(self._path_display_frame, stretch=1)

        # A.2.1: Filename
        self._file_name_line = QLineEdit()
        self._file_name_line.setMinimumWidth(200)
        self._file_name_line.setReadOnly(True)
        self._file_name_line.setAlignment(Qt.AlignLeft)
        self._file_name_line.setStyleSheet(
            "QLineEdit {  border: None;font-size: 12px; font-weight: bold; }"
        )
        self._path_display_frame_layout.addWidget(self._file_name_line)

        # A.2.2: Filepath
        self._file_path_line = QLineEdit()
        self._file_path_line.setReadOnly(True)
        self._file_path_line.setAlignment(Qt.AlignLeft)
        self._path_display_frame_layout.addWidget(self._file_path_line)

        # B: No Selection Display
        self._no_selection = QWidget()
        self._no_selection_layout = QVBoxLayout()
        self._no_selection_layout.setContentsMargins(0, 0, 0, 0)
        self._no_selection.setLayout(self._no_selection_layout)
        self._no_selection.setStyleSheet("background-color: #f1f1f1;")
        self._stacked_widget.addWidget(self._no_selection)

        self._no_selection_label = QLabel("No Selection")
        self._no_selection_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._no_selection_label.setAlignment(Qt.AlignCenter)
        self._no_selection_label.setStyleSheet("color: #666; font-size: 12px;")
        self._no_selection_layout.addWidget(
            self._no_selection_label, alignment=Qt.AlignCenter
        )

    def show_selection(self, path: Path, iconpath: str = None) -> None:
        self._stacked_widget.setCurrentIndex(0)
        self._file_path_line.setText(path.as_posix())
        self._file_path_line.setCursorPosition(0)
        self._file_name_line.setText(path.name)
        self._file_name_line.setCursorPosition(0)

        if iconpath is not None:
            pixmap = QPixmap(iconpath)
            self._icon_label.setPixmap(
                pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            self._icon_label.setScaledContents(True)

    def show_no_selection(self) -> None:
        self._stacked_widget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication([])
    display = SelectionDisplayC1()
    display.widget.show()
    app.exec_()
