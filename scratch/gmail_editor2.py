import re
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class GmailLikeEditor(QWidget):
    def __init__(self, root):
        super().__init__(root)

        self.setWindowTitle("Gmail-like Rich Text Editor")

        # List of variables
        self.variables = []

        # Create a QLineEdit for the email subject
        self.subject_edit = QLineEdit(self)
        self.subject_edit.setPlaceholderText("Enter email subject...")
        self.subject_edit.setStyleSheet("border: 1px solid #ccc; padding: 5px;")

        # Create the QTextEdit for rich text editing (email body)
        self.text_edit = QTextEdit(self)
        self.text_edit.setAcceptRichText(True)
        self.text_edit.setStyleSheet("border: 1px solid #ccc; padding: 5px;")

        # Set up the toolbar for text formatting
        self.toolbar = QToolBar(self)

        # Add actions for the toolbar (bold, italic, underline, font size)
        self.bold_action = QAction("B", self)
        self.bold_action.triggered.connect(self.apply_bold)
        self.toolbar.addAction(self.bold_action)

        self.italic_action = QAction("I", self)
        self.italic_action.triggered.connect(self.apply_italic)
        self.toolbar.addAction(self.italic_action)

        self.underline_action = QAction("U", self)
        self.underline_action.triggered.connect(self.apply_underline)
        self.toolbar.addAction(self.underline_action)

        # Add font size selector dropdown to the toolbar
        self.font_size_selector = QComboBox(self)
        self.font_size_selector.addItems(["12pt", "14pt", "16pt", "18pt", "20pt"])
        self.font_size_selector.currentTextChanged.connect(self.change_font_size)
        self.toolbar.addWidget(self.font_size_selector)

        # Create a section for displaying the available variables
        self.variable_list = QTextEdit(self)
        self.variable_list.setReadOnly(True)
        self.variable_list.setHtml("<p><strong>Available variables:</strong></p>")

        # Create a layout to hold the subject editor, toolbar, text editor, and variable list
        layout = QVBoxLayout()
        layout.addWidget(self.subject_edit)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.variable_list)

        self.setLayout(layout)

        # Set up text change handler
        self.text_edit.textChanged.connect(self.handle_text_change)

    def set_variables(self, variables):
        """Set the list of variables and update the available variables section"""
        self.variables = variables
        variable_html = "<p><strong>Available variables:</strong></p>"
        for var in self.variables:
            variable_html += f"<p>{var}</p>"
        self.variable_list.setHtml(variable_html)

    def handle_text_change(self):
        """Handler for text changes to highlight variables"""
        self.highlight_variables()

    def highlight_variables(self):
        """Highlight variables in the email body and in the variable list"""
        # Get current text
        body_text = self.text_edit.toPlainText()

        # Create a cursor to manipulate text
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)

        # Reset all text to black
        default_format = QTextCharFormat()
        default_format.setForeground(QColor("black"))
        cursor.mergeCharFormat(default_format)

        # Regex pattern to find variables inside curly braces
        pattern = r"\{(.*?)\}"
        matches = re.finditer(pattern, body_text)

        # Highlight variables in the text edit
        for match in matches:
            variable_name = match.group(1)
            if variable_name in self.variables:
                start = match.start()
                end = match.end()

                # Set cursor to match range and highlight in blue
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.KeepAnchor)
                variable_format = QTextCharFormat()
                variable_format.setForeground(QColor("blue"))
                cursor.mergeCharFormat(variable_format)

        # Update the variable list colors based on usage
        variable_list_html = "<p><strong>Available variables:</strong></p>"
        for var in self.variables:
            color = "blue" if f"{{{var}}}" in body_text else "black"
            variable_list_html += f"<p style='color: {color};'>{var}</p>"
        self.variable_list.setHtml(variable_list_html)

    def apply_bold(self):
        """Apply bold text"""
        cursor = self.text_edit.textCursor()
        cursor.mergeCharFormat(self.create_char_format(weight=QFont.Weight.Bold))
        self.text_edit.setTextCursor(cursor)

    def apply_italic(self):
        """Apply italic text"""
        cursor = self.text_edit.textCursor()
        cursor.mergeCharFormat(self.create_char_format(italic=True))
        self.text_edit.setTextCursor(cursor)

    def apply_underline(self):
        """Apply underline text"""
        cursor = self.text_edit.textCursor()
        cursor.mergeCharFormat(self.create_char_format(underline=True))
        self.text_edit.setTextCursor(cursor)

    def change_font_size(self):
        """Change the font size based on the selected value in the dropdown"""
        selected_size = self.font_size_selector.currentText()
        cursor = self.text_edit.textCursor()
        format = cursor.charFormat()
        format.setFontPointSize(int(selected_size[:-2]))
        cursor.setCharFormat(format)
        self.text_edit.setTextCursor(cursor)

    def create_char_format(
        self, weight=QFont.Weight.Normal, italic=False, underline=False
    ):
        """Create a character format for text styling"""
        char_format = QTextCharFormat()
        char_format.setFontWeight(weight)
        char_format.setFontItalic(italic)
        char_format.setFontUnderline(underline)
        return char_format


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the GmailLikeEditor as a widget and display it in a window
    editor = GmailLikeEditor(None)
    editor.setWindowTitle("Gmail-like Rich Text Editor")
    editor.resize(800, 600)

    # Set some example variables
    variables = ["ABC", "DEF", "GHI", "ETC"]
    editor.set_variables(variables)

    editor.show()

    sys.exit(app.exec_())
