from   mcrcon import MCRcon
import pymysql
import sqlalchemy
import pandas as pd
from   errors import Error
import time
import yaml
import os
import re
from typing import Optional, Any
from settings_cls import Settings
from pydantic import BaseModel, validator

class User(BaseModel):
    class Config:
        validate_assignment = True

    mail: str
    username: str
    name: str
    token:int = 0

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if not all(list(
            map(bool,
                filter(lambda x : not isinstance(x,int),
                       self.__dict__.values())
               )
        )):
            raise Error("einige Felder sind nicht ausgefühlt")

class Parser():
    def __init__(self) -> None:
        pass

    def load_settings(self,path:str)->Settings:
        path = os.path.dirname(__file__)+path
        with open(path) as f:
            settings = yaml.load(f,Loader=yaml.FullLoader)
            return Settings(
                db_username          = settings['db']['user'],
                db_password          = settings['credentials']['password_db'],
                db_server_ip         = settings['db']['server_ip'],
                db_database          = settings['db']['db'],
                db_table             = settings['db']['table'],
                mail_password        = settings['credentials']['password_web'],
                mcrcon_password      = settings['credentials']['mcpassword'],
                trusted_mail_suffix  = settings["settings"]["trusted_mail_suffix"],
                token_email          = settings["settings"]["token_email"],
                false_username_email = settings["settings"]["false_username_email"],
                output               = settings["settings"]["output"],
            )

    def get_user(self, dbframe:pd.DataFrame)->User:
        mail     = str(dbframe["reg_mail"])    .strip("0 ").partition('\n')[0]
        username = str(dbframe["reg_username"]).strip("0 ").partition('\n')[0]
        name     = str(dbframe["reg_name"])    .strip("0 ").partition('\n')[0]
        return User(mail=mail,username=username,name=name)

    def mc_call(self,resp:str)->bool:
        # TODO: response als registriet oder falscher username identifizieren.
        whitelist_add = re.compile("Added (\w*?) to the whitelist")
        if re.fullmatch(whitelist_add,resp.strip()):
            return True
        return False

class Handler():

    def __init__(self,db_username:str,db_pswrd:str,db_server_ip:str, mc_pswrd:str) -> None:
        self.db_username:str = db_username
        self.db_password:str = db_pswrd
        self.db_ip:str       = db_server_ip
        self.mc_password:str = mc_pswrd
        self.token_limit:int = 3
        self.timeout:int     = 5*60

    def sql_call(self,cmd:str)->pd.DataFrame:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/Registration")
        return pd.read_sql(str(cmd),
                           con=engine
                          )

    def sql_update(self,cmd:str)->None:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/Registration")
        with engine.connect() as connection:
            connection.execute(sqlalchemy.text(cmd))

    def sql_set_reg_status(self,user:User, status:int)->None:
        self.sql_update(f"UPDATE registration SET reg_done = {status}.0 WHERE reg_mail = '{user.mail}'")

    def sql_set_reg_comment(self,user:User, comment:str)->None:
        self.sql_update(f"UPDATE registration SET reg_comment = {comment} WHERE reg_mail = '{user.mail}'")

    def sql_get_first_user(self)->pd.DataFrame:
        return self.sql_call("SELECT * FROM registration WHERE reg_done is Null LIMIT 1")

    def await_token(self,user:User)->bool:
        timeout_limit = time.time() + self.timeout
        counter       = 0
        ret           = 0

        while counter <=self.token_limit or time.time()>=timeout_limit:
            sql = self.sql_call(f"SELECT token FROM registration WHERE reg_mail = '{user.mail}'")
            if sql.empty:
                raise Error("Es gibt kein user")
            token = str(sql).split()[-1]

            if token != "None":
                counter +=1
                try: ret = int(token)
                except ValueError: raise Error(f"kein korrekter Token syntax: {token}")
            if ret == user.token:
                return True

            time.sleep(5)

        return False

    def mcrcon_call(self,cmd:str)->str:
        with MCRcon("45.154.49.72", self.mc_password) as mcr:
            resp = mcr.command(cmd)
        return resp

def main()->None:
    #  p = Parser()
    #  conf = p.load_settings("/../settings.yml")
    u = User( mail= "test", username = "test", name= "test")     
    print(u)
    #  h = Handler(conf["db_username"],conf["db_password"],conf["db_server_ip"],conf["mcrcon_password"])
    #p.load_settings("/../settings.json")
    #u = User("samuel.huwiler@gmx.ch","test","samuel")
if __name__ == "__main__":
    main()
