from PyQt5.QtCore import QEvent, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QKeyEvent, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget


class EmailBodyC1:
    def __init__(self):
        self.widget = QTextEdit()

        self._text_edit = self.widget

        self.key_filter = KeyPressFilter()
        self._text_edit.installEventFilter(self.key_filter)  # Install the event filter
        self.key_filter.characterTyped.connect(self._on_character_typed)

        self._text_edit.setAcceptRichText(True)
        self._text_edit.setStyleSheet("border: 1px solid #ccc; padding: 5px;")

    def apply_bold(self):
        cursor = self._text_edit.textCursor()
        cursor.mergeCharFormat(self._create_char_format(weight=QFont.Weight.Bold))
        self._text_edit.setTextCursor(cursor)

    def apply_italic(self):
        cursor = self._text_edit.textCursor()
        cursor.mergeCharFormat(self._create_char_format(italic=True))
        self._text_edit.setTextCursor(cursor)

    def apply_underline(self):
        cursor = self._text_edit.textCursor()
        cursor.mergeCharFormat(self._create_char_format(underline=True))
        self._text_edit.setTextCursor(cursor)

    def change_font_size(self, font_size: str):
        selected_size = font_size
        cursor = self._text_edit.textCursor()
        format = cursor.charFormat()
        format.setFontPointSize(
            int(selected_size[:-2])
        )  # Remove "pt" and convert to int for font size
        cursor.setCharFormat(format)
        self._text_edit.setTextCursor(cursor)

    def _create_char_format(
        self, weight: int = None, italic: bool = None, underline: bool = None
    ):
        char_format = QTextCharFormat()
        if weight is not None:
            char_format.setFontWeight(weight)
        if italic is not None:
            char_format.setFontItalic(italic)
        if underline is not None:
            char_format.setFontUnderline(underline)
        return char_format

    def _on_character_typed(self):
        default_format = QTextCharFormat()
        default_format.setFontWeight(12)
        default_format.setFontItalic(False)
        default_format.setFontUnderline(False)
        cursor = self._text_edit.textCursor()
        cursor.mergeCharFormat(default_format)
        self._text_edit.setTextCursor(cursor)


class KeyPressFilter(QObject):
    characterTyped = pyqtSignal(str)  # Custom signal for typed characters

    def eventFilter(self, obj, event):
        if obj and isinstance(obj, QTextEdit) and event.type() == QEvent.KeyPress:
            key_event = event
            if key_event.text().isprintable():  # Check if it's a printable character
                self.characterTyped.emit(
                    key_event.text()
                )  # Emit signal for typed character
        return super().eventFilter(obj, event)
