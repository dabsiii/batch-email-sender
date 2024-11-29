from pathlib import Path

from src.model.credentials import Credentials
from src.model.data import Data
from src.model.email_bot import EmailBot


# Example usage
def t_email_bot():
    credentials = Credentials(Path("tests\\files\\credentials.json").resolve())
    data = Data(Path("tests\\files\\excel file.xlsx").resolve())
    document_path = Path("tests\\files\\documents").resolve()

    username = credentials.get_username()
    password = credentials.get_password()
    email_bot = EmailBot(username, password)

    try:
        email_bot.connect()

        for record in data.get_records():
            email = record["EMAIL"]
            file = record["FILE"]
            name = record["NAME"]
            id = record["ID"]

            attachment = f"{document_path}\\{file}"
            html_body = """"""
            email_bot.send_email(
                recipient=email,
                subject=f"Test Email Sample 1 {id}_{name}",
                body=html_body,
                is_html=True,
                attachments=[attachment],  # Update paths
            )
    finally:
        email_bot.disconnect()
