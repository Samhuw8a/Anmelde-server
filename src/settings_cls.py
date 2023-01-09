from   errors import Error
from pydantic import BaseModel,validator,ValidationError
from typing import List, Any
import re

class Settings(BaseModel):

    class Config:
        validate_assignment = True

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

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if not all(list(map(bool,self.__dict__.values()))):
            raise Error("einige Felder sind nicht ausgefühlt")


    def set_tms(self, n:Any)->None:
        self.trusted_mail_suffix =n

    def set_ip(self, n:Any)->None:
        self.db_server_ip =n

    def set_tmail(self,n:Any)->None:
        self.token_email = n
    def set_fumail(self,n:Any)->None:
        self.false_username_email = n

    @validator( "false_username_email","token_email")
    @classmethod
    def is_valid_path(cls,path:str)->str:
        p=re.compile("^(\/(\w+|\.{1,2}))+(\.\w+)$")
        if not re.fullmatch(p,path):
            raise Error("Kein korrekter Pfad")
        return path

    @validator("trusted_mail_suffix")
    @classmethod
    def is_correct_list(cls,tms:list)-> list:
        email=re.compile("(\w*)\.(\w*)")
        for el in tms:
            if not re.fullmatch(email,el):
                raise Error(f"Kein korrektes Email format: {el}")
        return tms

    @validator("db_server_ip")
    @classmethod
    def is_correct_ip(cls,ip:str)->str:
        splt=ip.split(".")
        if len(splt)!= 4:
            raise Error(f"Kein korrektes ip format: {ip}")
        for el in splt:
            try: int(el)
            except: raise Error(f"Kein korrektes ip format: {ip}")
            if int(el)<0 or int(el)>255:
                raise Error(f"Kein korrektes ip format: {ip}")
        return ip
