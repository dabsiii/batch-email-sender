from pathlib import Path
from typing import Dict, List

from src.gui.email_bot_gui_c1 import EmailBotGuiC1
from src.model.credentials import Credentials
from src.model.data import Data
from src.model.email_bot import EmailBot


class EmailBotApp:
    def __init__(self):

        self._variables: List = None
        self._credentials: Credentials = None
        self._data: Data = None
        self._attachment_folder_path: Path = None
        self._email_bot: EmailBot = None
        self._gui = EmailBotGuiC1()
        self._gui.selected_credentials.subscribe(self._read_credentials)
        self._gui.selected_data.subscribe(self._read_data)
        self._gui.selected_folder.subscribe(self._read_attachment_folder)
        self._gui.send_email_clicked.subscribe(self._on_send_email_click)

    def start(self):
        self._gui.show()

    # self._data_reader = Data()
    # self._email_bot = EmailBot()

    def _read_credentials(self, data) -> None:
        credentials_path = self._gui.get_credentials_path()
        self._credentials = Credentials(credentials_path)
        username = self._credentials.get_username()
        password = self._credentials.get_password()
        self._email_bot = EmailBot(username, password)

    def _read_data(self, data) -> None:
        data_file_path = self._gui.get_data_path()
        self._data = Data(data_file_path)
        self._variables = self._data.get_columns()
        self._gui.update_variables(self._variables)

    def _read_attachment_folder(self, data) -> None:
        self._attachment_folder_path = self._gui.get_attachment_folder_path()

    def _on_send_email_click(self, data) -> None:
        credentials = self._credentials
        data = self._data
        attachment_folder_path = self._attachment_folder_path

        username = credentials.get_username()
        password = credentials.get_password()
        email_bot = EmailBot(username, password)

        try:
            email_bot.connect()

            for record in data.get_records():
                email = record["EMAIL"]
                file = record["FILE"]

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
