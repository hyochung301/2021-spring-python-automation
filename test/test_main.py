import unittest
import sys
sys.path.append('../')
from src.main import main
import io

class TestMain(unittest.TestCase):
    
    # Please delete this later
    def test_ex(self):
        print("-------------------------------------------------------")
        print("Initial example test for kesa python automation project")
        output = io.StringIO()                # Create StringIO object
        sys.stdout = output                   #  and redirect stdout.
        main()                                # Call unchanged function.
        sys.stdout = sys.__stdout__           # Reset redirect.
        self.assertEqual(output.getvalue(), "Hello World\n")
        print("test_ex done")
        print("-------------------------------------------------------", end="\n\n")