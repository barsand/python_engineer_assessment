import unittest


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.csv_path = "./tests/data/people.csv"
