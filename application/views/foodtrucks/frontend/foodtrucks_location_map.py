from flask import render_template
from flask.views import MethodView


class FoodTrucksLocationMap(MethodView):
    """
    A class used to encapsulate the frontend view for the /foodtrucks/location/map endpoint

    Methods
    -------
    get()
        implements the GET /foodtrucks/location/map endpoint

    """

    def get(self):
        """
        GET /foodtrucks/location/map endpoint returns interactive map view that will illustrate
        the location of nearby foodtrucks for locations chosen by the user.
    

        Returns:
            str: html view with interactive map
        """
        return render_template('foodtrucks_location_map.html')