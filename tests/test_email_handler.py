import unittest
import logging
from email_handler import *


class MAIL_test(unittest.TestCase):
    def setUp(self):
        logger = logging.Logger("test")
        logger.addHandler(logging.NullHandler())
        self.email_client = Email_server(logger,0,"test","passwort","0.0.0.0")

    def test_loading(self):
        self.email_client.load_from_template("/test_mail.txt")
        self.assertEqual( self.email_client.message.replace("{mail}","test_mail") , "test test_mail" )

if __name__ == "__main__":
    unittest.main()
