from handling import Handler, Parser, User, Settings
from email_handler import Email_server
from errors import Error
import random

SETTINGS ="/../settings.json" 
CONFIG ="/../config.ini" 


class Event_handler():
    def __init__(self)->None:
        self.parser              = Parser()
        self.settings:Settings   = self.parser.load_settings(SETTINGS)
        config:dict              = self.parser.load_config(CONFIG)
        self.handler             = Handler(config["db_username"],config["db_password"],config["db_server_ip"],config["mcrcon_password"])
        self.emailer             = Email_server(465,"cap.ssl.hosttech.eu",config["mail_password"])

        self.emailer.load_from_template(self.settings.token_email)
    def is_done(self,user:User)->None:
        self.handler.sql_update(f"UPDATE registration SET reg_done = 1.0 WHERE reg_mail = '{user.mail}'")
    def is_undone(self,user:User)->None:
        self.handler.sql_update(f"UPDATE registration SET reg_done = 2.0 WHERE reg_mail = '{user.mail}'")


    def main(self)->None:
        que = self.handler.sql_call("SELECT * FROM registration WHERE reg_done is Null LIMIT 1")
        if que.empty:
            if self.settings.output:
                print("Keine neuen Einträge")
            return 

        user = self.parser.get_user(que)

        if self.settings.output:
            print("Neuer User:")
            print(user)

        if user.mail.strip()[-8:] not in self.settings.trusted_mail_suffix:
            self.is_undone(user)
            raise Error(f"keine valide email adresse: {user.mail}")

        user.token =  random.randint(1_000_000, 999_999_999)

        self.emailer.load_from_template(self.settings.token_email)
        self.emailer.send(user)

        try: is_valid = self.handler.await_token(user)
        except Error as e:
            self.is_undone(user)
            raise e

        if not is_valid:
            self.is_undone(user)
            raise Error("falscher token")

        response = self.handler.mcrcon_call(f"whitelist add {user.username}")

        if not self.parser.mc_call(response):
            self.is_undone(user)
            self.emailer.load_from_template(self.settings.false_username_email)
            self.emailer.send(user)
            raise Error("falscher Username")

        self.is_done(user)


def main()->None:
    eventhandler = Event_handler()
    eventhandler.main()

if __name__ == "__main__":
    main()
