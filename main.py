from handling import Handler,Parser,User
from email_handler import Email_server
from errors import Error
import random
import time

class Event_handler():
    def __init__(self)->None:
        self.parser  = Parser()
        config:dict  = self.parser.load_config("config.ini")
        self.handler = Handler(config["db_username"],config["db_passord"],config["db_server_ip"],config["mcrcon_password"])
        self.emailer = Email_server(465,"cap.ssl.hosttech.eu",config["mail_passord"])

    def is_done(self,user:User)->None:
        self.handler.sql_call(f"UPDATE registration SET reg_done =1.0 WHERE reg_mail = {user.mail}")
    def is_undone(self,user:User)->None:
        self.handler.sql_call(f"UPDATE registration SET reg_done =2.0 WHERE reg_mail = {user.mail}")


    def main(self)->None:
        que = self.handler.sql_call("SELECT * FROM registration WHERE reg_done is Null LIMIT 1")
        user = self.parser.get_user(que)

        if user.mail.strip().split("@") !="sluz.ch":
            self.is_undone(user)
            raise Error("keine valide sluz adresse")

        user.token =  random.randint(1_000_000, 999_999_999)
        self.emailer.send(user.mail,user.token,user.name)
        is_valid = self.handler.await_token(user)

        if not is_valid:
            self.is_undone(user)
            raise Error("falscher token")

        response = self.handler.mcrcon_call(f"whitelist add {user.username}")
        if not self.parser.mc_call(response):
            self.is_undone(user)
            raise Error("falscher Username")

        self.is_done(user)


def main()->None:
    eventhandler = Event_handler()
    while True:
        eventhandler.main()

if __name__ =="__main__":
    main()
