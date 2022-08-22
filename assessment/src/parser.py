import os
import sys
import csv
import json
import logging
import sqlalchemy
from . import utils


INTEREST_KEYS = ["Interest1", "Interest2", "Interest3", "Interest4"]


class PeopleCSVParser:
    def __init__(self, csv_path):
        logger = logging.getLogger()
        logging.basicConfig(
            stream = sys.stdout,
            filemode = "w",
            format = "%(levelname)s %(asctime)s - %(message)s",
            level = os.environ.get('LOGLEVEL', logging.INFO)
        )

        logger.info("establishing database connection")
        try:
            engine = sqlalchemy.create_engine(
                os.environ.get("DB_URL", "mysql://root:root@database/main")
            )

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
            logger.info("connection established")
        except Exception as e:
            logger.error("could not connect to database")
            logger.error(str(e))
            sys.exit()

        self.read_csv(csv_path)


    def _json(self, obj=None, sort_keys=True, indent=4, **kwargs):
        if obj is None:
            obj = self.data
        return json.dumps(obj, sort_keys=sort_keys, indent=indent, **kwargs)

    def read_csv(self, csv_path, export_json=True):
        logger = logging.getLogger()
        logger.info("starting csv reading")
        self.raw_data = list()
        with open(csv_path, "r") as f:
            csvreader = csv.DictReader(f)
            for entry in csvreader:
                self.raw_data.append(entry)
        logger.info("csv reading finished")

        if export_json:
            logger.info("starting json export")
            with open(os.environ.get("JSON_OUTPATH", "/data/parsed.json"), "w") as f:
                f.write(json.dumps(self.raw_data))
            logger.info("json export finished")

    def clean_data(self):
        logger = logging.getLogger()
        logger.info("starting data cleaning for %d entries")
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
            curr_city = utils.normalize_case(entry['City'])
            curr_city = utils.remove_accentuation(curr_city)

            self.people.append({
                'Name': utils.normalize_spacing(entry['Name']),
                'Age': entry['Age'],
                'City': curr_city,
                'PhoneNumber': utils.normalize_phone_number(entry['PhoneNumber']),
                'Interests': person_interests,
            })
        logger.info("data cleaning finished")

    def to_db(self):
        logger = logging.getLogger()
        logger.info("starting database insertions")
        db_info = self.db_info
        logger.info("erasing data from previous executions")
        db_info["connection"].execute(db_info["interests_tb"].delete())
        db_info["connection"].execute(db_info["people_tb"].delete())
        db_info["connection"].execute(db_info["people_interests_tb"].delete())

        self.interest_slug2db_ref = dict()
        count = 0
        logger.info("inserting %d records on `Interests` table" % len(self.interests))
        for interest in self.interests:
            count += 1
            if count % 1000 == 0:
                logger.info("%d records inserted" % count)

            res = db_info["connection"].execute(db_info["interests_tb"].insert().values({
                "slug": interest
            }))
            self.interest_slug2db_ref[interest] = res.inserted_primary_key[0]
        logger.info("insertion finished")


        count = 0
        logger.info("inserting %d records on `People` table" % len(self.people))
        for person in self.people:
            count += 1
            if count % 1000 == 0:
                logger.info("%d records inserted" % count)
            res = db_info["connection"].execute(db_info["people_tb"].insert().values(**{
                "name": person["Name"],
                "age": person["Age"],
                "phone_number": person["PhoneNumber"],
                "city": person["City"],
            }))
            person["db_ref"] = res.inserted_primary_key[0]


            for interest in person["Interests"]:
                logger.debug("inserting data on `PeopleInterests` table")
                res = db_info["connection"].execute(
                    db_info["people_interests_tb"].insert().values(**{
                        "person_id": person["db_ref"],
                        "interest_id": self.interest_slug2db_ref[interest],
                    })
                )
            logger.debug("insertion finished")
        logger.info("insertion finished")

        logger.info("database update finished")
