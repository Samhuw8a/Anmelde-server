import unittest
from email_handler import *


class MAIL_test(unittest.TestCase):
    def test_mail(self):
        ec = Email_server(0,"test","passwort")
        ec.load_from_template("test_mail.txt")
        self.assertEqual( ec.message.replace("{mail}","test_mail") , "test test_mail" )

if __name__ == "__main__":
    unittest.main()
