from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget


def main():
    app = QApplication([])
    widget = QWidget()
    label1 = QLabel("HAHHAHA", widget)
    label2 = QLabel("HELO ", widget)

    widget.show()
    app.exec_()


main()
