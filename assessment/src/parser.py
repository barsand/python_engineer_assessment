import csv
import json
from . import utils


INTEREST_KEYS = ["Interest1", "Interest2", "Interest3", "Interest4"]


class PeopleCSVParser:
    def __init__(self, csv_path):
        self.read_csv(csv_path)
        self.clean_data()

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

            self.people.append({
                'Name': entry['Name'],
                'Age': entry['Age'],
                'City': entry['City'],
                'PhoneNumber': utils.normalize_phone_number(entry['PhoneNumber']),
                'Interests': person_interests,
            })
