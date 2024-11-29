import json
from typing import Dict


class Credentials:
    def __init__(self, file_path: str):
        """
        Initializes the CredentialsReader with the path to the credentials file.

        :param file_path: Path to the JSON file containing credentials.
        """
        self.file_path: str = file_path
        self.credentials: Dict[str, str] = {}
        self._read_credentials()

    def _read_credentials(self) -> None:
        """
        Reads and parses the credentials from the JSON file and stores them internally.

        :raises: FileNotFoundError if the file doesn't exist.
                 ValueError if the file content is invalid.
        """
        try:
            with open(self.file_path, "r") as file:
                credentials = json.load(file)
                if not all(key in credentials for key in ["username", "password"]):
                    raise ValueError("Missing required keys in credentials file.")
                self.credentials = credentials
        except FileNotFoundError:
            print(f"Credentials file not found: {self.file_path}")
            raise
        except json.JSONDecodeError:
            print("Error decoding JSON file. Please check the format.")
            raise
        except ValueError as e:
            print(f"Invalid credentials file: {e}")
            raise

    def get_username(self) -> str:
        """
        Returns the username from the credentials.

        :return: Username string.
        :raises: ValueError if the credentials are not loaded.
        """
        if not self.credentials:
            raise ValueError(
                "Credentials have not been loaded. Call 'read_credentials' first."
            )
        return self.credentials["username"]

    def get_password(self) -> str:
        """
        Returns the password from the credentials.

        :return: Password string.
        :raises: ValueError if the credentials are not loaded.
        """
        if not self.credentials:
            raise ValueError(
                "Credentials have not been loaded. Call 'read_credentials' first."
            )
        return self.credentials["password"]
