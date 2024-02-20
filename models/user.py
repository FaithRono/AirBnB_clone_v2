#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column
from os import getenv


class User(BaseModel):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship('Place',
                              back_populates='user',
                              cascade='all, delete-orphan')
        reviews = relationship('Review',
                               cascade='all,delete-orphan',
                               backref='user')
    else:     
       email = ''
       password = ''
       first_name = ''
       last_name = ''
