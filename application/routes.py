from flask import request, jsonify, abort, make_response, current_app as app
from .models import FoodTruck, db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

# application root
@app.route('/', methods=['GET', 'POST'])
def index():
    # create dict with metadata and return as JSON
    entry_count = FoodTruck.query.count()
    lat_min = db.session.query(db.func.min(FoodTruck.latitude)).scalar()
    lat_max = db.session.query(db.func.max(FoodTruck.latitude)).scalar()
    long_min = db.session.query(db.func.min(FoodTruck.longitude)).scalar()
    long_max = db.session.query(db.func.max(FoodTruck.longitude)).scalar()
    collection_meta = {'name':'SF Food Truck Locator',
                        'entries':entry_count,
                        'geo_area':{
                        'min_latitude':lat_min,
                        'min_longitude':long_min,
                        'max_latitude':lat_max,
                        'max_longitude':long_max}}
    return jsonify(collection_meta)

# get all food trucks
@app.route("/foodtrucks", methods=['GET'])
def get_all_food_trucks():
    try:
        # query all trucks in the database
        trucks = FoodTruck.query.all()
        return jsonify([e.serialize() for e in trucks])
    except SQLAlchemyError as e:
        app.logger.error('error retriveing all entries: %s', e)
        abort(500)

# get food truck by id
@app.route("/foodtrucks/<int:truck_id>", methods=['GET'])
def get_food_truck(truck_id):
    try:
        # query truck by id
        truck = FoodTruck.query.filter_by(uuid=truck_id).first()

        # return JSON representation if truck was found
        if truck:
            return jsonify(truck.serialize())
        # otherwise return empty dict
        else:
            return jsonify({})
    except SQLAlchemyError as e:
        app.logger.error('error retriveing entry id %d: %s', truck_id, e)
        abort(500)

# update truck by id or create if it does not exist
@app.route("/foodtrucks/<int:truck_id>", methods=['PUT'])
def update_food_truck(truck_id):
    # validate JSON request
    if not request.json:
        abort(400)
    if not 'name' in request.json or type(request.json['name']) != str:
        abort(400)
    if not 'longitude' in request.json or type(request.json['longitude']) != float:
        abort(400)
    if not 'latitude' in request.json or type(request.json['latitude']) != float:
        abort(400)
    if not 'days_hours' in request.json or type(request.json['days_hours']) != str:
        abort(400)
    if not 'food_items' in request.json or type(request.json['food_items']) != str:
        abort(400)

    # extract values from request
    name = request.json['name']
    longitude = request.json['longitude']
    latitude = request.json['latitude']
    days_hours = request.json['days_hours']
    food_items = request.json['food_items']
    
    # fetch truck by id and update or create if it does not exist
    try:
        truck = FoodTruck.query.filter_by(uuid=truck_id).first()

        # truck does exist, so it is created
        if truck is None:
            truck = FoodTruck(
                name = name,
                longitude = longitude,
                latitude = latitude,
                days_hours = days_hours,
                food_items = food_items
            )
            truck.uuid = truck_id
            db.session.add(truck)
        # truck exists, so it is updated
        else:
            truck.name = request.json.get('name', truck.name)
            truck.longitude = request.json.get('longitude', truck.longitude)
            truck.latitude = request.json.get('latitude', truck.latitude)
            truck.days_hours = request.json.get('days_hours', truck.days_hours)
            truck.food_items = request.json.get('food_items', truck.food_items)
        
        # commit changes to database
        db.session.commit()
        app.logger.info('successfully updated entry id %d', truck_id)
        return make_response(jsonify({'food_truck': truck.serialize()}), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error('error updating entry id %d: %s', truck_id, e)
        abort(500)

# delete truck by id
@app.route("/foodtrucks/<int:truck_id>", methods=['DELETE'])
def delete_food_truck(truck_id):
    # delete truck with id if it exists
    try:
        truck = FoodTruck.query.filter_by(uuid=truck_id).delete()
        db.session.commit()
        app.logger.info('successfully deleted entry id %d', truck_id)
        return make_response(jsonify({'succes': 'Entry deleted'}), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error('error deleting entry id %d: %s', truck_id, e)
        abort(500)

# get trucks by name
@app.route("/foodtrucks/name/<string:needle>", methods=['GET'])
def get_food_trucks_by_name(needle):
    # format search string
    needle = '%{}%'.format(needle)

    # query by trucks where needle is a case-insensitive substring of name
    try:
        trucks = FoodTruck.query.filter(FoodTruck.name.ilike(needle))
        return jsonify([e.serialize() for e in trucks])
    except SQLAlchemyError as e:
        app.logger.error('error searching for needle %s: %s', needle, e)
        abort(500)

# get trucks by menu items
@app.route("/foodtrucks/items/<string:needle>", methods=['GET'])
def get_food_trucks_by_items(needle):
    # format search string
    needle = '%{}%'.format(needle)

    # query by trucks where needle is a case-insensitive substring of food_items
    try:
        trucks = FoodTruck.query.filter(FoodTruck.food_items.ilike(needle))
        return jsonify([e.serialize() for e in trucks])
    except SQLAlchemyError as e:
        app.logger.error('error searching for needle %s: %s', needle, e)
        abort(500)

# get trucks within radius from location
@app.route("/foodtrucks/location", methods=['GET'])
def get_nearby_food_trucks():
    # geo-position arguments are required - 400 returned if both are not present
    longitude = request.args['longitude']
    latitude = request.args['latitude']

    # search radius argument is optional (default if not present)
    radius = request.args.get('radius')
    if radius is None:
        radius = app.config['DEFAULT_SEARCH_RADIUS']

    # name and item filter arguments are optional
    name = request.args.get('name')
    item = request.args.get('item')

    try:
        # query trucks within radius of position
        trucks = FoodTruck.get_food_trucks_within_radius(longitude, latitude, radius)

        # filter results by name
        if name:
            name = name.lower()
            trucks = [e for e in trucks if name in e.name.lower()]

        # filter results by menu items
        if item:
            item = item.lower()
            trucks = [e for e in trucks if item in e.food_items.lower()]

        return jsonify([e.serialize() for e in trucks])
    except ValueError:
        abort(400)
    except SQLAlchemyError as e:
        app.logger.error('error retriveing entries by location=(%d,%d), radius=%d: %s', 
                        latitude, longitude, radius, e)
        abort(500)

# add truck to resources
@app.route("/foodtrucks", methods=['POST'])
def add_food_truck():
    # validate JSON request
    if not request.json:
        abort(400)
    if not 'name' in request.json or type(request.json['name']) != str:
        abort(400)
    if not 'longitude' in request.json or type(request.json['longitude']) != float:
        abort(400)
    if not 'latitude' in request.json or type(request.json['latitude']) != float:
        abort(400)
    if not 'days_hours' in request.json or type(request.json['days_hours']) != str:
        abort(400)
    if not 'food_items' in request.json or type(request.json['food_items']) != str:
        abort(400)
    
    # extract values from request
    name = request.json['name']
    longitude = request.json['longitude']
    latitude = request.json['latitude']
    days_hours = request.json['days_hours']
    food_items = request.json['food_items']

    # create and insert entry in database
    try:
        truck=FoodTruck(
            name = name,
            longitude = longitude,
            latitude = latitude,
            days_hours = days_hours,
            food_items = food_items
        )
        db.session.add(truck)
        db.session.commit()
        app.logger.info('successfully inserted entry with id %d', truck.uuid)
        return make_response(jsonify({'food_truck': truck.serialize()}), 201)
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error('error inserting entry (%s, %d, %d, %s, %s): %s', 
                        name, latitude, longitude, days_hours, food_items, e)
        abort(500)

# bad request
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

# route not found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

# internal server error
@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error': 'Internal server error'}), 500)