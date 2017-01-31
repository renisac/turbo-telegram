
class RIException(Exception):
    def __init__(self, msg):
        self.msg = "{}".format(msg)

    def __str__(self):
        return self.msg


class AuthError(RIException):
    def __init__(self, msg):
        self.msg = 'Unauthorized'


class TimeoutError(RIException):
    def __init__(self, msg):
        self.msg = 'Timeout'


class InvalidSearch(RIException):
    def __init__(self, msg):
        self.msg = 'Invalid Search'


class MissingConfig(RIException):
    pass


class NotFound(RIException):
    def __init__(self, msg):
        self.msg = 'Not Found'
