import unittest
from handling import *
from errors import Error, ConfigError
from typing import Any
from pydantic import ValidationError


class test_User(unittest.TestCase):
    def setUp(self):
        self.user = User(mail="Test_mail", username="Test_username", name="Test_name")

    def set_false_args(self):
        user = User(mail="", username="Test_username", name="Test_name")

    def set_token(self, token: str):
        self.user.token = token

    def test_false_args(self):
        self.assertRaises(UserError, self.set_false_args)

    def test_fields(self):
        self.assertEqual(self.user.mail, "Test_mail")
        self.assertEqual(self.user.username, "Test_username")
        self.assertEqual(self.user.name, "Test_name")

    def test_token(self):
        self.assertEqual(self.user.token, 0)
        self.user.token = 1234
        self.assertEqual(self.user.token, 1234)
        self.assertRaises(ValidationError, self.set_token, "test_string")


class test_Parser(unittest.TestCase):
    def setUp(self):
        logger = logging.Logger("test")
        logger.addHandler(logging.NullHandler())
        self.parser = Parser(logger)

    def test_mcrcon(self):
        add_resp = "Added test to the whitelist"
        self.assertTrue(self.parser.mc_call(add_resp))
        self.assertFalse(self.parser.mc_call("Player does not exist"))
        self.assertFalse(self.parser.mc_call("Added to the whitelist"))
        self.assertFalse(self.parser.mc_call(""))
        self.assertFalse(self.parser.mc_call("Added to the Whitelist"))

    def test_load_settings(self):
        test_settings = self.parser.load_settings("/test_settings.yml")
        self.assertIsInstance(test_settings, Settings)

    # TODO: get_user,load_settings


if __name__ == "__main__":
    unittest.main()
