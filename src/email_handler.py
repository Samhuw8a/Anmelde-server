import logging
import smtplib
import ssl
import os
from handling import User
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email_server:
    # TODO message loading weg
    def __init__(
        self,
        logger: logging.Logger,
        port: int,
        server: str,
        pswrd: str,
        sender_mail: str,
    ) -> None:
        self.logger = logger
        self.port: int = port
        self.server: str = server
        self.pswrd: str = pswrd
        self.sender: str = sender_mail
        self.message: str = "Hello_world"

        self.logger.debug("initialised Email_server")

    def load_from_template(self, file_name: str) -> None:
        #  path = os.path.dirname(__file__)+file_name
        with open(os.path.dirname(__file__) + file_name, "r") as f:
            self.message = f.read().strip()

    def send(self, user: User, subject: str) -> None:
        self.message = self.message.replace("{mail}", user.mail)
        self.message = self.message.replace("{token}", str(user.token))
        self.message = self.message.replace("{name}", user.name)
        self.message = self.message.replace("{username}", user.username)
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = user.mail
        msg["Subject"] = subject
        msg.attach(MIMEText(self.message, "plain", "utf-8"))
        text = msg.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
            server.login(self.sender, self.pswrd)
            server.sendmail(self.sender, user.mail, text)


def main() -> None:
    log = logging.Logger("test")
    serv = Email_server(
        log, 465, "cap.ssl.hosttech.eu", "**************", "no_reply@ksrminecraft.ch"
    )
    samuel = User(mail="samuel.huwiler@gmx.ch", username="samhuw_8a", name="Samuel")
    serv.load_from_template("/../tests/test_mail.txt")
    serv.send(samuel, "Test_mail")


if __name__ == "__main__":
    main()
