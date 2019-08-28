from flask import request, jsonify, abort, make_response, Blueprint, current_app
from application.models import FoodTruck, User, db
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from application.views.authentication import get_token_from_header, get_user_id_from_token


class FoodTrucksAPI(MethodView):
    """
    A class used to encapsulate the API for the /foodtrucks resource

    Methods
    -------
    get(truck_id)
        implements the GET /foodtrucks endpoint

    post()
        implements the POST /foodtrucks/ endpoint

    put(truck_id)
        implements the PUT /foodtrucks/<id> endpoint

    delete(truck_id)
        implements the DELETE /foodtrucks/<id> endpoint
    """

    def get(self, truck_id):
        """
        GET /foodtrucks endpoint returns all resources in collection /foodtrucks
        or a specific food truck if truck_id is specified.

        Parameters:
            truck_id (int): id of truck to query

        Returns:
            str: JSON representation of all resources in /foodtrucks
        """
        try:
            # query all trucks in the database
            if truck_id is None:
                trucks = FoodTruck.query.all()
                return jsonify({'foodtrucks': [e.serialize() for e in trucks]})
            # query truck by id
            else:
                truck = FoodTruck.query.filter_by(uuid=truck_id).first()

                # return JSON representation if truck was found
                if truck:
                    return jsonify(truck.serialize())
                # otherwise return empty dict
                else:
                    return jsonify({})
        except SQLAlchemyError as e:
            current_app.logger.error('error retriveing resources: %s', e)
            abort(500, 'Error retrieving resources')


    def post(self):
        """
        POST /foodtrucks endpoint creates a /foodtrucks resource

        The request must include JSON data specifying the field values of the resource.

        Returns:
            str: JSON representation of the created resource
        """
        # get authentication token from request header
        auth_token = get_token_from_header()

        # return unauthorized if token is not present
        if not auth_token:
            abort(401, 'A valid token must be included')

        # get the user_id from the token
        user_id = get_user_id_from_token(auth_token)

        # get the POST data
        post_data = request.get_json()

        # validate JSON request
        if not post_data:
            abort(400, 'Request must be JSON mimetype')
        if not 'name' in post_data or type(post_data['name']) != str:
            abort(400, "invalid or missing 'name' field")
        if not 'longitude' in post_data or type(post_data['longitude']) != float:
            abort(400, "invalid or missing 'longitude' field")
        if not 'latitude' in post_data or type(post_data['latitude']) != float:
            abort(400, "invalid or missing 'latitude' field")
        if not 'days_hours' in post_data or type(post_data['days_hours']) != str:
            abort(400, "invalid or missing 'dayshours' field")
        if not 'food_items' in post_data or type(post_data['food_items']) != str:
            abort(400, "invalid or missing'food_items' field")
        
        # extract values from request
        name = post_data['name']
        longitude = post_data['longitude']
        latitude = post_data['latitude']
        days_hours = post_data['days_hours']
        food_items = post_data['food_items']

        # create and insert entry in database
        try:
            truck=FoodTruck(
                name = name,
                longitude = longitude,
                latitude = latitude,
                days_hours = days_hours,
                food_items = food_items,
                user_id = user_id
            )
            db.session.add(truck)
            db.session.commit()
            current_app.logger.info('successfully inserted food truck entry with id %d', truck.uuid)
            return make_response(jsonify(truck.serialize()), 201)
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error('error inserting food truck entry (%s, %d, %d, %s, %s): %s', 
                            name, latitude, longitude, days_hours, food_items, e)
            abort(500, 'Error creating resource')
    

    def put(self, truck_id):
        """
        PUT /foodtrucks/<id> endpoint updates or creates /foodtrucks resource with specific id

        The request must include JSON data specifying the field values of the updated resource.

        Parameters:
            truck_id (int): id of truck to query

        Returns:
            str: JSON representation of updated or created resource
        """
        # get authentication token from request header
        auth_token = get_token_from_header()

        # return unauthorized if token is not present
        if not auth_token:
            abort(401, 'A valid token must be included')

        # get the user_id from the token
        user_id = get_user_id_from_token(auth_token)
    
        # get the POST data
        post_data = request.get_json()

        # validate JSON request
        if not post_data:
            abort(400, 'Request must be JSON mimetype')
        if not 'name' in post_data or type(post_data['name']) != str:
            abort(400, "invalid or missing 'name' field")
        if not 'longitude' in post_data or type(post_data['longitude']) != float:
            abort(400, "invalid or missing 'longitude' field")
        if not 'latitude' in post_data or type(post_data['latitude']) != float:
            abort(400, "invalid or missing 'latitude' field")
        if not 'days_hours' in post_data or type(post_data['days_hours']) != str:
            abort(400, "invalid or missing 'dayshours' field")
        if not 'food_items' in post_data or type(post_data['food_items']) != str:
            abort(400, "invalid or missing 'food_items' field")

        # extract values from request
        name = post_data['name']
        longitude = post_data['longitude']
        latitude = post_data['latitude']
        days_hours = post_data['days_hours']
        food_items = post_data['food_items']
        
        # fetch truck by id and update or create if it does not exist
        try:
            truck = FoodTruck.query.filter_by(uuid=truck_id).first()

            # truck does not exist, so it is created
            if truck is None:
                truck = FoodTruck(
                    name = name,
                    longitude = longitude,
                    latitude = latitude,
                    days_hours = days_hours,
                    food_items = food_items,
                    user_id = user_id
                )
                truck.uuid = truck_id
                db.session.add(truck)
            # truck exists, so it is updated
            else:
                if truck.user_id == user_id or User.is_admin(user_id):
                    truck.name = name
                    truck.longitude = longitude
                    truck.latitude = latitude
                    truck.days_hours = days_hours
                    truck.food_items = food_items
                else:
                    abort(401, 'Not authorized to modify this resource')
            # commit changes to database
            db.session.commit()
            current_app.logger.info('successfully updated food truck entry id %d', truck_id)
            return make_response(jsonify(truck.serialize()), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error('error updating food truck entry id %d: %s', truck_id, e)
            abort(500, 'Error updating resource with id {}'.format(truck_id))
    

    def delete(self, truck_id):
        """
        DELETE /foodtrucks/<id> endpoint deletes /foodtrucks resource with specific id

        Parameters:
            truck_id (int): id of truck to query

        Returns:
            str: JSON response with success message
        """
        # get authentication token from request header
        auth_token = get_token_from_header()

        # return unauthorized if token is not present
        if not auth_token:
            abort(401, 'A valid token must be included')

        # get the user_id from the token
        user_id = get_user_id_from_token(auth_token)

        # delete truck with id if it exists
        try:
            truck = FoodTruck.query.filter_by(uuid=truck_id).first()
            if truck:
                if truck.user_id == user_id or User.is_admin(user_id):
                    FoodTruck.query.filter_by(uuid=truck_id).delete()
                    db.session.commit()
                    current_app.logger.info('successfully deleted food truck entry id %d', truck_id)
                    return make_response(jsonify({'message': 'Entry deleted'}), 200)
                else:
                    abort(401, 'Not authorized to modify this resource')
            else:
                return make_response(jsonify({'message': 'Entry deleted'}), 200)
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error('error deleting food truck entry id %d: %s', truck_id, e)
            abort(500, 'Error deleting resource with id {}'.format(truck_id))   