import os
from flask import Flask
from flask_migrate import Migrate
import logging
from logging.handlers import TimedRotatingFileHandler
from math import ceil
from .models import FoodTruck, db
from .blueprints import error_handlers
from .views.root import RootAPI
from .views.foodtrucks.api import FoodTrucksAPI, FoodTrucksItemsAPI, FoodTrucksLocationAPI, FoodTrucksNameAPI
from .views.foodtrucks.frontend import FoodTrucksLocationMap


migrate = Migrate()


def register_get_api(app, view, endpoint, url, pk=None, pk_type='int'):
    """
    Register a view to an endpoint for a specified url. Only registers
    a GET request.

    Parameters:
        app (object): Flask app
        view (View): Flask view to register with endpoint
        endpoint (str): endpoint to register
        url (str): url to register endpoint at
        pk (str): parameter key to register with endpoint
        pk_type (str): parameter data type

    Returns:
        -
    """
    view_func = view.as_view(endpoint)
    
    # register endpoint with parameter if specified
    if pk:
        app.add_url_rule('{}<{}:{}>'.format(url, pk_type, pk), view_func=view_func,
                     methods=['GET',])
    # otherwise register endpoint without parameter and with default
    else:
        # register endpoint without parameter
        app.add_url_rule(url, view_func=view_func, defaults={pk: None}, 
                    methods=['GET',])

        app.add_url_rule(url, view_func=view_func, methods=['GET',])


def register_api(app, view, endpoint, url, pk='id', pk_type='int'):
    """
    Register a view to a REST API endpoint for a specified url. Registers
    GET, POST, PUT and DELETE endpoints.

    Parameters:
        app (object): Flask app
        view (View): Flask view to register with endpoint
        endpoint (str): endpoint to register
        url (str): url to register endpoint at
        pk (str): parameter key to register with endpoint
        pk_type (str): parameter data type

    Returns:
        -
    """
    view_func = view.as_view(endpoint)
    # register endpoint without parameter
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    
    # register endpoints with parameter
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('{}<{}:{}>'.format(url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


def register_view(app, view, endpoint, url):
    """
    Register a view to an endpoint for a specified url. Only registers
    a GET request.

    Parameters:
        app (object): Flask app
        view (View): Flask view to register with endpoint
        endpoint (str): endpoint to register
        url (str): url to register endpoint at

    Returns:
        -
    """
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=['GET',])


def create_app():
    """
    Creates a flask application using configuration defined in config.py and specified
    by environment variable APP_SETTINGS.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.url_map.strict_slashes = False

    # disable Flask-SQLAlchemy event system since it is unused
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # initialize logging to stream to files in timed increments
    interval = app.config['LOGGING_INTERVAL_HOURS']
    file_count = ceil(app.config['LOGGING_LOG_DURATION'] / interval)
    log_path = os.path.join(app.config['LOGGING_DIR'],'sf_food_trucks_app.log')
    if not os.path.exists(app.config['LOGGING_DIR']):
        os.makedirs(app.config['LOGGING_DIR'])
    handler = TimedRotatingFileHandler(log_path, when='h', interval=interval, backupCount=file_count)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    app.logger.addHandler(handler)
    
    # register views
    register_get_api(app, RootAPI, 'root_api', '/')
    register_api(app, FoodTrucksAPI, 'foodtrucks_api', '/foodtrucks/', pk='truck_id')
    register_get_api(app, FoodTrucksNameAPI, 'foodtrucks_name_api', '/foodtrucks/name/', pk='needle', pk_type='string')
    register_get_api(app, FoodTrucksItemsAPI, 'foodtrucks_items_api', '/foodtrucks/items/', pk='needle', pk_type='string')
    register_get_api(app, FoodTrucksLocationAPI, 'foodtrucks_location_api', '/foodtrucks/location')
    register_view(app, FoodTrucksLocationMap, 'foodtrucks_location_map', '/foodtrucks/location/map')
    
    # register blueprints
    app.register_blueprint(error_handlers)

    return app