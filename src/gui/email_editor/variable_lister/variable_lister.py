from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class VariableLister:
    def __init__(self):
        self.widget = QWidget()
        self._init_ui()

    def _init_ui(self):
        # Set minimum height for the widget
        self.widget.setMinimumHeight(200)
        # self.widget.setStyleSheet("background-color: pink;")

        # Main layout for the widget
        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(5, 5, 5, 5)
        self._main_layout.setSpacing(0)  # Remove spacing for compactness
        self.widget.setLayout(self._main_layout)

        # Frame to encapsulate everything
        self._frame = QFrame()
        # self._frame.setStyleSheet(
        #     "QFrame { border: 2px solid #ccc; border-radius: 5px; background-color: #f9f9f9; }"
        # )
        self._frame_layout = QVBoxLayout()
        self._frame_layout.setContentsMargins(5, 5, 5, 5)
        self._frame_layout.setSpacing(0)
        self._frame.setLayout(self._frame_layout)
        self._main_layout.addWidget(self._frame)

        # Add title at the top of the frame
        self._title_label = QLabel("Variables")
        self._title_label.setStyleSheet(
            "QLabel { font-size: 12px; font-weight: bold; }"
        )
        self._title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._frame_layout.addWidget(self._title_label, alignment=Qt.AlignTop)

        # Grid layout to display variables
        self._grid_layout = QGridLayout()
        self._grid_layout.setSpacing(5)
        self._grid_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Remove margins for compactness
        self._frame_layout.addLayout(self._grid_layout)

        # Spacer to push the grid layout to the top
        self._frame_layout.addStretch()

    def set_variables(self, variables: List[str]) -> None:
        """Populate the grid with labels or buttons for each variable."""

        # Clear existing widgets in the grid layout
        while self._grid_layout.count():
            child = self._grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Populate grid with variable labels or buttons
        for i, variable in enumerate(variables):
            row, col = divmod(i, 3)  # Adjust number of columns for compactness
            button = QPushButton(variable)
            button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            button.setMinimumSize(80, 30)  # Set a minimum size for each button
            button.setStyleSheet(
                "QPushButton { padding: 2px; border: 1px solid #ccc; border-radius: 3px; }"
            )
            self._grid_layout.addWidget(button, row, col)


# Example usage
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    lister = VariableLister()
    lister.set_variables(["Variable 1", "Variable 2", "Variable 3", "Variable 4"])
    lister.widget.show()
    app.exec_()
