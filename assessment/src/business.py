import sqlalchemy


def fetch_people_age_indicators(db_info):
    res = db_info["connection"].execute(
        """
        SELECT min(age) as min, max(age) as max, avg(age) as avg
        FROM main.People
    """
    )
    min_age, max_age, avg_age = res.fetchone()
    return {"min": min_age, "max": max_age, "average": float(round(avg_age, 1))}


def fetch_most_frequent_city(db_info):
    res = db_info["connection"].execute(
        """
        SELECT city, COUNT(city) AS occurrences
        FROM main.People
        GROUP BY city
        ORDER BY occurrences DESC
        LIMIT 1
    """
    )
    city, occurrences = res.fetchone()
    return {
        "city": city,
        "occurrences": occurrences,
    }


def fetch_top_interests(db_info, count=2):
    res = db_info["connection"].execute(
        f"""
        SELECT slug FROM
        (
            SELECT interest_id, COUNT(interest_id) as occurrences
            FROM main.PeopleInterests
            GROUP BY interest_id
            ORDER BY occurrences DESC
            LIMIT {count}
        ) AS q
        JOIN main.Interests
        ON q.interest_id = main.Interests.id
    """
    )
    return [i[0] for i in res]
