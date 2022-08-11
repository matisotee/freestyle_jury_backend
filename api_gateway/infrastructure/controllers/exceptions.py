from starlette.exceptions import HTTPException as StarletteHTTPException


class HTTPException(StarletteHTTPException):

    def __init__(self, error_code=None, description=None, *args, **kwargs):
        super(HTTPException, self).__init__(*args, **kwargs)
        self.error_code = error_code
        self.description = description
