from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAction, QComboBox, QMessageBox, QToolBar

MESSAGE = """
Contact the Developer

Name   : Elyson L. Panolino
Email  : elysonpanolino@gmail.com
Mobile : 0930 696 3101
Address: Sabanes Compound 2, El Rancho, Santa Monica, Puerto Princesa City, Palawan, Philippines, 5300
"""


class ToolBar:
    """
    HELP
    """

    def __init__(self):
        # Set up the toolbar for text formatting
        self.widget = QToolBar()

        self._help_action = QAction("HELP")
        self.widget.addAction(self._help_action)
        self._help_action.triggered.connect(self._show_help_message)

    def _show_help_message(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Help & Support")
        msg_box.setText(MESSAGE)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.exec_()
