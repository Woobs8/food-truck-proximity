from flask import request, jsonify, abort, make_response, current_app as app
from .models import FoodTruck, db
from sqlalchemy.exc import SQLAlchemyError

@app.route('/', methods=['GET'])
def index():
    """
    Application root endpoint returns metadata about resource collection

    Returns:
        str: JSON string with resource meta data
    """
    # create dict with metadata and return as JSON
    entry_count = FoodTruck.query.count()
    lat_min = db.session.query(db.func.min(FoodTruck.latitude)).scalar()
    lat_max = db.session.query(db.func.max(FoodTruck.latitude)).scalar()
    long_min = db.session.query(db.func.min(FoodTruck.longitude)).scalar()
    long_max = db.session.query(db.func.max(FoodTruck.longitude)).scalar()
    collection_meta = {
                        'foodtrucks': {
                            'name':'SF Food Truck Locator',
                            'entries':entry_count,
                            'geo_area':{
                                'min_latitude':lat_min,
                                'min_longitude':long_min,
                                'max_latitude':lat_max,
                                'max_longitude':long_max
                            }
                        }
                    }
    return jsonify(collection_meta)

@app.route("/foodtrucks", methods=['GET'])
def get_all_food_trucks():
    """
    GET /foodtrucks endpoint returns all resources in collection /foodtrucks

    Returns:
        str: JSON representation of all resources in /foodtrucks
    """
    try:
        # query all trucks in the database
        trucks = FoodTruck.query.all()
        return jsonify({'foodtrucks': [e.serialize() for e in trucks]})
    except SQLAlchemyError as e:
        app.logger.error('error retriveing all entries: %s', e)
        abort(500)

# get food truck by id
@app.route("/foodtrucks/<int:truck_id>", methods=['GET'])
def get_food_truck(truck_id):
    """
    GET /foodtrucks/<id> endpoint returns /foodtrucks resource with specific id

    Parameters:
        truck_id (int): id of truck to query (inferred from request URL)

    Returns:
        str: JSON representation of food truck with truck_id or empty dict if it does not exist
    """
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

@app.route("/foodtrucks/<int:truck_id>", methods=['PUT'])
def update_food_truck(truck_id):
    """
    PUT /foodtrucks/<id> endpoint updates or creates /foodtrucks resource with specific id

    The request must include JSON data specifying the field values of the updated resource.

    Parameters:
        truck_id (int): id of truck to query (inferred from request URL)

    Returns:
        str: JSON representation of updated or created resource
    """
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
        return make_response(jsonify(truck.serialize()), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error('error updating entry id %d: %s', truck_id, e)
        abort(500)

@app.route("/foodtrucks/<int:truck_id>", methods=['DELETE'])
def delete_food_truck(truck_id):
    """
    DELETE /foodtrucks/<id> endpoint deletes /foodtrucks resource with specific id

    Parameters:
        truck_id (int): id of truck to query (inferred from request URL)

    Returns:
        str: JSON response with success message
    """
    # delete truck with id if it exists
    try:
        truck = FoodTruck.query.filter_by(uuid=truck_id).delete()
        db.session.commit()
        app.logger.info('successfully deleted entry id %d', truck_id)
        return make_response(jsonify({'message': 'Entry deleted'}), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error('error deleting entry id %d: %s', truck_id, e)
        abort(500)

@app.route("/foodtrucks/name/<string:needle>", methods=['GET'])
def get_food_trucks_by_name(needle):
    """
    GET /foodtrucks/name/<needle> endpoint returns resources in /foodtrucks 
    filtered by content of name field

    Parameters:
        needle (str): substring that name field must contain (inferred from request URL)

    Returns:
        str: JSON representation of all resources in /foodtrucks filtered by those where the
            name field contains substring needle 
    """
    # query by trucks where needle is a case-insensitive substring of name
    try:
        trucks = FoodTruck.query.filter(FoodTruck.name.ilike('%{}%'.format(needle)))
        return jsonify({'foodtrucks': [e.serialize() for e in trucks]})
    except SQLAlchemyError as e:
        app.logger.error('error searching for needle %s: %s', needle, e)
        abort(500)

@app.route("/foodtrucks/items/<string:needle>", methods=['GET'])
def get_food_trucks_by_items(needle):
    """
    GET /foodtrucks/items/<needle> endpoint returns resources in /foodtrucks 
    filtered by content of food_items field

    Parameters:
        needle (str): substring that food_items field must contain (inferred from request URL)

    Returns:
        str: JSON representation of all resources in /foodtrucks filtered by those where the
            food_items field contains substring needle 
    """
    # query by trucks where needle is a case-insensitive substring of food_items
    try:
        trucks = FoodTruck.query.filter(FoodTruck.food_items.ilike('%{}%'.format(needle)))
        return jsonify({'foodtrucks': [e.serialize() for e in trucks]})
    except SQLAlchemyError as e:
        app.logger.error('error searching for needle %s: %s', needle, e)
        abort(500)

@app.route("/foodtrucks/location", methods=['GET'])
def get_nearby_food_trucks():
    """
    GET /foodtrucks/location/<params> endpoint returns resource in /foodtrucks within
    a specified distance of a specified location. 
    
    The request must include latitude and longitude parameters specifying the location 
    in decimal coordinates. Optionally, the request may also include the search radius
    im meters, a substring to filter results by the name field and a substring to filter 
    results by the food_items field.

    Returns:
        str: JSON representation of all resources in /foodtrucks with radius distance of location,
            filtered by those where the name and/or food_items field contain needle substrings
    """
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
        trucks = FoodTruck.get_food_trucks_within_radius(latitude, longitude, radius, name, item)

        return jsonify({'foodtrucks': [e.serialize() for e in trucks]})
    except ValueError:
        abort(400)
    except SQLAlchemyError as e:
        app.logger.error('error retriveing entries by location=(%d,%d), radius=%d: %s', 
                        latitude, longitude, radius, e)
        abort(500)

# add truck to resources
@app.route("/foodtrucks", methods=['POST'])
def add_food_truck():
    """
    POST /foodtrucks/<id> endpoint creates a /foodtrucks resource

    The request must include JSON data specifying the field values of the resource.

    Returns:
        str: JSON representation of the created resource
    """
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
        return make_response(jsonify(truck.serialize()), 201)
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error('error inserting entry (%s, %d, %d, %s, %s): %s', 
                        name, latitude, longitude, days_hours, food_items, e)
        abort(500)

# bad request
@app.errorhandler(400)
def bad_request(error):
    """
    Flask error handler for manually invoking 'bad request' response codes
    """
    return make_response(jsonify({'message': 'Bad request'}), 400)

# route not found
@app.errorhandler(404)
def not_found(error):
    """
    Flask error handler for manually invoking 'resource not found' response codes
    """
    return make_response(jsonify({'message': 'Resource not found'}), 404)

# internal server error
@app.errorhandler(500)
def internal_error(error):
    """
    Flask error handler for manually invoking 'internal server error' response codes
    """
    return make_response(jsonify({'message': 'Internal server error'}), 500)