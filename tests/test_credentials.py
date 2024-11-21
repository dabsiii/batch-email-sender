from pathlib import Path

from icecream import ic

from src.credentials import Credentials


def test_credentials():
    relative_path = Path("tests\\credentials.json")
    cred = Credentials(relative_path.resolve())
    ic(cred.get_username())
    ic(cred.get_password())
