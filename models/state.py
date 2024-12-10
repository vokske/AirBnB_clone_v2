#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class that represents a state in the HBNB project"""
    __tablename__ = "states"

    if isinstance(Base, type):
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        name = ""
        
        @property
        def cities(self):
            """Getter attribute that returns a list of City instances with state_id equals to the current State.id. It will be the FileStorage relationship between State and City.
            """
            from models import storage
            from models.city import City
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
