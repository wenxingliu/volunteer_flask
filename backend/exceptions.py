class GenericException(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class APIException(GenericException):
    def __init__(self, error, status_code):
        super(APIException, self).__init__(error, status_code)


class DBException(GenericException):
    def __init__(self, error, status_code=422):
        super(DBException, self).__init__(
            error=f"Unprocessable Entity: {error}", 
            status_code=status_code)

