import sys
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SelectionDisplay(QWidget):
    """
    ICON
    PATH Display
    """

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self._display_widget = QWidget(self)

        # Layout for the widget
        self._display_widget_layout = QHBoxLayout()
        self._display_widget.setLayout(self._display_widget_layout)

        self._icon_label = QLabel(text="file icon image")
        self._display_widget_layout.addWidget(self._icon_label)

        self._path_display_frame = QFrame()
        # self._path_display_frame.setFrameShape(QFrame.Box)
        # self._path_display_frame.setFrameShadow(QFrame.Raised)
        self._path_display_frame_layout = QVBoxLayout()
        self._path_display_frame.setLayout(self._path_display_frame_layout)
        self._display_widget_layout.addWidget(self._path_display_frame)

        # Text box to display the file path
        self.file_path_box = QLineEdit()
        self.file_path_box.setPlaceholderText("file path")
        self._path_display_frame_layout.addWidget(self.file_path_box)

        # Text box to display the file path
        self.file_name_box = QLineEdit()
        self.file_name_box.setPlaceholderText("file name")
        self._path_display_frame_layout.addWidget(self.file_name_box)

    def _set_file_path(self, filepath: Path):
        self.show()
        self.file_path_box.setText(filepath.as_posix())
        self.file_name_box.setText(filepath.name)
        print(f"file path set: {filepath}")

    def _set_icon(self, icon_path: Path):
        print(f"icon set: {icon_path}")

    def show_no_selection(self) -> None:
        print("Hello")

    def show_selection(self, filepath: Path, icon_path: Path = None):
        if filepath:
            self._set_file_path(filepath)
            self._set_icon(icon_path)
        else:
            self._show_no_selection()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SelectionDisplay()
    widget.show()
    sys.exit(app.exec_())
