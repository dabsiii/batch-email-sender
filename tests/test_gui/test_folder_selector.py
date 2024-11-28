import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.gui.selector.folder_selector import FolderSelector


def test_FolderSelector():
    app = QApplication(sys.argv)
    widg = QWidget()
    widg_layout = QVBoxLayout()
    widg.setLayout(widg_layout)
    selector1 = FolderSelector(
        info_text="Select a folder",
        icon_path=Path("assets\\folder-icon.jpg").resolve(),
    )
    widg_layout.addWidget(selector1.widget)

    widg_layout.addWidget(selector1.widget)

    widg.show()
    sys.exit(app.exec_())
