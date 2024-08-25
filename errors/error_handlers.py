from marshmallow import ValidationError
from errors.user_not_found import UserNotFoundException
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest
from dtos.response_helper import ResponseHelper
from config.logconfig import LogConfig

# Configure logger using LogConfig class
logger = LogConfig.configure_logging()


def register_error_handlers(app):
    # Handle UserNotFoundException
    @app.errorhandler(UserNotFoundException)
    def handle_user_not_found_error(error):
        logger.error(f'User not found: {str(error)}')
        return ResponseHelper.base_response(
            False,
            404,
            str(error.messages)
        )

    # Handle ValidationError from Marshmallow
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        logger.error(f'Validation error: {error.messages}')
        return ResponseHelper.base_response(
            False,
            400,
            str(error.messages)
        )

    # Handle MethodNotAllowed (e.g., POST request to a GET route)
    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
        logger.error(f'Method not allowed: {str(error)}')
        return ResponseHelper.base_response(
            False,
            405,
            str(error)
        )

    # Handle NotFound (e.g., invalid path variables)
    @app.errorhandler(NotFound)
    def handle_not_found_error(error):
        logger.warning(f'Resource not found: {str(error)}')
        return ResponseHelper.base_response(
            False,
            404,
            'Resource not found'
        )

    # Handle BadRequest (e.g., invalid request parameters)
    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        logger.warning(f'Bad request: {str(error)}')
        return ResponseHelper.base_response(
            False,
            400,
            str(error)
        )

    # Handle other generic exceptions
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        logger.critical(f'An unexpected error occurred: {str(error)}')
        return ResponseHelper.base_response(
            False,
            500,
            str(error)
        )
