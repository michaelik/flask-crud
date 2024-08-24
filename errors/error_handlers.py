from marshmallow import ValidationError
from errors.user_not_found import UserNotFoundException
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest, InternalServerError
from config.logconfig import LogConfig

# Configure logger using LogConfig class
logger = LogConfig.configure_logging()

def register_error_handlers(app):
    @app.errorhandler(UserNotFoundException)
    def handle_user_not_found_error(error):
        response = {
            'success': False,
            'status': 404,
            'message': str(error)
        }
        logger.error(f'User not found: {str(error)}')
        return response, 404

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = {
            'success': False,
            'status': 400,
            'message': str(error.messages)
        }
        logger.error(f'Validation error: {error.messages}')
        return response, 400

    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
        response = {
            'success': False,
            'status': 405,
            'message': str(error)
        }
        logger.error(f'Method not allowed: {str(error)}')
        return response, 405

    @app.errorhandler(NotFound)
    def handle_not_found_error(error):
        response = {
            'success': False,
            'status': 404,
            'message': 'Resource not found'
        }
        logger.warning(f'Resource not found: {str(error)}')
        return response, 404

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        response = {
            'success': False,
            'status': 400,
            'message': str(error)
        }
        logger.warning(f'Bad request: {str(error)}')
        return response, 400

    @app.errorhandler(InternalServerError)
    def handle_internal_server_error(error):
        response = {
            'success': False,
            'status': 500,
            'message': 'Internal server error'
        }
        logger.error(f'Internal server error: {str(error)}')
        return response, 500

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        response = {
            'success': False,
            'status': 500,
            'message': str(error)
        }
        logger.critical(f'An unexpected error occurred: {str(error)}')
        return response, 500

