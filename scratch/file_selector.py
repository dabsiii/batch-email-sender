import os
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
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
        self.layout = QVBoxLayout()

        # Label for description
        self.label = QLabel(self.label_text)
        self.layout.addWidget(self.label)

        # Inner HLayout to hold icon, file name, and file path
        self.info_layout = QHBoxLayout()
        # Browse Button
        self.button = QPushButton(self.button_text)
        self.button.setIcon(QIcon.fromTheme("document-open"))
        self.button.clicked.connect(self.browse_file)
        self.layout.addWidget(self.button)
        # File Icon
        self.icon_label = QLabel(self)
        self.info_layout.addWidget(self.icon_label)

        # File Name
        self.file_name_label = QLabel("No file selected")
        self.info_layout.addWidget(self.file_name_label)

        # Full Path display
        self.path_label = QLabel("")
        self.layout.addLayout(self.info_layout)
        self.layout.addWidget(self.path_label)

        # Set the layout for the main widget
        self.setLayout(self.layout)

        # Store file path
        self.file_path = None

        # Apply an outline around the entire widget for clear separation
        self.setStyleSheet(
            """
            outline: 3px solid #4CAF50; 
            outline-offset: 5px;
            padding: 10px;
            margin-bottom: 20px;  # To create space between the browsers
        """
        )

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
        """Update the display with the selected file path, icon, and file name."""
        # Extract the file name from the full path
        file_name = os.path.basename(self.file_path)

        # Set the file name in the label
        self.file_name_label.setText(file_name)

        # Show the full path in the label
        self.path_label.setText(f"Full Path: {self.file_path}")

        # Set the appropriate icon based on file type
        icon = self.get_file_icon(self.file_type)
        pixmap = icon.pixmap(30, 30)  # Convert to QPixmap and scale it
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignLeft)

    def get_file_icon(self, file_type):
        """Return the appropriate icon based on the file type"""
        if file_type == "json":
            return QIcon(
                str(Path("assets\\json-icon.png").resolve())
            )  # Custom JSON icon (use local image)
        elif file_type == "xlsx":
            return QIcon(
                str(Path("assets\\xlsx-icon.png").resolve())
            )  # Custom XLSX icon (use local image)
        elif file_type == "folder":
            return QIcon(
                str(Path("assets\\folder-icon.jpg").resolve())
            )  # Custom Folder icon (use local image)
        return QIcon(":/icons/default-icon.png")  # Default icon (use local image)


class FileSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Sender - File Selector")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Layout setup
        grid_layout = QGridLayout()

        # File Browser Widgets for different file types
        self.credentials_widget = FileBrowserWidget(
            "Import Sender Credentials File (.json):", "Select a file", "json", self
        )
        self.excel_widget = FileBrowserWidget(
            "Select the Data File (.xlsx):", "Select a file", "xlsx", self
        )
        self.folder_widget = FileBrowserWidget(
            "Select Folder Containing Attachments:", "Select a file", "folder", self
        )

        # Adding widgets with appropriate grid positioning
        grid_layout.addWidget(self.credentials_widget, 0, 0)
        grid_layout.addWidget(self.excel_widget, 1, 0)
        grid_layout.addWidget(self.folder_widget, 2, 0)

        # Proceed button
        self.proceed_button = QPushButton("Proceed", self)
        self.proceed_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;"
        )
        self.proceed_button.clicked.connect(self.proceed)
        grid_layout.addWidget(self.proceed_button, 3, 0)

        # Status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Set the layout for the central widget
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
