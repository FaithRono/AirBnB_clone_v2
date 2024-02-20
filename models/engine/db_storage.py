#!/usr/bin/python3
"""Database Storage Module"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

mapped_classes = {"User": User, "BaseModel": BaseModel,
                  "Place": Place, "State": State,
                  "City": City, "Amenity": Amenity,
                  "Review": Review}


class DBStorage():
    """class that defines a storage methods for the class"""
    __engine = None
    __session = None

    def __init__(self):
        """class initialization"""
        try:
            from models.base_model import Base

            self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                         .format(getenv('HBNB_MYSQL_USER'),
                                                 getenv('HBNB_MYSQL_PWD'),
                                                 getenv('HBNB_MYSQL_HOST'),
                                                 getenv('HBNB_MYSQL_DB')),
                                          pool_pre_ping=True)
            Base.metadata.create_all(self.__engine)

        except Exception as e:
            print(f"Error connecting to the Database: {e}")

    def all(self, cls=None):
        """ Returns a dict of all objs"""
        if not self.__session:
            self.reload()

        objects = {}
        if isinstance(cls, str):
            cls = mapped_classes.get(cls, None)

        query_classes = [cls] if cls else mapped_classes.values()

        for query_cls in query_classes:
            for obj in self.__session.query(query_cls).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj

        return objects

    def new(self, obj):
        """ adds session to workflow"""
        self.__session.add(obj)

    def save(self):
        """saves session to the db"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes a session from the db"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Reloads a session for CRUD"""
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)
    def close(self):
        """Ends/closes a session"""
        self.__session.remove()
