import requests
import argparse
import os

def delete_food_truck(server, uuid):   
    resource = os.path.join(server, str(uuid))
    return requests.delete(resource)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script for deleting a food truck from the service database')
    parser.add_argument('server', help='Server URL', type=str)
    parser.add_argument('uuid', help='UUID of food truck to update', type=int)
    args = parser.parse_args()

    ret = delete_food_truck(args.server,
                        args.uuid)
    print('Status code: {}'.format(ret.status_code))
    print(ret.json())