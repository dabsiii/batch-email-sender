import sys

from PyQt5.QtWidgets import QApplication

from src.gui.file_selector.file_selector_c1 import FileSelectorWidgetC1


def test_FileSelectorWidgetC1():
    app = QApplication(sys.argv)
    widget = FileSelectorWidgetC1(info_text="Select a file")
    widget.widget.show()
    sys.exit(app.exec_())
