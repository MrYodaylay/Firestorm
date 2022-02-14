# TODO Location API
#   - Represents a single source of data on a database, for example tables in a SQL database or collections in nosql.
# TODO Model API
#   - Represents a a group of related data points, for example a row in a relational database.
#   - Should also allow object oriented access to relationships. Attempting to access a foreign key, as in Object.fk
#       should not return the key, but a model.

from Firestorm.Exceptions import UnknownBackendException
from Firestorm.Exceptions import MissingOptionException
from Firestorm.Backend import Backend
from Firestorm.Backends import *


class Firestorm:

    def __init__(self, dsn: str, **kwargs):

        # Create instance of backend indicated by dsn
        backend_instance = None
        for backend in Backend.__subclasses__():
            if backend._dsn == dsn:
                backend_instance = backend()

        if backend_instance is None:
            raise UnknownBackendException(f"String {dsn} matches no known backend")

        # Process remaining kwargs according to backend
        config = {}
        for argument in backend_instance._configurationOptions.keys():
            conversion, required = backend_instance._configurationOptions[argument]
            if argument in kwargs:
                config[argument] = conversion(kwargs[argument])
            elif required:
                raise MissingOptionException(f"Required option {argument} was not provided")
        backend_instance._configuration = config

# Temporary testing code.
f = Firestorm("sqlite", file_path = "temp.db")
