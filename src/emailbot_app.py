import threading
from pathlib import Path
from typing import Dict, List

from src.event.event_ import Event_
from src.gui.email_bot_gui_c1 import EmailBotGuiC1
from src.model.credentials import Credentials
from src.model.data import Data
from src.model.email_bot import EmailBot

INFO_LOG_COLOR = (250, 255, 250)
WARNING_LOG_COLOR = (200, 100, 50)
SUCCESS_LOG_COLOR = (20, 255, 100)
TASK_LOG_COLOR = (20, 100, 255)


class EmailBotApp:
    def __init__(self, version: str = ""):
        self._email_sending_thread = threading.Thread(
            target=lambda: self._send_batch_emails(0)
        )
        # EVENTS
        self._ready = Event_()
        self._not_ready = Event_()
        self._invalid_email_found_in_email_column = Event_()
        self._file_not_found_in_attachment_folder = Event_()

        # ELEMENTS

        self._variables: List = None
        self._credentials: Credentials = None
        self._data: Data = None
        self._attachment_folder_path: Path = None
        self._email_bot: EmailBot = None

        self._gui = EmailBotGuiC1(version)
        # EVENTS HANDLING
        self._gui.selected_credentials.subscribe(self._read_credentials)
        self._gui.selected_data.subscribe(self._read_data)
        self._gui.selected_folder.subscribe(self._read_attachment_folder)
        self._gui.send_email_clicked.subscribe(
            lambda e: self._email_sending_thread.start()
        )
        self._gui.selected_email_column.subscribe(lambda e: self._check_valid_emails())
        self._gui.selected_attachments_column.subscribe(
            lambda e: self._check_attachments()
        )

        self._ready.subscribe(lambda e: self._gui.enable_send_email())
        self._not_ready.subscribe(lambda e: self._gui.disable_send_email())

    def start(self):
        self._gui.show()

    # self._data_reader = Data()
    # self._email_bot = EmailBot()

    def _read_credentials(self, data) -> None:
        credentials_path = self._gui.get_credentials_path()
        if credentials_path is not None:
            self._credentials = Credentials(credentials_path)
            username = self._credentials.get_username()
            password = self._credentials.get_password()
            self._email_bot = EmailBot(username, password)
            self._log_sender_info(username)

        self._check_ready()

    def _read_data(self, data) -> None:
        data_file_path = self._gui.get_data_path()
        if data_file_path is not None:
            self._data = Data(data_file_path)
            self._variables = self._data.get_columns()
            self._gui.update_variables(self._variables)
            self._log_number_of_records(self._data.get_number_of_records())
        if data_file_path is None:
            self._gui.update_variables([])

        self._check_ready()

    def _read_attachment_folder(self, data) -> None:
        attachment_folder_path = self._gui.get_attachment_folder_path()

        if attachment_folder_path is not None:
            number_of_files = count_files_in_directory(attachment_folder_path)
            self._log_number_of_files(number_of_files)
            self._attachment_folder_path = attachment_folder_path

        self._check_ready()

    def _send_batch_emails(self, data) -> None:
        self._log_sending_email()
        credentials = self._credentials
        data = self._data
        attachment_folder_path = self._attachment_folder_path

        username = credentials.get_username()
        password = credentials.get_password()
        email_bot = EmailBot(username, password)
        email_bot.email_sent.subscribe(self._log_email_sent)
        email_column = self._gui.get_email_column()
        attachments_column = self._gui.get_attachments_column()

        try:
            email_bot.connect()

            for record in data.get_records():
                email = record[email_column]
                file = record[attachments_column]

                attachment = f"{attachment_folder_path}\\{file}"
                raw_html_body = self._gui.get_email_body_html()
                raw_subject = self._gui.get_email_subject()
                email_bot.send_email(
                    recipient=email,
                    subject=self._replace_variables(
                        raw_subject, self._variables, record
                    ),
                    body=self._replace_variables(
                        raw_html_body, self._variables, record
                    ),
                    is_html=True,
                    attachments=[attachment],  # Update paths
                )
            self._log_finished()
        finally:
            email_bot.disconnect()

    def _replace_variables(self, text: str, variables: List[str], record: Dict) -> str:
        out_text = text
        for variable in variables:
            substring = f"{{{variable}}}"
            if out_text.find(substring) != -1:
                value = record[variable]
                out_text: str = out_text.replace(substring, str(value))

        return out_text

    def _check_ready(self):
        credentials = self._gui.get_credentials_path() is not None
        data = self._gui.get_data_path() is not None
        attachment_folder = self._gui.get_attachment_folder_path() is not None

        if credentials and data and attachment_folder:
            self._ready.publish(True)
        else:
            self._not_ready.publish(True)

    def _check_valid_emails(self):
        email_column = self._gui.get_email_column()
        for record in self._data.get_records():
            email = record[email_column]
            if not is_valid_email(email):
                self._invalid_email_found_in_email_column.publish
                return
            else:
                pass

    def _check_attachments(self):
        attachments_column = self._gui.get_attachments_column()
        attachment_dir = self._gui.get_attachment_folder_path()
        if attachment_dir is not None:
            for record in self._data.get_records():
                attachment = record[attachments_column]
                if not file_is_in_directory(attachment_dir, attachment):
                    self._file_not_found_in_attachment_folder.publish
                else:
                    print(attachment)

    def _log_email_sent(self, data) -> None:
        recipient = data["recipient"]
        attachment = data["attachment"]
        message = f"Email succesfuly sent to {recipient} [attachment: {attachment}]"
        self._gui.log(message, color=SUCCESS_LOG_COLOR)

    def _log_finished(self) -> None:
        self._gui.log("Task Finished ...", color=TASK_LOG_COLOR)

    def _log_sending_email(self) -> None:
        self._gui.log("Sending emails, please wait ...", color=TASK_LOG_COLOR)

    def _log_sender_info(self, username: str) -> None:
        self._gui.log(f"Sender Username: {username}")

    def _log_number_of_records(self, number_of_records: int) -> None:
        message = f"{number_of_records} records found from data file"
        self._gui.log(message)

    def _log_number_of_files(self, number_of_files: int) -> None:
        message = f"{number_of_files} files found in attachments folder (okay lang sobra wag lang kulang)"
        self._gui.log(message)


def count_files_in_directory(directory_path: str) -> int:

    directory = Path(directory_path)
    if not directory.is_dir():
        raise ValueError(f"The path '{directory_path}' is not a valid directory.")

    return sum(1 for f in directory.iterdir() if f.is_file())


import re


def is_valid_email(email: str) -> bool:
    email = str(email)
    email_regex = r"^[^@]+@[^@]+\.[^@]+$"
    return bool(re.match(email_regex, email))


def file_is_in_directory(directory_path: str, filename: str) -> bool:
    directory = Path(directory_path)
    return directory.joinpath(filename).is_file()
