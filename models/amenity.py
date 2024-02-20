#!/usr/bin/python3
""" State Module for HBNB project """
from models.place import Place
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, Table
from os import getenv
from sqlalchemy.orm import relationship

# Define the association table for the many-to-many relationship between Place and Amenity
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
                      )

class Amenity(BaseModel, Base):
    """ Amenity class """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'amenities'

        id = Column(String(60), primary_key=True)
        name = Column(String(128), nullable=False)
        places = relationship('Place',
                              secondary=place_amenity,
                              back_populates='amenities')
    else:
        name = ""
