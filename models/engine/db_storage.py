#!/usr/bin/python3

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from models.base_model import Base, BaseModel
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):

        db_url = f'mysql+mysqldb://{getenv("HBNB_MYSQL_USER")}:{getenv("HBNB_MYSQL_PWD")}@{getenv("HBNB_MYSQL_HOST", "localhost")}/{getenv("HBNB_MYSQL_DB")}'
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        # Drop all tables if the environment variable is equal to 'test'
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)
    
    def classes(self):
        """Return a dictionary of classes and their references."""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        class_dict = {"User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review
                }
        return class_dict
    
    def all(self, cls=None):
        """ Public instance method with an optional argument `cls` which is the class name.
        Method queries on the current db session(self.__session) and returns all objects depending on the argument.
        If `cls` is `None`, objects of all the classes are queried and returned in a dictionary.
        """
        objects = {}
        class_dict = self.classes()
        if cls:
            if isinstance(cls, str):
                cls = class_dict.get(cls)
            if cls is None or not issubclass(cls, Base):
                raise ValueError(f"Class '{cls}' is not valid.")
            obj_list = self.__session.query(cls).all()
            for obj in obj_list:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        else:
            for cls in class_dict.values():
                obj_list = self.__session.query(cls).all()
                for obj in obj_list:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add an object to the current database session"""
        
        if obj:
            updated_obj = self.__session.merge(obj)
            self.__session.add(updated_obj)

    def save(self):
        """Commit changes of the current database session."""
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            self.__session.rollback() # Roll back the transaction in case of error
            print(f"Error: {e}")

    def delete(self, obj=None):
        """Deletes from the current database session an object if argument is not None."""
        if obj and isinstance(obj, Base):
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        # Create all tables
        Base.metadata.create_all(self.__engine)
        current_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # Create a scoped session
        Session = scoped_session(current_session)
        self.__session = Session()