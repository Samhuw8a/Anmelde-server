import unittest
from handling import *
from errors import Error

class test_User(unittest.TestCase):
    def setUp(self):
        self.user = User("Test_mail","Test_username","Test_name")

    def set_token(self,token:str):
        self.user.token=token

    def test_User(self):
        self.assertEqual(self.user.mail,"Test_mail")
        self.assertEqual(self.user.username,"Test_username")
        self.assertEqual(self.user.name,"Test_name")

        self.assertEqual(self.user.token,0)
        self.assertEqual(self.user.token_internal,None)
        self.user.token=1234
        self.assertEqual(self.user.token,1234)
        self.assertRaises(Error ,self.set_token,"test_string")

        self.assertEqual(repr(self.user),"User(Test_mail,Test_username,Test_name)")

class test_Parser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_config(self):
        test_config={ "db_username": "register", "db_password":"**************", "db_server_ip":"185.101.158.55", "db_database":"Registration", "db_table":"registration", "mail_password":"**************", "mcrcon_password":"***************", }
        self.assertDictEqual(self.parser.load_config("/test_config.ini"),test_config)

    def test_mcrcon(self):
        add_resp = "Added test to the whitelist"
        self.assertTrue(self.parser.mc_call(add_resp))
        self.assertFalse(self.parser.mc_call("Player does not exist"))
        self.assertFalse(self.parser.mc_call("Added to the whitelist"))
        self.assertFalse(self.parser.mc_call(""))
        self.assertFalse(self.parser.mc_call("Added to the Whitelist"))

    #TODO: get_user,load_settings


if __name__ == "__main__":
    unittest.main()
