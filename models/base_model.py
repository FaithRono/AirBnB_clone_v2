#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel(Base):
    """A base class for all hbnb models"""
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __abstract__= True

        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime,
                            nullable=False,
                            default=datetime.utcnow)
        updated_at = Column(DateTime,
                            nullable=False,
                            default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiate a new model."""
        self.id = str(uuid.uuid4())
        if not kwargs:
            self.created_at = self.updated_at = datetime.utcnow()
        else:
            self.updated_at = kwargs.get('updated_at',
                                             datetime.now())
            self.created_at = kwargs.get('created_at',
                                             datetime.now())
            if isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime\
                    (self.updated_at, '%Y-%m-%dT%H:%M:%S.%f')
            if isinstance(self.created_at, str):
                self.created_at = datetime.strptime\
                    (self.created_at, '%Y-%m-%dT%H:%M:%S.%f')

            kwargs.pop('__class__', None)

            for key, value in kwargs.items():
                setattr(self, key, str(value))

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.pop('_sa_instance_state', None)
        dictionary.update({'__class__':
                       (str(type(self)).split('.')[-1]).split('\'')[0]})
        if isinstance(self.created_at, datetime):
            dictionary['created_at'] = self.created_at.isoformat()

        if isinstance(self.updated_at, datetime):
            dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary


    def delete(self):
        """Delete current instance from storage by calling
        its delete method"""
        from models import storage
        storage.delete(self)
