#!/usr/bin/python3
"""This module defines a class User"""

from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.base_model import BaseModel, Base
    
else:
    from models.base_model import BaseModel
    Base = object

class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = "users"

    if isinstance(Base, type):
        from sqlalchemy import Column, String
        from sqlalchemy.orm import relationship
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="all, delete-orphan")
        reviews = relationship("Review", backref="user", cascade="all, delete-orphan")

    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        @property
        def places(self):
            """Retrieves a list of Place objects linked to the User (in FileStorage mode)."""
            from models import storage
            from models.review import Place
            
            place_list = []
            for place in storage.all(Place).values():
                if self.id == place.user_id:
                    place_list.append(place)
            return place_list
        
        @property
        def reviews(self):
            """Retrieves a list of Review objects linked to the User"""
            from models import storage
            from models.review import Review
            
            review_list = []
            for review in storage.all(Review):
                if review.user_id == self.id:
                    review_list.append(review)
            return review_list


