import unittest
from src import errors
from src import handling
from src import email_handler

class ERROR_tests(unittest.TestCase):
    def f(self):
        raise errors.Error("test")

    def test_error(self):
        e = errors.Error("test")
        self.assertEqual(str(e),"test")
        self.assertRaises(errors.Error,self.f)


class MAIL_test(unittest.TestCase):
    # Email_client
    def test_mail(self):
        ec = email_handler.Email_server(0,"test","passwort")
        ec.load_from_template("template/test_mail.txt")
        self.assertEqual( ec.message.replace("{mail}","test_mail") , "test test_mail" )

class HANDLING_test(unittest.TestCase):

    def test_User(self):
        u = handling.User("Test_mail","Test_username","Test_name")

        self.assertEqual(u.mail,"Test_mail")
        self.assertEqual(u.username,"Test_username")
        self.assertEqual(u.name,"Test_name")

        self.assertEqual(u.token,0)
        u.token=1234
        self.assertEqual(u.token,1234)

        self.assertEqual(repr(u),"User(Test_mail,Test_username,Test_name)")

    def test_Parser(self):
        p = handling.Parser()
        test_config={ "db_username": "register", "db_password":"**************", "db_server_ip":"185.101.158.55", "db_database":"Registration", "db_table":"registration", "mail_password":"**************", "mcrcon_password":"***************", }
        self.assertDictEqual(p.load_config("test_config.ini"),test_config)
        "TODO: get_user,mc_call,load_settings"

    def test_Handler(self):
        pass

if __name__ == "__main__":
    unittest.main()
