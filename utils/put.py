import requests
import argparse
import os

def update_food_truck(server, uuid, name, latitude, longitude, days_hours, food_items):
    params = {'name': str(name),
            'latitude':float(latitude),
            'longitude':float(longitude),
            'days_hours':str(days_hours),
            'food_items':str(food_items)}
    
    resource = os.path.join(server, str(uuid))
    return requests.put(resource, json=params)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script for updating a food truck in the service database')
    parser.add_argument('server', help='Server URL', type=str)
    parser.add_argument('uuid', help='UUID of food truck to update', type=int)
    parser.add_argument('name', help='Name of food truck to add', type=str)
    parser.add_argument('latitude', help='Latitude of food truck position in decimal format', type=float)
    parser.add_argument('longitude', help='Longitude of food truck position in decimal format', type=float)
    parser.add_argument('dayshours', help='Business days/hours', type=str)
    parser.add_argument('fooditems', help='Menu items', type=str)
    args = parser.parse_args()

    ret = update_food_truck(args.server,
                        args.uuid,
                        args.name,
                        args.latitude,
                        args.longitude,
                        args.dayshours,
                        args.fooditems)
    print('Status code: {}'.format(ret.status_code))
    print(ret.json())