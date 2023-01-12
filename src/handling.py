from   mcrcon import MCRcon

import pymysql
import sqlalchemy
import pandas as pd

import time
import yaml
import os
import re

from settings_cls import Settings
from pydantic import BaseModel, validator

from typing import Optional, Any
from errors import Error, UserError, SQLError
import logging

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
            raise UserError("einige Felder sind nicht ausgefühlt")

class Parser():
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

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
                trusted_mail_suffix  = settings['settings']["trusted_mail_suffix"],
                token_email          = settings["settings"]["token_email"],
                logs                 = settings['settings']['logs'],
                false_username_email = settings["settings"]["false_username_email"],
                output               = settings["settings"]["output"],
            )

    def get_user(self, dbframe:pd.DataFrame)->User:
        mail = dbframe.head(1).loc[0,:]["reg_mail"]
        username = dbframe.head(1).loc[0,:]["reg_username"]
        name = dbframe.head(1).loc[0,:]["reg_name"]
        #  mail     = str(dbframe["reg_mail"])    .strip("0 ").partition('\n')[0]
        #  username = str(dbframe["reg_username"]).strip("0 ").partition('\n')[0]
        #  name     = str(dbframe["reg_name"])    .strip("0 ").partition('\n')[0]
        return User(mail=mail,username=username,name=name)

    def mc_call(self,resp:str)->bool:
        # TODO: response als registriet oder falscher username identifizieren.
        whitelist_add = re.compile("Added (\w*?) to the whitelist")
        if re.fullmatch(whitelist_add,resp.strip()):
            return True
        return False

class Handler():

    def __init__(self, logger:logging.Logger,db_username:str,db_pswrd:str,db_server_ip:str, mc_pswrd:str) -> None:
        self.logger = logger
        self.db_username:str = db_username
        self.db_password:str = db_pswrd
        self.db_ip:str       = db_server_ip
        self.mc_password:str = mc_pswrd
        #TODO token_limit und timeout in settings
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
        self.logger.debug(f"set reg_status for user {user.mail} to {status}")

    def sql_set_reg_comment(self,user:User, comment:str)->None:
        self.sql_update(f"UPDATE registration SET reg_comment = {comment} WHERE reg_mail = '{user.mail}'")
        self.logger.debug(f"updated comment for user {user.mail}")

    def sql_get_first_user(self)->pd.DataFrame:
        self.logger.debug("Getting the first Element from the db")
        return self.sql_call("SELECT * FROM registration WHERE reg_done is Null ORDER BY reg_mail LIMIT 1")

    def await_token(self,user:User)->bool:
        timeout_limit = time.time() + self.timeout
        counter       = 0
        ret           = 0

        while counter <=self.token_limit or time.time()>=timeout_limit:
            sql = self.sql_call(f"SELECT token FROM registration WHERE reg_mail = '{user.mail}'")
            if sql.empty:
                self.logger.error("SQL query didn't return a value whilst waiting for token")
                raise SQLError("SQL query didn't return a value")

            token = str(sql).split()[-1]

            if token != "None":
                counter +=1
                try: ret = int(token)
                except ValueError: 
                    self.logger.debug("user entered an invalid token. try:{counter}")

            if ret == user.token:
                return True
            elif token != "None": self.logger.debug("user entered a false token. try:{counter}")

            #TODO sleep timer multiplizieren 
            time.sleep(5)

        if counter <= self.token_limit:
            self.logger.info("user took to many tries")
        else: 
            self.logger.info("user: {user.mail} took to long")
        return False

    def mcrcon_call(self,cmd:str)->str:
        #TODO ip in settings
        with MCRcon("45.154.49.72", self.mc_password) as mcr:
            resp = mcr.command(cmd)
            self.logger.info(resp)
        return resp

def main()->None:
    p = Parser(logging.Logger("test"))
    conf = p.load_settings("/../settings.yml")
    #  u = User( mail= "test", username = "test", name= "test")
    #  print(u)
    h = Handler(logging.Logger("test"),conf.db_username,conf.db_password,conf.db_server_ip,conf.mcrcon_password)
    sq = h.sql_get_first_user()
    u = p.get_user(sq)
    print(u)
    #p.load_settings("/../settings.json")
    #u = User("samuel.huwiler@gmx.ch","test","samuel")
if __name__ == "__main__":
    main()
