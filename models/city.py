#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from os import getenv
from sqlalchemy.orm import relationship


class City(BaseModel):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        id = Column(String, primary_key=True)
        id = Column(String(60), ForeignKey("states.id"),
                          nullable=False)
        places = relationship('Place',
                              backref='cities',
                              cascade='all, delete-orphan')

    else:
        state_id = ""
        name = ""
