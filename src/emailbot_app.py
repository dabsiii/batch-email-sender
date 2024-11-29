from typing import List

from src.gui.email_bot_gui_c1 import EmailBotGuiC1
from src.model.credentials import Credentials
from src.model.data import Data
from src.model.email_bot import EmailBot


class EmailBotApp:
    def __init__(self):

        self._variables: List = None
        self._credentials: Credentials = None
        self._data: Data = None
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
        path = self._gui.get_attachment_folder_path()
        print(path)

    def _on_send_email_click(self, data) -> None:
        body = self._gui.get_email_body_html()
        print(body)
