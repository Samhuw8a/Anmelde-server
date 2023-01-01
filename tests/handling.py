from   configparser import ConfigParser
from   mcrcon import MCRcon
import pymysql
import sqlalchemy
import pandas as pd
from   errors import Error
import time
import yaml
import os
import re
from typing import Optional, List
from pydantic import BaseModel,validator

class Settings(BaseModel):
    db_username     : str
    db_password     : str
    db_server_ip    : str
    db_database     : str
    db_table        : str
    mail_password   : str
    mcrcon_password : str

    trusted_mail_suffix  : List[str]
    token_email          : str      
    false_username_email : str      
    output               : bool     

    @validator("trusted_mail_suffix")
    @classmethod
    def is_correct_list(cls,tms:list)-> list:
        email=re.compile("@(\w*)\.(\w*)")
        for el in tms:
            if not re.fullmatch(email,el):
                raise Error(f"Kein korrektes Email format: {el}")
        return tms

class User():
    def __init__(self,mail:str,username:str,name:str) -> None:
        self.mail:str                     = mail 
        self.username:str                 = username
        self.name:str                     = name
        self.token_internal:Optional[int] = None

    @property
    def token(self)->int:
        return self.token_internal if self.token_internal else 0


    @token.setter
    def token(self,token:int)->None:
        if isinstance(token, int):
            self.token_internal = token
        else: raise Error("kein korrekter token")

    def __repr__(self) -> str:
        return f"User({self.mail},{self.username},{self.name})"

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
        return User(mail,username,name)

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

    def sql_call_informatik(self,cmd:str)->pd.DataFrame:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/informatik")
        return pd.read_sql(str(cmd),
                           con=engine
                          )

    def sql_call(self,cmd:str)->pd.DataFrame:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/Registration")
        return pd.read_sql(str(cmd),
                           con=engine
                          )

    def sql_update(self,cmd:str)->pd.DataFrame:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/Registration")
        with engine.connect() as connection:
            connection.execute(sqlalchemy.text(cmd))

    def await_token(self,user:User)->bool:
        timeout_limit = time.time() + self.timeout
        counter       = 0
        ret           = 0

        while counter <=self.token_limit or time.time()>=timeout_limit:
            sql = self.sql_call(f"SELECT token FROM registration WHERE reg_mail = '{user.mail}'")
            if sql.empty:
                raise Error("Es gibt kein user")
            token = sql.split()[-1]

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
    p = Parser()
    conf = p.load_settings("/../settings.yml")
    #  h = Handler(conf["db_username"],conf["db_password"],conf["db_server_ip"],conf["mcrcon_password"])
    #p.load_settings("/../settings.json")
    #u = User("samuel.huwiler@gmx.ch","test","samuel")
    h = Handler("ksruser","PLbLYYSgGvfqC4j",conf.db_server_ip,conf.mcrcon_password)
if __name__ == "__main__":
    main()