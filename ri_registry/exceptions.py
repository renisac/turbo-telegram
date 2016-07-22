
class RIException(Exception):
    def __init__(self, msg):
        self.msg = "{}".format(msg)

    def __str__(self):
        return self.msg


class AuthError(RIException):
    pass


class TimeoutError(RIException):
    pass


class InvalidSearch(RIException):
    pass


class MissingConfig(RIException):
    pass

