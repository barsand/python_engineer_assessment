import json
import sqlalchemy
from src import parser, business
from base import BaseTest


class TestBusiness(BaseTest):
    def test_business_queries(self):
        csv_parser = parser.PeopleCSVParser("./tests/data/people.csv")
        csv_parser.clean_data()
        csv_parser.to_db()

        self.assertEqual(
            business.fetch_people_age_indicators(csv_parser.db_info),
            {"max": 66, "min": 32, "average": 55.5},
        )
        self.assertEqual(
            business.fetch_most_frequent_city(csv_parser.db_info),
            {"city": "belo horizonte", "occurrences": 3},
        )
        self.assertEqual(
            sorted(business.fetch_top_interests(csv_parser.db_info, 2)),
            ["parkour", "soccer"],
        )
