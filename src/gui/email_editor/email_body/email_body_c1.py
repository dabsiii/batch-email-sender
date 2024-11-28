from typing import List

from PyQt5.QtGui import QFont, QTextCharFormat
from PyQt5.QtWidgets import QTextEdit, QWidget

from src.gui.email_editor.email_body.email_body import EmailBody


class EmailBodyC1(EmailBody):
    def __init__(self):
        self.widget = QTextEdit()

        self._text_edit = self.widget
        self._text_edit.setAcceptRichText(True)
        self._text_edit.setStyleSheet("border: 1px solid #ccc; padding: 5px;")

    def apply_bold(self) -> None:
        cursor = self._text_edit.textCursor()
        cursor.mergeCharFormat(self._create_char_format(weight=QFont.Weight.Bold))
        self._text_edit.setTextCursor(cursor)

    def apply_italic(self) -> None:
        cursor = self._text_edit.textCursor()
        cursor.mergeCharFormat(self._create_char_format(italic=True))
        self._text_edit.setTextCursor(cursor)

    def apply_underline(self) -> None:
        cursor = self._text_edit.textCursor()
        cursor.mergeCharFormat(self._create_char_format(underline=True))
        self._text_edit.setTextCursor(cursor)

    def change_font_size(self, fontsize: str) -> None:
        selected_size = fontsize
        cursor = self._text_edit.textCursor()
        format = cursor.charFormat()
        format.setFontPointSize(int(selected_size[:-2]))
        cursor.setCharFormat(format)
        self._text_edit.setTextCursor(cursor)

    def _create_char_format(
        self, weight=QFont.Weight.Normal, italic=False, underline=False
    ):
        """Create a character format for text styling"""
        char_format = QTextCharFormat()
        char_format.setFontWeight(weight)
        char_format.setFontItalic(italic)  # Use setFontItalic to apply italic
        char_format.setFontUnderline(underline)  # Use setFontUnderline for underline
        return char_format

    def highlight_variables(self, variables: List[str]): ...

    def get_html(self): ...
