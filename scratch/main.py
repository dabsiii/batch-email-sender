import sys

from gmail_editor import (
    GmailLikeEditor,  # Assuming GmailLikeEditor is in gmail_editor.py
)
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class FileSelectorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize attributes
        self.credentials_file = None
        self.excel_file = None
        self.folder_path = None

        # Layout setup
        self.layout = QVBoxLayout()

        # Add File Browsers
        self.credentials_button = QPushButton("Select Sender Credentials File (.json)", self)
        self.excel_button = QPushButton("Select Excel File (.xlsx)", self)
        self.folder_button = QPushButton("Select Folder Containing Attachments", self)

        # Connect buttons to browse files
        self.credentials_button.clicked.connect(self.browse_credentials)
        self.excel_button.clicked.connect(self.browse_excel)
        self.folder_button.clicked.connect(self.browse_folder)

        # Proceed button to open GmailLikeEditor
        self.proceed_button = QPushButton("Proceed", self)
        self.proceed_button.clicked.connect(self.on_proceed)

        # Add widgets to layout
        self.layout.addWidget(self.credentials_button)
        self.layout.addWidget(self.excel_button)
        self.layout.addWidget(self.folder_button)
        self.layout.addWidget(self.proceed_button)

        # Set layout for this window
        self.setLayout(self.layout)

    def browse_credentials(self):
        """Browse for the credentials .json file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Sender Credentials File", "", "JSON Files (*.json)")
        if file_path:
            self.credentials_file = file_path

    def browse_excel(self):
        """Browse for the .xlsx file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Data File", "", "Excel Files (*.xlsx)")
        if file_path:
            self.excel_file = file_path

    def browse_folder(self):
        """Browse for the folder containing attachments"""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Containing Attachments")
        if folder_path:
            self.folder_path = folder_path

    def on_proceed(self):
        """Check if all files and folders are selected, then open the editor"""
        if not self.credentials_file or not self.excel_file or not self.folder_path:
            QMessageBox.warning(self, "Missing Files", "Please select all required files and folder.")
            return

        # Proceed to open the GmailLikeEditor
        self.open_gmail_editor()

    def open_gmail_editor(self):
        """Open the GmailLikeEditor"""
        self.editor_window = GmailLikeEditor(self)
        self.editor_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the file selector window
    file_selector_window = FileSelectorWindow()
    file_selector_window.setWindowTitle("Email Sender - File Selector")
    file_selector_window.show()

    sys.exit(app.exec_())
