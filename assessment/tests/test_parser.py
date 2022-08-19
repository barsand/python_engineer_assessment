import json
from src import parser
from base import BaseTest


class TestParser(BaseTest):
    def test_csv2json(self):
        kwargs = {
            "indent": 4,
            "sort_keys": True,
        }

        csv_parser = parser.CSVParser('./tests/data/input-parser.csv')
        result = csv_parser._json(csv_parser.raw_data, **kwargs)

        with open('./tests/data/output-parser.json') as f:
            expected = json.dumps(json.loads(f.read()), **kwargs)

        self.assertEqual(expected, result)
