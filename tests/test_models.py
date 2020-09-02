import unittest

from models.description import Descriptions, DescriptionRow


class TestModelDescription(unittest.TestCase):
    sheet_dict = [{
        'values': [{
            'effectiveValue': {
                'stringValue': 'some test string'
            }
        }]
    }]

    def test_parsing_gs(self):
        expected_string = 'some test string'
        actual_string = Descriptions(self.sheet_dict).get_table()[0][0]
        self.assertEqual(expected_string, actual_string)

    def test_rows_equals(self):
        text = 'abc'
        row1 = DescriptionRow(text)
        row2 = DescriptionRow(text)
        self.assertEqual(row1, row2)

    def test_rows_not_equals(self):
        text = 'abc'
        row1 = DescriptionRow(text)
        row2 = DescriptionRow(text + 'def')
        self.assertNotEqual(row1, row2)

    def test_table_get(self):
        table = Descriptions(self.sheet_dict)
        self.assertEqual(table.get(0), table.rows[0])
