#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship
from models.place import Place

class User(BaseModel, Base):
    """User class"""
    __tablename__ = 'users'

    id = Column(String(60), primary_key=True, nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship('Place', backref='user', cascade='all, delete-orphan')
    else:
        @property
        def places(self):
            """getter attribute in case it gets called"""
            from models import storage
            places_list = []
            for place in storage.all(Place).values():
                if place.user_id == self.id:
                    places_list.append(place)
            return places_list
