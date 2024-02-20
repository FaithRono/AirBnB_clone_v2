#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from os import getenv

class City(BaseModel):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'

    if getenv("HBNB-TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("state.id"), nullable=False)
        place = relationship('place', back_populates='cities',
                            cascades='all, delete-orphan')
    else:
        state_id = ""
        name = ""
