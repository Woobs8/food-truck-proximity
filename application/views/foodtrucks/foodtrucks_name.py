from flask import request, jsonify, abort, make_response, Blueprint, current_app
from application.models import FoodTruck, db
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView


class FoodTrucksNameAPI(MethodView):
    """
    A class used to encapsulate the API for the /foodtrucks/name resource

    Methods
    -------
    get(truck_id)
        implements the GET /foodtrucks/name/<string: needle> endpoint

    """

    def get(self, needle):
        """
        GET /foodtrucks/name/<needle> endpoint returns resources in /foodtrucks 
        filtered by content of name field

        Parameters:
            needle (str): substring that name field must contain (inferred from request URL)

        Returns:
            str: JSON representation of all resources in /foodtrucks filtered by those where the
                name field contains substring needle 
        """
        # search needle must be defined
        if not needle:
            abort(400, 'Missing parameter')

        # query by trucks where needle is a case-insensitive substring of name
        try:
            trucks = FoodTruck.query.filter(FoodTruck.name.ilike('%{}%'.format(needle)))
            return jsonify({'foodtrucks': [e.serialize() for e in trucks]})
        except SQLAlchemyError as e:
            current_app.logger.error('error searching for needle %s: %s', needle, e)
            abort(500, 'Error retriving resources by name {}'.format(needle))