#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from models.city import City


class State(BaseModel, Base):
    """State class"""
    __tablename__ = 'states'

    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """getter attribute in case it gets called"""
            from models import storage
            cities_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
    else:
        cities = relationship('City', backref='state', cascade='all, delete-orphan')
