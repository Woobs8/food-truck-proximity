from flask import request, jsonify, abort, make_response, Blueprint, current_app
from application.models import FoodTruck, db
from sqlalchemy.exc import SQLAlchemyError


foodtrucks = Blueprint('foodtrucks', __name__)


@foodtrucks.route("", methods=['GET'])
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
        current_app.logger.error('error retriveing all entries: %s', e)
        abort(500, 'Error retrieving resources')


@foodtrucks.route("/<int:truck_id>", methods=['GET'])
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
        current_app.logger.error('error retriveing entry id %d: %s', truck_id, e)
        abort(500, 'Error retriving resource with id {}'.format(truck_id))


@foodtrucks.route("/<int:truck_id>", methods=['PUT'])
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
        abort(400, 'Request must be JSON mimetype')
    if not 'name' in request.json or type(request.json['name']) != str:
        abort(400, "invalid or missing 'name' field")
    if not 'longitude' in request.json or type(request.json['longitude']) != float:
        abort(400, "invalid or missing 'longitude' field")
    if not 'latitude' in request.json or type(request.json['latitude']) != float:
        abort(400, "invalid or missing 'latitude' field")
    if not 'days_hours' in request.json or type(request.json['days_hours']) != str:
        abort(400, "invalid or missing 'dayshours' field")
    if not 'food_items' in request.json or type(request.json['food_items']) != str:
        abort(400, "invalid or missing 'food_items' field")

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
        current_app.logger.info('successfully updated entry id %d', truck_id)
        return make_response(jsonify(truck.serialize()), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error('error updating entry id %d: %s', truck_id, e)
        abort(500, 'Error updating resource with id {}'.format(truck_id))


@foodtrucks.route("/<int:truck_id>", methods=['DELETE'])
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
        FoodTruck.query.filter_by(uuid=truck_id).delete()
        db.session.commit()
        current_app.logger.info('successfully deleted entry id %d', truck_id)
        return make_response(jsonify({'message': 'Entry deleted'}), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error('error deleting entry id %d: %s', truck_id, e)
        abort(500, 'Error deleting resource with id {}'.format(truck_id))


@foodtrucks.route("/name/<string:needle>", methods=['GET'])
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
        current_app.logger.error('error searching for needle %s: %s', needle, e)
        abort(500, 'Error retriving resources by name {}'.format(needle))


@foodtrucks.route("/items/<string:needle>", methods=['GET'])
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
        current_app.logger.error('error searching for needle %s: %s', needle, e)
        abort(500, 'Error retriving resources by items {}'.format(needle))


@foodtrucks.route("/location", methods=['GET'])
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
        radius = current_app.config['DEFAULT_SEARCH_RADIUS']

    # name and item filter arguments are optional
    name = request.args.get('name')
    item = request.args.get('item')

    try:
        # query trucks within radius of position
        trucks = FoodTruck.get_food_trucks_within_radius(latitude, longitude, radius, name, item)

        return jsonify({'foodtrucks': [e.serialize() for e in trucks]})
    except ValueError:
        abort(400, 'Invalid parameter type')
    except SQLAlchemyError as e:
        current_app.logger.error('error retriveing entries by location=(%d,%d), radius=%d: %s', 
                        latitude, longitude, radius, e)
        abort(500, 'Error retriving resources near location ({},{})'.format(latitude, longitude))


@foodtrucks.route("", methods=['POST'])
def add_food_truck():
    """
    POST /foodtrucks/<id> endpoint creates a /foodtrucks resource

    The request must include JSON data specifying the field values of the resource.

    Returns:
        str: JSON representation of the created resource
    """
    # validate JSON request
    if not request.json:
        abort(400, 'Request must be JSON mimetype')
    if not 'name' in request.json or type(request.json['name']) != str:
        abort(400, "invalid or missing 'name' field")
    if not 'longitude' in request.json or type(request.json['longitude']) != float:
        abort(400, "invalid or missing 'longitude' field")
    if not 'latitude' in request.json or type(request.json['latitude']) != float:
        abort(400, "invalid or missing 'latitude' field")
    if not 'days_hours' in request.json or type(request.json['days_hours']) != str:
        abort(400, "invalid or missing 'dayshours' field")
    if not 'food_items' in request.json or type(request.json['food_items']) != str:
        abort(400, "invalid or missing'food_items' field")
    
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
        current_app.logger.info('successfully inserted entry with id %d', truck.uuid)
        return make_response(jsonify(truck.serialize()), 201)
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error('error inserting entry (%s, %d, %d, %s, %s): %s', 
                        name, latitude, longitude, days_hours, food_items, e)
        abort(500, 'Error creating resource')