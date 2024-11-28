import sys

from PyQt5.QtWidgets import QApplication

from src.gui.email_editor.email_editor_c1 import EmailEditorC1


def test_email_editor():
    app = QApplication(sys.argv)

    editor = EmailEditorC1()
    editor.widget.show()
    app.exit(app.exec_())
