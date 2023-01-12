from handling import Handler, Parser, User 
from settings_cls import Settings
from email_handler import Email_server
from errors import Error, UserError, SQLError
import random
import logging
import os
import sys

SETTINGS ="/../settings.yml" 

#TODO logging.conf

OUTPUT=True
LOG_FILE="/../logs/log.log"
STREAM_LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
FILE_LOGGING_FORMAT   = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
FILE_LEVEL  = logging.INFO
STREAM_LEVEL= logging.DEBUG


class Event_handler():
    def __init__(self)->None:
        self.logger            = self.init_logger()
        self.parser            = Parser(self.logger)
        self.settings:Settings = self.parser.load_settings(SETTINGS)
        self.handler           = Handler(self.logger, self.settings.db_username,self.settings.db_password,self.settings.db_server_ip,self.settings.mcrcon_password)
        self.emailer           = Email_server(self.logger, 465,"cap.ssl.hosttech.eu",self.settings.mail_password)

        self.emailer.load_from_template(self.settings.token_email)
        self.logger.info("Initialised Event_handler")

    def is_done(self,user:User)->None:
        self.handler.sql_set_reg_status(user,1)
    def is_undone(self,user:User)->None:
        self.handler.sql_set_reg_status(user,2)

    def init_logger(self)->logging.Logger:
        path = os.path.dirname(__file__)+LOG_FILE

        file_formater   = logging.Formatter(FILE_LOGGING_FORMAT)
        stream_formater = logging.Formatter(STREAM_LOGGING_FORMAT)

        if OUTPUT:
            streamhandler   = logging.StreamHandler(sys.stdout)
            streamhandler.setLevel(STREAM_LEVEL)
            streamhandler.setFormatter(stream_formater)

        filehandler     = logging.FileHandler(path)
        filehandler.setFormatter(file_formater)
        filehandler.setLevel(FILE_LEVEL)

        logger = logging.Logger("main")
        logger.addHandler(filehandler)
        if OUTPUT:
            logger.addHandler(streamhandler)

        return logger

    def main(self)->None:
        que = self.handler.sql_get_first_user()

        if que.empty:
            return 

        user = self.parser.get_user(que)

        self.logger.info(f"Neuer User: {user}")

        mail_addr = user.mail.split("@")[-1]
        if mail_addr not in self.settings.trusted_mail_suffix:
            self.logger.error(f"Kein valider Emailadressen-Suffix: {mail_addr}")
            self.is_undone(user)

        user.token =  random.randint(1_000_000, 999_999_999)

        self.emailer.load_from_template(self.settings.token_email)
        self.emailer.send(user,"Deine Registration bei KSRMinecraft")
        self.logger.info(f"sent token to {user.mail}")

        try: is_valid = self.handler.await_token(user)
        except SQLError as e:
            raise e

        if not is_valid:
            self.is_undone(user)

        response = self.handler.mcrcon_call(f"whitelist add {user.username}")

        if not self.parser.mc_call(response):
            self.is_undone(user)
            self.emailer.load_from_template(self.settings.false_username_email)
            self.emailer.send(user,"Minecraftname existiert nicht")
            self.logger.info(f"sent false_username_email to {user.mail}")
            raise UserError(f"falscher Username : {user.username}")

        self.is_done(user)


def main()->None:
    eventhandler = Event_handler()
    eventhandler.main()

if __name__ == "__main__":
    main()
