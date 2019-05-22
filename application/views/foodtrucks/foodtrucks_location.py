from flask import request, jsonify, abort, make_response, Blueprint, current_app
from application.models import FoodTruck, db
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView


class FoodTrucksLocationAPI(MethodView):
    """
    A class used to encapsulate the API for the /foodtrucks/location resource

    Methods
    -------
    get(truck_id)
        implements the GET /foodtrucks/location endpoint

    """

    def get(self):
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