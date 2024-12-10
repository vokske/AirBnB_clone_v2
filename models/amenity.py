#!/usr/bin/python3
""" Amenity Module for HBNB project """

from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    
    from models.base_model import BaseModel, Base
else:
    from models.base_model import BaseModel
    Base = object

class Amenity(BaseModel, Base):
    """Amenity class represents the various amenities available in a place."""
    __tablename__ = "amenities"

    if isinstance(Base, type):
        from sqlalchemy import Column, String
        from sqlalchemy.orm import relationship
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity", viewonly=False)
        places = relationship("Place", secondary="place_amenity", back_populates="amenities", overlaps="place_amenities")
    else:
        name = ""
        
        @property
        def places(self):
            """Retrieves associated places for this amenity in FileStorage. It returns a list of Place instances."""
            
            from models import storage
            from models.place import Place

            places_list = []
            
            for place in storage.all(Place).values():
                if self.id in place.amenity_ids:
                    places_list.append(place)
            return places_list