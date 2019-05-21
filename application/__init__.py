import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import TimedRotatingFileHandler
from math import ceil


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """
    Creates a flask application using configuration defined in config.py and specified
    by environment variable APP_SETTINGS.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ['APP_SETTINGS'])

    # disable Flask-SQLAlchemy event system since it is unused
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize database
    db.init_app(app)

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

    with app.app_context():
        # import routes
        from . import routes

        # initialize extensions
        db.init_app(app)
        migrate.init_app(app, db)
        app.logger.addHandler(handler)

        return app