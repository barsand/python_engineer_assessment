import json
from src import parser
from base import BaseTest


class TestParser(BaseTest):
    def _test_csv2json(self):
        kwargs = {
            "indent": 4,
            "sort_keys": True,
        }

        csv_parser = parser.PeopleCSVParser('./tests/data/input-parser.csv')
        result = csv_parser._json(csv_parser.raw_data, **kwargs)

        with open('./tests/data/output-parser.json') as f:
            expected = json.dumps(json.loads(f.read()), **kwargs)

        self.assertEqual(expected, result)

    def test_csv_clean(self):
        csv_parser = parser.PeopleCSVParser('./tests/data/people.csv')
        self.assertEqual(len(csv_parser.people), 9)
        for p in csv_parser.people:
            self.assertEqual(
                sorted(p.keys()),
                ['Age', 'City', 'Interests', 'Name', 'PhoneNumber']
            )
