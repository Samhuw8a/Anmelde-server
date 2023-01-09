import unittest
from errors import Error
from settings_cls import *
from pydantic import ValidationError 

class test_Settings(unittest.TestCase):
    def set_false_args(self):
        self.settings = Settings(
            db_username     = "",
            db_password     = "test",
            db_server_ip    = "0.0.0.0",
            db_database     = "test",
            db_table        = "test",
            mail_password   = "test",
            mcrcon_password = "test",
            trusted_mail_suffix=["test.ch"],
            token_email= "/token_email.txt",
            false_username_email= "/false_username_email.txt",
            output = True
        )

    def setUp(self):
        self.settings = Settings(
            db_username     = "test",
            db_password     = "test",
            db_server_ip    = "0.0.0.0",
            db_database     = "test",
            db_table        = "test",
            mail_password   = "test",
            mcrcon_password = "test",
            trusted_mail_suffix=["test.ch"],
            token_email= "/token_email.txt",
            false_username_email= "/false_username_email.txt",
            output = True
        )

    def test_false_args(self):
        self.assertRaises(Error, self.set_false_args)

    def test_paths(self):
        self.assertRaises(Error,self.settings.set_tmail,1234)

        self.assertRaises(Error,self.settings.set_tmail,"/tsetset/../")
        self.assertRaises(Error,self.settings.set_tmail,"/test/")
        self.assertRaises(Error,self.settings.set_tmail,".py")
        self.settings.token_email="/../tes.test"

        self.assertRaises(Error,self.settings.set_fumail,"/tsetset/../")
        self.assertRaises(Error,self.settings.set_fumail,"/test/")
        self.assertRaises(Error,self.settings.set_fumail,".py")
        self.settings.false_username_email="/../tes.test"

    def test_server_ip(self):
        self.assertRaises(Error,self.settings.set_ip,1234)
        self.assertRaises(Error,self.settings.set_ip,"1.1000.2.3")
        self.assertRaises(Error,self.settings.set_ip,"1.1.3")
        self.assertRaises(Error,self.settings.set_ip,"1.abs.3.255")

    def test_tms(self):
        self.assertRaises(ValidationError,self.settings.set_tms,"test")
        self.assertRaises(Error,self.settings.set_tms,["test","@sluz.ch"])
        self.assertRaises(Error,self.settings.set_tms,["test"])

if __name__ == "__main__":
    unittest.main()
