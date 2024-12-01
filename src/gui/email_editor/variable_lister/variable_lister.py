from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

MESSAGE = """

You can personalize your email content by using variables enclosed in curly braces {}. 
Each variable corresponds to a column in your data file, 
and its value will change based on the record being processed.

Guidelines:
Variable Names: Ensure the variable names (inside {}) exactly match the column headers in your data file (case-sensitive).

Placeholder Usage:
Use {ColumnName} wherever you want the corresponding value to appear in the email.

Example:
If your data file looks like this:

Name    |Email                             |Greeting
---------------------------------------
Alice      | alice@example.com    | Hello Alice
Bob        | bob@example.com     | Hello Bob

You can write your email template as:

Subject: Welcome, {Name}!
Body: Hi {Name}, your message is: {Greeting}.
The placeholders (e.g., {Name}, {Greeting}) will automatically be replaced with the corresponding values from your data file for each recipient.

Output:

For Alice:
Subject: Welcome, Alice!
Body: Hi Alice, your message is: Hello Alice. 

For Bob:
Subject: Welcome, Bob!
Body: Hi Bob, your message is: Hello Bob.


"""


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
        self._title_label.setCursor(Qt.PointingHandCursor)  # Change cursor to hand
        self._title_label.mousePressEvent = self._on_title_label_clicked
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
            # button.setStyleSheet(" ")
            button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            button.setMinimumSize(80, 30)  # Set a minimum size for each button
            button.setStyleSheet(
                "QPushButton { padding: 2px; border: 1px solid #ccc; border-radius: 3px;background-color: lightblue ; }"
            )
            self._grid_layout.addWidget(button, row, col)

    def _on_title_label_clicked(self, event):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("How to Use Variables")
        msg_box.setText(MESSAGE)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.exec_()
