import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.gui.selector.file_selector import FileSelector


def test_FileSelector():
    app = QApplication(sys.argv)
    widg = QWidget()
    widg_layout = QVBoxLayout()
    widg.setLayout(widg_layout)
    selector1 = FileSelector(
        info_text="Select a file",
        icon_path=Path("assets\\json-icon.png").resolve(),
        filter="JSON Files (*.json);;All Files (*)",
    )
    widg_layout.addWidget(selector1.widget)

    selector2 = FileSelector(
        info_text="Select a file",
        icon_path=Path("assets\\xlsx-icon.png").resolve(),
        filter="Excel Files (*.xls *.xlsx);;All Files (*)",
    )
    widg_layout.addWidget(selector2.widget)

    selector3 = FileSelector(
        info_text="Select a file",
        icon_path=Path("assets\\folder-icon.jpg").resolve(),
    )
    widg_layout.addWidget(selector3.widget)

    widg.show()
    sys.exit(app.exec_())
