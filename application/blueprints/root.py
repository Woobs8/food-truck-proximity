from flask import request, jsonify, abort, make_response, Blueprint, current_app
from application.models import FoodTruck, db
from sqlalchemy.exc import SQLAlchemyError


root = Blueprint('root', __name__)


@root.route('/', methods=['GET'])
def index():
    """
    Application root endpoint returns metadata about resource collection

    Returns:
        str: JSON string with resource meta data
    """
    try:
        # create dict with metadata and return as JSON
        entry_count = FoodTruck.query.count()
        lat_min = db.session.query(db.func.min(FoodTruck.latitude)).scalar()
        lat_max = db.session.query(db.func.max(FoodTruck.latitude)).scalar()
        long_min = db.session.query(db.func.min(FoodTruck.longitude)).scalar()
        long_max = db.session.query(db.func.max(FoodTruck.longitude)).scalar()
        collection_meta =   {
                                'foodtrucks': {
                                    'name':'foodtrucks',
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
    except SQLAlchemyError as e:
        current_app.logger.error('error retriveing foodtrucks metadata: %s', e)
        abort(500, 'Error retrieving foodtrucks metadata')