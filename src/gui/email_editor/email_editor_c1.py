from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QTextEdit, QVBoxLayout, QWidget

from src.gui.email_editor.email_body.email_body_c1 import EmailBodyC1
from src.gui.email_editor.email_editor import EmailEditor
from src.gui.email_editor.tool_bar.toolbar_c1 import ToolBarC1
from src.gui.email_editor.variable_lister.variable_lister import VariableLister


class EmailEditorC1(EmailEditor):
    """
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

    def set_variables(self, variables: List[str]): ...

    def get_body_html(self) -> str: ...

    def get_subject(self) -> str: ...
