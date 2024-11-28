from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction, QComboBox, QToolBar

from src.gui.email_editor.tool_bar.toolbar import Toolbar


class ToolBarC1(Toolbar):
    """
    BOLD
    ITALIC
    UNDERLINE
    FONTSIZE
    """

    def __init__(self):
        # Set up the toolbar for text formatting
        self.widget = QToolBar()

        # Add actions for the toolbar (bold, italic, underline, font size)
        self._bold_action = QAction("B")
        # self.bold_action.triggered.connect(self.apply_bold)
        self.widget.addAction(self._bold_action)

        self._italic_action = QAction("I")
        # self.italic_action.triggered.connect(self.apply_italic)
        self.widget.addAction(self._italic_action)

        self._underline_action = QAction("U")
        # self.underline_action.triggered.connect(self.apply_underline)
        self.widget.addAction(self._underline_action)

        # Add font size selector dropdown to the toolbar
        self._font_size_selector = QComboBox()
        self._font_size_selector.addItems(["12pt", "14pt", "16pt", "18pt", "20pt"])
        # self.font_size_selector.currentTextChanged.connect(self.change_font_size)
        self.widget.addWidget(self._font_size_selector)

    @property
    def bold_action_triggered(self) -> pyqtSignal:
        return self._bold_action.triggered

    @property
    def italic_action_triggered(self) -> pyqtSignal:
        return self._italic_action.triggered

    @property
    def underline_action_triggered(self) -> pyqtSignal:
        return self._underline_action.triggered

    @property
    def change_font_size_triggered(self) -> pyqtSignal:
        self.font_size_selector.currentTextChanged
