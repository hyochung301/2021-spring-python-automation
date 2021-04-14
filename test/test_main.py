import unittest
import sys
sys.path.append('../')
from src.main import main, getAccountInformation
import io

class TestMain(unittest.TestCase):

    def test_getAccountInformation(self):
        print("-------------------------------------------------------")
        print("Testing Account Information in main.py")
        accountInfo = getAccountInformation()
        self.assertIsNotNone(accountInfo)  #Check if it is not NONE
        self.assertTrue(type(accountInfo) is type({}))  #check if the type is dictioineary
        self.assertEqual(accountInfo["account_number"], "PA3C0KJPLYY2")  #check if the values match
        print("test_ex done")
        print("-------------------------------------------------------", end="\n\n")