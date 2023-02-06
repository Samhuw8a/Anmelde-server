import unittest
from errors import *


def f():
    raise Error("Test")


class test_Errors(unittest.TestCase):
    def test_error(self):
        e = Error("test")
        self.assertEqual(str(e), "test")
        self.assertRaises(Error, f)


if __name__ == "__main__":
    unittest.main()
