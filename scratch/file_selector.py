import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCharFormat
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class FileSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Sender - File Selector")
        self.setGeometry(100, 100, 600, 300)

        # Labels and Buttons for selecting files
        self.smtp_label = QLabel("Import SMTP Credentials (.json):", self)
        self.smtp_label.setGeometry(20, 30, 250, 30)
        self.smtp_button = QPushButton("Browse", self)
        self.smtp_button.setGeometry(400, 30, 100, 30)
        self.smtp_button.clicked.connect(self.select_smtp_file)

        self.excel_label = QLabel("Select the Data File (.xlsx):", self)
        self.excel_label.setGeometry(20, 80, 250, 30)
        self.excel_button = QPushButton("Browse", self)
        self.excel_button.setGeometry(400, 80, 100, 30)
        self.excel_button.clicked.connect(self.select_excel_file)

        self.folder_label = QLabel(
            "Select the Folder Containing Attachment Files:", self
        )
        self.folder_label.setGeometry(20, 130, 300, 30)
        self.folder_button = QPushButton("Browse", self)
        self.folder_button.setGeometry(400, 130, 100, 30)
        self.folder_button.clicked.connect(self.select_folder)

        # Button to proceed
        self.proceed_button = QPushButton("Proceed", self)
        self.proceed_button.setGeometry(250, 200, 100, 40)
        self.proceed_button.clicked.connect(self.proceed)

        # File paths (store selected files)
        self.smtp_file_path = None
        self.excel_file_path = None
        self.folder_path = None

    def select_smtp_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select SMTP Credentials", "", "JSON Files (*.json)"
        )
        if file_path:
            self.smtp_file_path = file_path
            self.smtp_label.setText(f"SMTP File: {os.path.basename(file_path)}")

    def select_excel_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Data File", "", "Excel Files (*.xlsx)"
        )
        if file_path:
            self.excel_file_path = file_path
            self.excel_label.setText(f"Excel File: {os.path.basename(file_path)}")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Folder Containing Attachments"
        )
        if folder_path:
            self.folder_path = folder_path
            self.folder_label.setText(
                f"Attachment Folder: {os.path.basename(folder_path)}"
            )

    def proceed(self):
        # Ensure all files and folders are selected
        if not self.smtp_file_path or not self.excel_file_path or not self.folder_path:
            QMessageBox.warning(
                self, "Missing Files", "Please select all required files and folder."
            )
            return

        # Open the email editor window
        self.email_editor = GmailLikeEditor()
        self.setCentralWidget(
            self.email_editor
        )  # Embed the editor widget inside the main window
        self.close()


class GmailLikeEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Email Sender - Email Editor")
        self.setGeometry(100, 100, 800, 600)

        # Create the QTextEdit for rich text editing
        self.text_edit = QTextEdit(self)
        self.text_edit.setAcceptRichText(True)  # Enable rich text editing (HTML)
        self.text_edit.setText(
            "<html><body><p>Compose your email here...</p></body></html>"
        )

        # Create a toolbar for text formatting
        self.toolbar = QToolBar(self)

        # Add actions for the toolbar (bold, italic, underline, font size)
        self.bold_action = QAction("B", self)
        self.bold_action.triggered.connect(self.apply_bold)
        self.toolbar.addAction(self.bold_action)

        self.italic_action = QAction("I", self)
        self.italic_action.triggered.connect(self.apply_italic)
        self.toolbar.addAction(self.italic_action)

        self.underline_action = QAction("U", self)
        self.underline_action.triggered.connect(self.apply_underline)
        self.toolbar.addAction(self.underline_action)

        # Send Email button
        self.send_button = QAction("Send Email", self)
        self.send_button.triggered.connect(self.send_email)
        self.toolbar.addAction(self.send_button)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def apply_bold(self):
        cursor = self.text_edit.textCursor()
        cursor.mergeCharFormat(self.create_char_format(weight=QFont.Weight.Bold))
        self.text_edit.setTextCursor(cursor)

    def apply_italic(self):
        cursor = self.text_edit.textCursor()
        cursor.mergeCharFormat(self.create_char_format(italic=True))
        self.text_edit.setTextCursor(cursor)

    def apply_underline(self):
        cursor = self.text_edit.textCursor()
        cursor.mergeCharFormat(self.create_char_format(underline=True))
        self.text_edit.setTextCursor(cursor)

    def create_char_format(
        self, weight=QFont.Weight.Normal, italic=False, underline=False
    ):
        char_format = QTextCharFormat()
        char_format.setFontWeight(weight)
        char_format.setFontItalic(italic)
        char_format.setFontUnderline(underline)
        return char_format

    def send_email(self):
        # Placeholder for sending email logic
        html_content = self.text_edit.toHtml()
        QMessageBox.information(
            self,
            "Send Email",
            f"Email sent with the following content:\n\n{html_content}",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Start with the file selector window
    selector_window = FileSelectorWindow()
    selector_window.show()

    sys.exit(app.exec_())
