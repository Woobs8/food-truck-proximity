import sys, os
from application.models import FoodTruck
import argparse
import pandas as pd
from sodapy import Socrata
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def populate_db():
    """
    Fetches data from the public API https://data.sfgov.org/resource/rqzj-sfat and stores it
    in the PostgreSQL database specified in the environment variable DATABASE_URL.
    """
    # fetch data from https://data.sfgov.org/resource/rqzj-sfat API
    client = Socrata("data.sfgov.org", None)
    trucks = pd.DataFrame.from_records(client.get("rqzj-sfat"))
    fetched = len(trucks.index)
    print('Fetched {} entries from https://data.sfgov.org/resource/rqzj-sfat'.format(fetched))

    # initialize sqlalchemy engine
    engine = create_engine(os.environ['DATABASE_URL'])
    Session = sessionmaker(bind=engine)
    session = Session()

    # iterate fetched data and insert valid entries
    pushed = 0
    try:
        for __, row in trucks.iterrows():
            name = str(row['applicant'])
            longitude = float(row['longitude'])
            latitude = float(row['latitude'])
            days_hours = str(row['dayshours'])
            food_items = str(row['fooditems'])

            # skip any row that is missing field(s)
            if 'nan' in (name, days_hours, food_items) or 0 in (longitude, latitude):
                continue

            truck = FoodTruck(
                name=name,
                longitude=longitude,
                latitude=latitude,
                days_hours=days_hours,
                food_items=food_items,
                user_id=None
            )

            session.add(truck)
            session.commit()
            pushed += 1
    except SQLAlchemyError as e:
        session.rollback()
        sys.exit('Error: {}'.format(e))
    
    print('Pushed {} entries to {}'.format(pushed, engine.url))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Helper script for populating database with data from SF food trucks API')
    populate_db()