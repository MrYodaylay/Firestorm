# TODO Finish SQLite3 backend implementation

import sqlite3
from types import NoneType
from typing import Any

from Firestorm.Backend import Backend
from Firestorm.Model import Model


class SQLite3(Backend):

    # The backend name is used in exceptions and logging
    _backend = "SQLite3"
    _dsn = "sqlite"

    # Should FireStorm ensure that the field names and types on the database exactly match the
    # annotations on the model? Typically should be true for SQL, false for NoSQL databases. If
    # _ensureFieldIntegrity is False, _ensureTypeIntegrity has no effect. If both _ensureFieldIntegrity
    # and _ensureTypeIntegrity are True, the _typeMapping dictionary must not be empty, or Firestorm will
    # throw an exception.
    _ensureFieldIntegrity = True
    _ensureTypeIntegrity = True

    # Mapping between Python types and database types, if needed. These mappings are used for introspecting the
    # database. Firestorm makes no attempt to convert data from Python types to database types, but will throw
    # an exception if the database type does not correspond to a Python type in this dictionary
    _typeMapping = {
        "NULL": NoneType,
        "INTEGER": int,
        "REAL": float,
        "TEXT": str,
        "BLOB": bytes
    }

    # A dictionary of options that will be exposed to the user. The key should be the name of the option, and the
    # values should by a tuple with a Python type in the 0th position, and either True or False in the 1st position,
    # indicating if the field is required. The configuration provided by the user is placed into the _configuration
    # dictionary.
    _configurationOptions = {
        "file_path": (str, True),
        "test": (str, False)
    }
    _configuration = {}

    def create(self, path: str, data: dict):
        """Inserts a new entry into the database, throwing an exception of it already exists"""
        pass

    def upsert(self, path: str, data: dict):
        """Updates an existing entry in the database, creating a new entry if it doesn't exist. If it does exist,
        any fields that are filled both on the database and locally will be overwritten with the local value"""
        pass

    def insert(self, path: str, data: dict):
        """Updates an existing entry in the database, creating a new entry if it doesn't exist. If it does exist,
        only fields that are empty, none, null or equivalent will be written to, existing fields will be unmodified"""
        pass

    def update(self, path: str, data: dict):
        """Updates an existing entry in the database, throwing an exception if it doesn't exist. Any fields that
        are filled both on the database and locally will be overwritten with the local value"""
        pass

    def merge(self, path: str, data: dict):
        """Updates an existing entry in the database, throwing an exception if it doesn't exist. Only fields that
         are empty, none, null or equivalent will be written to, existing fields will be unmodified"""
        pass

    def get(self, path: str, key: str, value: Any) -> dict:
        """Returns the model object corresponding an existing entry from the database"""
        self._cur.execute("SELECT * FROM [] WHERE ? = ?", [path, key, value])
        result = self._cur.fetchone()
        print("result")

    def commit(self):
        """Save any changes to the database if necessary. This is called when the save() method is called on a Model,
        or a Model used in a with statement leaves scope. """
        self._db.commit()

    def connect(self):
        """Connect to the remote database. If this backend uses a cursor type object, also get the cursor. """
        self._db = sqlite3.connect(self._configuration["filePath"])
        self._db.row_factory = sqlite3.Row
        self._cur = self._db.cursor()

    def fields(self, path: str) -> dict:
        """Returns a dictionary of the fields and types in the table or collection on the database. This method is only
        ever used by Firestorm if _ensureFieldIntegrity is set to True, to ensure that every field present in the Model
        class exists on the database. This prevents errors when inserting data into fields that do not exist"""
        pass
