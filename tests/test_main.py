import unittest

import main


class TestMainFuncs(unittest.TestCase):

    def test_parse_sheet_id(self):
        url = 'https://docs.google.com/spreadsheets/d/1111222222333dkkfjlsdfj/edit?usp=sharing'
        expected_id = '1111222222333dkkfjlsdfj'
        actual_id = main.parse_sheet_id(url)
        self.assertEqual(expected_id, actual_id)
