import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


class FileBrowserWidget(QWidget):
    def __init__(self, label_text, button_text, file_type, parent=None):
        super().__init__(parent)

        self.label_text = label_text
        self.button_text = button_text
        self.file_type = file_type

        # Layout for the File Browser Widget
        self.layout = QHBoxLayout()

        # Label
        self.label = QLabel(self.label_text)
        self.layout.addWidget(self.label)

        # Browse Button
        self.button = QPushButton(self.button_text)
        self.button.setIcon(QIcon.fromTheme("document-open"))
        self.button.clicked.connect(self.browse_file)
        self.layout.addWidget(self.button)

        # Path display label
        self.path_label = QLabel("")
        self.layout.addWidget(self.path_label)

        self.setLayout(self.layout)

        # Store file path
        self.file_path = None

    def browse_file(self):
        file_path = None
        if self.file_type == "json":
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Sender Credentials File", "", "JSON Files (*.json)"
            )
        elif self.file_type == "xlsx":
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Data File", "", "Excel Files (*.xlsx)"
            )
        elif self.file_type == "folder":
            file_path = QFileDialog.getExistingDirectory(
                self, "Select Folder Containing Attachments"
            )

        if file_path:
            self.file_path = file_path
            self.update_display()

    def update_display(self):
        """Update the display with the selected file path and icon."""
        # Show the file path in the label
        self.path_label.setText(f"Path: {self.file_path}")

        # Set the appropriate icon based on file type
        icon = self.get_file_icon(self.file_type)
        pixmap = icon.pixmap(30, 30)  # Convert to QPixmap and scale it
        icon_label = QLabel(self)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignLeft)

        # Update the layout
        self.layout.insertWidget(0, icon_label)

    def get_file_icon(self, file_type):
        """Return the appropriate icon based on the file type"""
        if file_type == "json":
            return QIcon.fromTheme("application-json")
        elif file_type == "xlsx":
            return QIcon.fromTheme(
                "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif file_type == "folder":
            return QIcon.fromTheme("folder-open")
        return QIcon.fromTheme("text-plain")  # Default icon


class FileSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Sender - File Selector")
        self.setGeometry(100, 100, 600, 300)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Layout setup
        grid_layout = QGridLayout()

        # File Browser Widgets for different file types
        self.credentials_widget = FileBrowserWidget(
            "Import Sender Credentials File (.json):", "Browse", "json", self
        )
        self.excel_widget = FileBrowserWidget(
            "Select the Data File (.xlsx):", "Browse", "xlsx", self
        )
        self.folder_widget = FileBrowserWidget(
            "Select Folder Containing Attachments:", "Browse", "folder", self
        )

        grid_layout.addWidget(self.credentials_widget, 0, 0)
        grid_layout.addWidget(self.excel_widget, 1, 0)
        grid_layout.addWidget(self.folder_widget, 2, 0)

        # Proceed button
        self.proceed_button = QPushButton("Proceed", self)
        self.proceed_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold;"
        )
        self.proceed_button.clicked.connect(self.proceed)
        grid_layout.addWidget(self.proceed_button, 3, 0)

        # Status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Set the layout
        container = QWidget()
        container.setLayout(grid_layout)
        self.setCentralWidget(container)

    def proceed(self):
        # Ensure all files and folders are selected
        if (
            not self.credentials_widget.file_path
            or not self.excel_widget.file_path
            or not self.folder_widget.file_path
        ):
            QMessageBox.warning(
                self, "Missing Files", "Please select all required files and folder."
            )
            return

        # Show a message box with the selected paths
        QMessageBox.information(
            self,
            "Proceeding",
            f"Proceeding with the following:\n"
            f"Sender Credentials File: {self.credentials_widget.file_path}\n"
            f"Excel File: {self.excel_widget.file_path}\n"
            f"Attachment Folder: {self.folder_widget.file_path}",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Start with the file selector window
    selector_window = FileSelectorWindow()
    selector_window.show()

    sys.exit(app.exec_())
