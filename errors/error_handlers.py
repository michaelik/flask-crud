import logging
from flask import jsonify
from marshmallow import ValidationError
from errors.user_not_found import UserNotFoundException

# Create a logger
logger = logging.getLogger(__name__)

# Create a console handler for logging
console_handler = logging.StreamHandler()

# Define a formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)  # Global log level


def register_error_handlers(app):
    @app.errorhandler(UserNotFoundException)
    def handle_user_not_found_error(error):
        logger.error(f'User not found: {str(error)}')
        return jsonify({'message': str(error)}), 404

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        logger.error(f'Validation error: {error.messages}')
        return jsonify({'errors': error.messages}), 400

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        logger.critical(f'An unexpected error occurred: {str(error)}')
        return jsonify({'message': str(error)}), 500
    #
    # @app.errorhandler(400)
    # def bad_request(error):
    #     logger.setLevel(logging.WARNING)
    #     logger.critical(f'An error occurred: {str(error)}')
    #     return jsonify({'message': 'Bad request'}), 400
    #
    # @app.errorhandler(404)
    # def not_found(error):
    #     logger.setLevel(logging.CRITICAL)
    #     logger.critical(f'An error occurred: {str(error)}')
    #     return jsonify({'message': 'Not found'}), 404
    #
    # @app.errorhandler(500)
    # def internal_server_error(error):
    #     logger.setLevel(logging.CRITICAL)
    #     logger.critical(f'An error occurred: {str(error)}')
    #     return jsonify({'message': 'Internal server error'}), 500
