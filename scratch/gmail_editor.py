import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCharFormat
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
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

        # Create a QLineEdit for the email subject
        self.subject_edit = QLineEdit(self)
        self.subject_edit.setPlaceholderText("Enter email subject...")
        self.subject_edit.setStyleSheet(
            "border: 1px solid #ccc; padding: 5px;"
        )  # Outline for subject

        # Create the QTextEdit for rich text editing (email body)
        self.text_edit = QTextEdit(self)
        self.text_edit.setAcceptRichText(True)  # Enable rich text editing (HTML)
        self.text_edit.setHtml(
            "<html><body contenteditable='true'><p>Edit your email body here...</p></body></html>"
        )
        self.text_edit.setStyleSheet(
            "border: 1px solid #ccc; padding: 5px;"
        )  # Outline for body

        # Set up placeholder text logic
        self.text_edit.textChanged.connect(self.check_empty_body)

        # Create a toolbar for text formatting
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
        self.font_size_selector.addItems(
            ["12pt", "14pt", "16pt", "18pt", "20pt"]
        )  # Predefined sizes
        self.font_size_selector.currentTextChanged.connect(self.change_font_size)
        self.toolbar.addWidget(self.font_size_selector)

        # Add a layout to hold the subject editor, toolbar, and text editor
        layout = QVBoxLayout()
        layout.addWidget(self.subject_edit)  # Add the subject editor
        layout.addWidget(self.toolbar)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def check_empty_body(self):
        """Hide the placeholder text when the user starts typing."""
        text = self.text_edit.toPlainText().strip()

        # Temporarily disconnect the signal to prevent recursion
        self.text_edit.textChanged.disconnect(self.check_empty_body)

        if not text:
            # Restore placeholder text if the body is empty
            self.text_edit.setHtml(
                "<html><body contenteditable='true'><p>Edit your email body here...</p></body></html>"
            )
        elif "Edit your email body here..." in text:
            # If the user deletes the text and leaves the placeholder, reset it to empty
            self.text_edit.setHtml("<html><body contenteditable='true'></body></html>")

        # Reconnect the signal after updating the text
        self.text_edit.textChanged.connect(self.check_empty_body)

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
        selected_size = (
            self.font_size_selector.currentText()
        )  # Get the selected font size as text (e.g., "16pt")
        cursor = self.text_edit.textCursor()
        format = cursor.charFormat()
        format.setFontPointSize(
            int(selected_size[:-2])
        )  # Remove "pt" and convert to int for font size
        cursor.setCharFormat(format)
        self.text_edit.setTextCursor(cursor)

    def create_char_format(
        self, weight=QFont.Weight.Normal, italic=False, underline=False
    ):
        """Create a character format for text styling"""
        char_format = QTextCharFormat()
        char_format.setFontWeight(weight)
        char_format.setFontItalic(italic)  # Use setFontItalic to apply italic
        char_format.setFontUnderline(underline)  # Use setFontUnderline for underline
        return char_format

    def get_body_html(self) -> str:
        """Return the body content as HTML"""
        return self.text_edit.toHtml()

    def get_subject(self) -> str:
        """Return the subject content as plain text"""
        return self.subject_edit.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the GmailLikeEditor as a widget and display it in a window
    editor = GmailLikeEditor(None)
    editor.setWindowTitle("Gmail-like Rich Text Editor")
    editor.resize(800, 600)
    editor.show()

    sys.exit(app.exec_())
