import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from src.event.event_ import Event_


class EmailBot:
    def __init__(
        self,
        username: str,
        password: str,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
    ):
        self.smtp_server: str = smtp_server
        self.smtp_port: int = smtp_port
        self.username: str = username
        self.password: str = password
        self.server: Optional[smtplib.SMTP] = None

        # Events
        self.connected = Event_()
        self.connecting_failed = Event_()
        self.email_sent = Event_()
        self._sending_failed = Event_()

    def connect(self) -> None:
        """Establishes a connection to the SMTP server."""
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.server.login(self.username, self.password)
            self.connected.publish(
                {"username": self.username, "password": self.password}
            )
        except Exception as e:
            self.connecting_failed.publish(
                {"username": self.username, "password": self.password}
            )
            raise

    def disconnect(self) -> None:
        """Closes the connection to the SMTP server."""
        if self.server:
            self.server.quit()
            print("Disconnected from the SMTP server.")

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        is_html: bool = False,  # New parameter to indicate if body is HTML
        attachments: Optional[List[str]] = None,
    ) -> None:
        """
        Sends an email with optional attachments and supports HTML content.

        :param recipient: Recipient email address.
        :param subject: Subject of the email.
        :param body: Body content of the email (HTML or plain text).
        :param is_html: Boolean flag to specify if body is HTML.
        :param attachments: List of file paths to attach.
        """
        try:
            # Create the email
            msg = MIMEMultipart()
            msg["From"] = self.username
            msg["To"] = recipient
            msg["Subject"] = subject

            # Add body (support for HTML or plain text)
            if is_html:
                msg.attach(MIMEText(body, "html"))  # HTML body
            else:
                msg.attach(MIMEText(body, "plain"))  # Plain text body

            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={os.path.basename(file_path)}",
                        )
                        msg.attach(part)
                    else:
                        print(f"Attachment {file_path} not found.")

            # Send the email
            if self.server:
                self.server.send_message(msg)
                self.email_sent.publish({"recipient": recipient})
                print(f"Email sent successfully to {recipient}. published email sent")
            else:
                print("SMTP server connection is not established.")

        except Exception as e:
            print(f"Failed to send email: {e}")
            self._sending_failed.publish({"recipient": recipient})
            raise
