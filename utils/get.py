import requests
import argparse
import os

def get_all_food_trucks(server):   
    return requests.get(server)

def get_food_truck_by_id(server, uuid):
    resource = os.path.join(server, str(uuid))
    return requests.get(resource)

def get_food_trucks_by_location(server, latitude, longitude, radius=None, name=None, item=None):
    param_str = 'latitude={}&longitude={}'.format(latitude, longitude)
    if radius:
        param_str += '&radius={}'.format(radius)

    if name:
        param_str += '&name={}'.format(name)

    if item:
        param_str += '&item={}'.format(item)

    resource = os.path.join(server, 'location?') + param_str
    return requests.get(resource)

def get_food_trucks_by_name(server, needle):
    resource = os.path.join(server, 'name', needle)
    return requests.get(resource)

def get_food_trucks_by_item(server, needle):
    resource = os.path.join(server, 'items', needle)
    return requests.get(resource)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script for fetching resources from the service')
    parser.add_argument('server', help='Server URL', type=str)
    g1 = parser.add_argument_group(title='Request Group', description='API request type')
    g2 = g1.add_mutually_exclusive_group(required=False)
    g2.add_argument('--id', help='id to query resource by', type=int)
    g2.add_argument('--loc',help='location to query resource by ([<lat> <long>])', nargs=2, type=float)
    g2.add_argument('--name',help='name to query resource by', type=str)
    g2.add_argument('--items',help='food item to query resource by', type=str)
    parser.add_argument('--radius',help='limit query by radius if relevant', type=int, required=False)
    parser.add_argument('--name_filter',help='limit query by name if relevant', type=str, required=False)
    parser.add_argument('--item_filter',help='limit query by menu item if relevant', type=str, required=False)
    args = parser.parse_args()
    
    if args.id:
        ret = get_food_truck_by_id(args.server, args.id)
    elif args.loc:
        ret = get_food_trucks_by_location(args.server, args.loc[0], args.loc[1], 
                                        args.radius, args.name_filter, args.item_filter)
    elif args.name:
        ret = get_food_trucks_by_name(args.server, args.search)
    elif args.items:
        ret = get_food_trucks_by_item(args.server, args.search)
    else:
        ret = get_all_food_trucks(args.server)
    
    print('Status code: {}'.format(ret.status_code))
    print(ret.json())