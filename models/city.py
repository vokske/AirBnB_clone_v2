#!/usr/bin/python3
""" City Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """ The city class that represents a city in the HBNB project."""
    __tablename__ = "cities"
    
    if isinstance(Base, type):
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship("Place", backref="cities", cascade="all, delete, delete-orphan")

    else:
        name = ""
        state_id = ""