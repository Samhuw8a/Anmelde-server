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

    def test_mcrcon(self):
        add_resp = "Added test to the whitelist"
        self.assertTrue(self.parser.mc_call(add_resp))
        self.assertFalse(self.parser.mc_call("Player does not exist"))
        self.assertFalse(self.parser.mc_call("Added to the whitelist"))
        self.assertFalse(self.parser.mc_call(""))
        self.assertFalse(self.parser.mc_call("Added to the Whitelist"))

    def test_load_settings(self):
        test_settings=self.parser.load_settings("/test_settings.yml") 
        self.assertIsInstance(test_settings,Settings)
        self.assertEqual(test_settings.db_username          , "register")
        self.assertEqual(test_settings.db_password          , "**************")
        self.assertEqual(test_settings.db_server_ip         , "185.101.158.55")
        self.assertEqual(test_settings.db_database          , "Registration")
        self.assertEqual(test_settings.db_table             , "registration")
        self.assertEqual(test_settings.mail_password        , "**************")
        self.assertEqual(test_settings.mcrcon_password      , "***************")
        self.assertEqual(test_settings.trusted_mail_suffix  , ["test.ch"])
        self.assertEqual(test_settings.token_email          , "/../template/Anmelde_mail.txt")
        self.assertEqual(test_settings.false_username_email , "/../template/false_username.txt")
        self.assertTrue(test_settings.output)

    #TODO: get_user,load_settings


if __name__ == "__main__":
    unittest.main()
