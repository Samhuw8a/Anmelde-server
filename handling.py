from   configparser import ConfigParser
from   mcrcon import MCRcon
import sqlalchemy
import pandas as pd
import time
import random

class User():
    def __init__(self,mail:str,username:str,name:str) -> None:
        self.mail:str     = mail 
        self.username:str = username
        self.name:str     = name
    def __repr__(self) -> str:
        return f"User({self.mail},{self.username},{self.name})"

class Parser():
    def __init__(self) -> None:
        pass

    def load_config(self,path:str)->dict:
        config=ConfigParser(interpolation=None)
        config.read(path)
        return {
        "db_username"     : str(config['credentials']['user']),
        "db_password"     : str(config['credentials']['password_db']),
        "db_server_ip"    : str(config['db']['server_ip']),
        "db_database"     : str(config['db']['db']),
        "db_table"        : str(config['db']['table']),
        "mail_password"   : str(config['credentials']['password_web']),
        "mcrcon_password" : str(config['credentials']['mcpassword']),
        }

    def get_user(self, dbframe:pd.DataFrame)->User:
        mail = dbframe["reg_mail"]
        username = dbframe["reg_username"]
        name = dbframe["reg_name"]
        return User(mail,username,name)

class Handler():

    def __init__(self,username:str,pswrd:str,server_ip:str) -> None:
        self.username:str = username
        self.password:str = pswrd
        self.ip:str       = server_ip

    def sql_call(self,cmd:str)->pd.DataFrame:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.username}:{self.password}@{self.ip}/Registration")
        return pd.read_sql(str(cmd),
                           con=engine
                          )

def main()->None:
    p = Parser()
    conf = p.load_config("test_config.ini")
    h = Handler(conf["db_username"],conf["db_password"],conf["db_server_ip"])
    print(str(h.sql_call("Select * from registration")))

if __name__ == "__main__":
    main()
