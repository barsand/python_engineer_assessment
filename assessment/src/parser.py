import csv
import json
import sqlalchemy
from . import utils


INTEREST_KEYS = ["Interest1", "Interest2", "Interest3", "Interest4"]


class PeopleCSVParser:
    def __init__(self, csv_path):
        self.read_csv(csv_path)

        engine = sqlalchemy.create_engine("mysql://root:root@127.0.0.1/main")
        connection = engine.connect()
        metadata = sqlalchemy.schema.MetaData(engine)

        self.db_info = {
            "engine": engine,
            "connection": connection,
            "metadata": metadata,
            "interests_tb": sqlalchemy.schema.Table(
                "Interests", metadata, autoload=True, autoload_with=engine
            ),
            "people_tb": sqlalchemy.schema.Table(
                "People", metadata, autoload=True, autoload_with=engine
            ),
            "people_interests_tb": sqlalchemy.schema.Table(
                "PeopleInterests", metadata, autoload=True, autoload_with=engine
            ),
        }

    def _json(self, obj=None, sort_keys=True, indent=4, **kwargs):
        if obj is None:
            obj = self.data
        return json.dumps(obj, sort_keys=sort_keys, indent=indent, **kwargs)

    def read_csv(self, csv_path):
        self.raw_data = list()
        with open(csv_path, "r") as f:
            csvreader = csv.DictReader(f)
            for entry in csvreader:
                self.raw_data.append(entry)

    def clean_data(self):
        self.people = list()
        self.interests = set()

        for entry in self.raw_data:
            person_interests = set()
            for i in INTEREST_KEYS:
                curr_interest = entry[i]
                if not len(curr_interest):
                    continue

                curr_interest = utils.normalize_spacing(curr_interest)
                curr_interest = utils.normalize_case(curr_interest)
                curr_interest = utils.remove_accentuation(curr_interest)
                person_interests.add(curr_interest)
                self.interests.add(curr_interest)

            if not person_interests:
                continue

            curr_city = utils.normalize_spacing(entry['City'])
            curr_city = utils.remove_accentuation(curr_city)

            self.people.append({
                'Name': utils.normalize_spacing(entry['Name']),
                'Age': entry['Age'],
                'City': curr_city,
                'PhoneNumber': utils.normalize_phone_number(entry['PhoneNumber']),
                'Interests': person_interests,
            })

    def to_db(self):
        db_info = self.db_info
        db_info["connection"].execute(db_info["interests_tb"].delete())
        db_info["connection"].execute(db_info["people_tb"].delete())
        db_info["connection"].execute(db_info["people_interests_tb"].delete())

        self.interest_slug2db_ref = dict()
        for interest in self.interests:
            res = db_info["connection"].execute(db_info["interests_tb"].insert().values({
                "slug": interest
            }))
            self.interest_slug2db_ref[interest] = res.inserted_primary_key[0]

        for person in self.people:
            res = db_info["connection"].execute(db_info["people_tb"].insert().values(**{
                "name": person["Name"],
                "age": person["Age"],
                "phone_number": person["PhoneNumber"],
                "city": person["City"],
            }))
            person["db_ref"] = res.inserted_primary_key[0]


            for interest in person["Interests"]:
                res = db_info["connection"].execute(
                    db_info["people_interests_tb"].insert().values(**{
                        "person_id": person["db_ref"],
                        "interest_id": self.interest_slug2db_ref[interest],
                    })
                )
