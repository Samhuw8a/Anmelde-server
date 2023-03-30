from mcrcon import MCRcon

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
from errors import Error, UserError, SQLError, TokenTimeOutError, ToManyTriesError
import logging


class User(BaseModel):
    class Config:
        validate_assignment = True

    mail: str
    username: str
    name: str
    token: int = 0

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if not all(
            list(
                map(
                    bool,
                    filter(lambda x: not isinstance(x, int), self.__dict__.values()),
                )
            )
        ):
            raise UserError("einige Felder sind nicht ausgefühlt")


class Parser:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def load_settings(self, path: str) -> Settings:
        path = os.path.dirname(__file__) + path
        with open(path) as f:
            settings = yaml.load(f, Loader=yaml.FullLoader)
            return Settings(
                db_username=settings["db"]["user"],
                db_password=settings["credentials"]["password_db"],
                db_server_ip=settings["db"]["server_ip"],
                db_database=settings["db"]["db"],
                db_table=settings["db"]["table"],
                mail_password=settings["credentials"]["password_web"],
                mcrcon_password=settings["credentials"]["mcpassword"],
                mcrcon_ip=settings["rcon"]["mc_server_ip"],
                trusted_mail_suffix=settings["settings"]["trusted_mail_suffix"],
                logs=settings["settings"]["logs"],
                sender_email=settings["email"]["sender"],
                token_email=settings["email"]["token_email"],
                false_username_email=settings["email"]["false_username_email"],
                token_tries=settings["token"]["tries"],
                token_timeout=settings["token"]["timeout"] * 60,
            )

    def get_user(self, dbframe: pd.DataFrame) -> User:
        head = dbframe.head(1)
        if head.empty:
            raise SQLError("DataFrame is empty")

        mail = head.loc[0, :]["reg_mail"]
        username = head.loc[0, :]["reg_username"]
        name = head.loc[0, :]["reg_name"]
        #  mail     = str(dbframe["reg_mail"])    .strip("0 ").partition('\n')[0]
        #  username = str(dbframe["reg_username"]).strip("0 ").partition('\n')[0]
        #  name     = str(dbframe["reg_name"])    .strip("0 ").partition('\n')[0]
        return User(mail=mail, username=username, name=name)

    def mc_call(self, resp: str) -> bool:
        whitelist_add = re.compile("Added (\w*?) to the whitelist")
        if re.fullmatch(whitelist_add, resp.strip()):
            return True
        return False


class Handler:
    def __init__(
        self,
        logger: logging.Logger,
        db_username: str,
        db_pswrd: str,
        db_server_ip: str,
        mc_pswrd: str,
        token_limit: int,
        timeout: int,
    ) -> None:
        self.logger = logger
        self.db_username: str = db_username
        self.db_password: str = db_pswrd
        self.db_ip: str = db_server_ip
        self.mc_password: str = mc_pswrd
        self.token_limit: int = token_limit
        self.timeout: int = timeout

    def sql_call(self, cmd: str) -> pd.DataFrame:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/Registration"
        )
        return pd.read_sql(str(cmd), con=engine)

    def sql_update(self, cmd: str) -> None:
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_ip}/Registration"
        )
        with engine.connect() as connection:
            connection.execute(sqlalchemy.text(cmd))

    def sql_set_reg_status(self, user: User, status: int) -> None:
        self.sql_update(
            f"UPDATE registration SET reg_done = {status}.0 WHERE reg_mail ="
            f" '{user.mail}'"
        )
        self.logger.debug(f"set reg_status for user {user.mail} to {status}")

    def sql_set_reg_comment(self, user: User, comment: str) -> None:
        self.sql_update(
            f"UPDATE registration SET reg_comment = {comment} WHERE reg_mail ="
            f" '{user.mail}'"
        )
        self.logger.debug(f"updated comment for user {user.mail}")

    def sql_get_first_user(self) -> pd.DataFrame:
        self.logger.debug("Getting the first Element from the db")
        return self.sql_call(
            "SELECT * FROM registration WHERE reg_done is Null ORDER BY reg_mail"
            " LIMIT 1"
        )

    def await_token(self, user: User) -> None:
        timeout_limit = time.time() + self.timeout
        counter = 0
        ret = 0
        tries = ["0"]

        while counter <= self.token_limit and time.time() <= timeout_limit:
            sql = self.sql_call(
                f"SELECT token FROM registration WHERE reg_mail = '{user.mail}'"
            )
            if sql.empty:
                self.logger.error(
                    "SQL query didn't return a value whilst waiting for token"
                )
                raise SQLError("SQL query didn't return a value")

            token = str(sql).split()[-1]

            if token != "None":
                counter += token not in tries
                try:
                    ret = int(token)

                except ValueError:
                    self.logger.debug(f"user entered an invalid token. try:{counter}")

            if ret == user.token:
                self.logger.info("User entered the correct token")
                return
            elif token not in tries and counter:
                self.logger.debug(f"user entered a false token. try:{counter}")
                tries.append(token)

            time.sleep(5)

        if counter > self.token_limit:
            self.logger.info("user took to many tries")
            raise ToManyTriesError
        elif time.time() >= timeout_limit:
            self.logger.info(f"user: {user.mail} took to long")
            raise TokenTimeOutError

    def mcrcon_call(self, cmd: str, ip: str) -> str:
        with MCRcon(ip, self.mc_password) as mcr:
            resp = mcr.command(cmd)
            self.logger.info(resp)
        return resp


def main() -> None:
    p = Parser(logging.Logger("test"))

    conf = p.load_settings("/../template_settings.yml")
    print(conf)
    conf = p.load_settings("/../settings.yml")
    #  u = User( mail= "test", username = "test", name= "test")
    #  print(u)
    h = Handler(
        logging.Logger("test"),
        conf.db_username,
        conf.db_password,
        conf.db_server_ip,
        conf.mcrcon_password,
        3,
        5 * 60,
    )
    sq = h.sql_get_first_user()
    u = p.get_user(sq)
    print(u)
    # p.load_settings("/../settings.json")
    # u = User("samuel.huwiler@gmx.ch","test","samuel")


if __name__ == "__main__":
    main()
