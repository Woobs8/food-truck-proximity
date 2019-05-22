from flask import request, jsonify, make_response, Blueprint

# error handling blueprint
error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.errorhandler(400)
def bad_request(error):
    """
    Flask error handler for manually invoking 'bad request' response codes
    """
    return make_response(jsonify({'code': error.code, 'message': error.description}), 400)


@error_handlers.errorhandler(404)
def not_found(error):
    """
    Flask error handler for manually invoking 'resource not found' response codes
    """
    return make_response(jsonify({'code': error.code, 'message': error.description}), 404)


@error_handlers.errorhandler(500)
def internal_error(error):
    """
    Flask error handler for manually invoking 'internal server error' response codes
    """
    return make_response(jsonify({'code': error.code, 'message': error.description}), 500)