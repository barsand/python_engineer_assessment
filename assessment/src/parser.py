import csv
import json


class CSVParser:
    def __init__(self, csv_path):
        self.read_csv(csv_path)

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
