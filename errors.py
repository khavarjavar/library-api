class LibraryError(Exception):
    def __init__(self, message, status):
        super().__init__(message)
        self.message = message
        self.status = status


def library_error(message, status):
    return LibraryError(message, status)


def bad_request(message):
    return library_error(message, 400)


def not_found(message):
    return library_error(message, 404)


def conflict(message):
    return library_error(message, 409)
