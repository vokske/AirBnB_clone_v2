#!/usr/bin/python3
"""Module contains class BaseModel."""
import uuid
from datetime import datetime
from os import getenv
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

if getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    """Defines all common attributes/methods for other classes.

    Class attributes:
        - id: represents a column containing a unique string (60 chars), can't be Null and is a primary key
        - created_at: represents a column containing a datetime, can't be null.
        - updated_at: represents a column containing a datetime and can't be null.

    Public instance attributes:
        - id
        - created_at
        - updated_at

    Public instance methods:
        - save: updates 'updated_at'
        - to_dict
    """
    if isinstance(Base, type):
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.now(), nullable=False)
        updated_at = Column(DateTime, default=datetime.now(), nullable=False)


    def __init__(self, *args, **kwargs):
        """Constructor for class BaseModel."""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                elif key != '__class__':
                    setattr(self, key, value)
            
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Returns a human-readable string representation of an instance."""
        dict_copy = self.__dict__.copy()
        dict_copy['created_at'] = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        dict_copy['updated_at'] = self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        return f"[{self.__class__.__name__}] ({self.id}) {dict_copy}"

    def save(self):
        """updates the public instance attribute
        updated_at with the current datetime."""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values
        of __dict__ of an instance."""
        instance_dict = self.__dict__.copy()
        instance_dict['__class__'] = self.__class__.__name__
        instance_dict['created_at'] = self.created_at.isoformat()
        instance_dict['updated_at'] = self.updated_at.isoformat()
        instance_dict.pop('_sa_instance_state', None)
        return instance_dict
    
    def delete(self):
        """Deletes the current instance from storage."""
        from models import storage
        storage.delete(self)
