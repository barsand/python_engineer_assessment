import os
from . import business, parser
from flask import Flask

app = Flask(__name__)
csv_parser = parser.PeopleCSVParser(os.environ.get("CSV_PATH", "/data/people.csv"))
csv_parser.clean_data()
csv_parser.to_db()


@app.route("/")
def home():
    return {
        "api routes": {
            "age insights (min, max and average)": "/insigts/ages",
            "cities insights (most frequent)": "/insigts/cities",
            "interests insights (top 5 interests)": "/insigts/interests",
        }
    }

@app.route("/insights/ages")
def age():
    return business.fetch_people_age_indicators(csv_parser.db_info)

@app.route("/insights/cities")
def cities():
    return business.fetch_most_frequent_city(csv_parser.db_info)

@app.route("/insights/interests")
def interests():
    return business.fetch_top_interests(csv_parser.db_info, 5)
