#!/usr/bin/python3
""" State Module for HBNB project """
from models.place import Place
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, Table
from os import getenv
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        places = relationship('Place',
                              secondary=Place.place_amenity,
                              back_populates='amenities')
    else:
        name = ""
