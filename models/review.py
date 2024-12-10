#!/usr/bin/python3
""" Review module for the HBNB project """

from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.base_model import BaseModel, Base
else:
    from models.base_model import BaseModel
    Base = object

class Review(BaseModel, Base):
    """ Review class to store review information """
    __tablename__ = "reviews"

    if isinstance(Base, type):
        from sqlalchemy import Column, String, ForeignKey

        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        text = Column(String(1024), nullable=False)

    else:
        place_id = ""
        user_id = ""
        text = ""