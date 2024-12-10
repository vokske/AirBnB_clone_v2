#!/usr/bin/python3
""" Place Module for HBNB project """

from os import getenv
from sqlalchemy import Table, Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column("place_id", String(60), ForeignKey("places.id"), primary_key=True, nullable=False),
        Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False),)


else:
    from models.base_model import BaseModel
    Base = object

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    if getenv("HBNB_TYPE_STORAGE") =="db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=True, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary="place_amenity", back_populates="places", overlaps="place_amenities", viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Retrieve related reviews in FileStorage"""
            from models.review import Review

            review_list = []
            from models import storage
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list
        
        @property
        def amenities(self):
            """Retrieves related amenities in FileStorage and returns a list of Amenity instances based on the amenity_ids."""

            from models.amenity import Amenity

            amenity_list = []
            from models import storage
            for amenity in storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list
        
        @amenities.setter
        def amenities(self, obj):
            """Appends an Amenity.id to the amenities_ids list."""
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)