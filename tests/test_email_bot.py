from pathlib import Path

from src.credentials import Credentials
from src.data import Data
from src.email_bot import EmailBot


# Example usage
def test_email_bot():
    credentials = Credentials(Path("tests\\credentials.json").resolve())
    data = Data(Path("tests\\excel file.xlsx").resolve())
    document_path = Path("tests\\documents").resolve()

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
