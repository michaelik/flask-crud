class ResponseHelper:

    @staticmethod
    def base_response(success, status, message, data=None):
        response = {
            'success': success,
            'status': status,
            'message': message
        }
        if data is not None:
            response['data'] = data

        return response, status
