from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import QLabel, QLineEdit, QSizePolicy, QVBoxLayout, QWidget

from src.gui.email_editor.email_body.email_body_c1 import EmailBodyC1
from src.gui.email_editor.email_editor import EmailEditor
from src.gui.email_editor.tool_bar.toolbar_c1 import ToolBarC1
from src.gui.email_editor.variable_lister.variable_lister import VariableLister


class EmailEditorC1(EmailEditor):
    """
    i. Title
    A. Subject
    B. Toolbar
    C. Body
    D. variables

    """

    def __init__(self):
        self._init_gui()
        self._variables = []

    def _init_gui(self):
        self.widget = QWidget()
        self._layout = QVBoxLayout()
        self._layout.setSpacing(0)
        self.widget.setLayout(self._layout)

        # i title
        self._title_label = QLabel(text="Edit Email Message")
        self._title_label.setStyleSheet(
            "QLabel { font-size: 12px; font-weight: bold; }"
        )
        self._layout.addWidget(self._title_label)
        # A. Subject
        self._subject_edit = QLineEdit()
        font = QFont("Arial", 10)
        self._subject_edit.setFont(font)

        self._subject_edit.setPlaceholderText("Enter email subject...")
        self._subject_edit.setStyleSheet("border: 1px solid #ccc; padding: 5px;")
        self._layout.addWidget(self._subject_edit)

        # B. Toolbar
        self._tool_bar = ToolBarC1()
        self._layout.addWidget(self._tool_bar.widget)

        # C. Body
        self._body_editor = EmailBodyC1()
        self._layout.addWidget(self._body_editor.widget, stretch=1)
        # D. variables
        self._variable_list = VariableLister()
        self._variable_list.widget.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed
        )

        # self._variable_list.setReadOnly(True)
        # self._variable_list.setHtml("<p><strong>Available variables:</strong></p>")
        self._layout.addWidget(self._variable_list.widget, stretch=0)

        self._handle_events()

    def _handle_events(self):
        self._tool_bar.bold_action_triggered.connect(self._body_editor.apply_bold)
        self._tool_bar.italic_action_triggered.connect(self._body_editor.apply_italic)
        self._tool_bar.underline_action_triggered.connect(
            self._body_editor.apply_underline
        )
        self._tool_bar.change_font_size_triggered.connect(
            self._body_editor.change_font_size
        )

    def set_variables(self, variables: List[str]):
        self._variable_list.set_variables(variables)

    def get_body_html(self) -> str:
        return self._body_editor.get_html()

    def get_subject(self) -> str:
        return self._subject_edit.text()
