import json
import sqlalchemy
from src import parser
from base import BaseTest


class TestParser(BaseTest):
    def test_csv2json(self):
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
        csv_parser.clean_data()
        self.assertEqual(len(csv_parser.people), 4)
        for p in csv_parser.people:
            self.assertEqual(
                sorted(p.keys()),
                ['Age', 'City', 'Interests', 'Name', 'PhoneNumber']
            )

    def test_db_insert(self):
        csv_parser = parser.PeopleCSVParser('./tests/data/people.csv')
        csv_parser.clean_data()
        csv_parser.to_db()

        expected_rows = {
            "people_tb": 4,
            "interests_tb": 11,
            "people_interests_tb": 14,
        }

        for k, v in expected_rows.items():
            self.assertEqual(
                len(csv_parser.db_info["connection"].execute(
                    sqlalchemy.sql.select([csv_parser.db_info[k]])
                ).fetchall()),
                v
            )
