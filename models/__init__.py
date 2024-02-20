#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""
from os import getenv
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

if getenv('HBNB_TYPE_STORAGE') == 'db':
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()

from .state import State
from .city import City
from .user import User
from .place import Place
from .amenity import Amenity
