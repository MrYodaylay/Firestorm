# FUTURE Better exceptions (inherit from more appropriate standard exception?)

class UnknownBackendException(Exception):
    pass


class DuplicateBackendException(Exception):
    pass


class UnknownOptionException(Exception):
    pass


class MissingOptionException(Exception):
    pass
