import unittest
import errors
import handling
import email_handler

class ERROR_tests(unittest.TestCase):
    def test_error(self):
        e = errors.Error("test")
        self.assertEqual(str(e),"test")


class MAIL_test(unittest.TestCase):
    # Email_client
    ec = email_handler.Email_server(0,"test","passwort")
    ec.load_from_template("template/test_mail.txt")
    assert ec.message.replace("{mail}","test_mail") =="test test_mail" 

if __name__ == "__main__":
    unittest.main()
