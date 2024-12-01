import threading
from pathlib import Path
from typing import Dict, List

from src.event.event_ import Event_
from src.gui.email_bot_gui_c1 import EmailBotGuiC1
from src.model.credentials import Credentials
from src.model.data import Data
from src.model.email_bot import EmailBot


class EmailBotApp:
    def __init__(self, version: str = ""):
        self._email_sending_thread = threading.Thread(
            target=lambda: self._send_batch_emails(0)
        )

        self._variables: List = None
        self._credentials: Credentials = None
        self._data: Data = None
        self._attachment_folder_path: Path = None
        self._email_bot: EmailBot = None
        self._ready = Event_()
        self._not_ready = Event_()
        self._gui = EmailBotGuiC1(version)
        self._gui.selected_credentials.subscribe(self._read_credentials)
        self._gui.selected_data.subscribe(self._read_data)
        self._gui.selected_folder.subscribe(self._read_attachment_folder)
        self._gui.send_email_clicked.subscribe(
            lambda e: self._email_sending_thread.start()
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
        if data_file_path is None:
            self._gui.update_variables([])

        self._check_ready()

    def _read_attachment_folder(self, data) -> None:
        attachment_folder_path = self._gui.get_attachment_folder_path()

        if attachment_folder_path is not None:
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

        try:
            email_bot.connect()

            for record in data.get_records():
                email = record[self._gui.get_email_column()]
                file = record[self._gui.get_attachments_column()]

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
            self._gui.log("Task Finished ...")
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

    def _log_email_sent(self, data) -> None:
        recipient = data["recipient"]
        attachment = data["attachment"]
        message = f"Email succesfuly sent to {recipient} [attachment: {attachment}]"
        self._gui.log(message)

    def _log_finished(self, data):
        self._gui.log("Task Finished ...")

    def _log_sending_email(self) -> None:
        self._gui.log("Sending emails, please wait ...")

    def _log_sender_info(self, username: str) -> None:
        self._gui.log(f"Sender Username: {username}")
