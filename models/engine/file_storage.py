#!/usr/bin/python3
"""Module contains class FileStorage."""
import os
import json


class FileStorage:
    """Serializes instances to a JSON file
    and deserializes JSON file to instances.

    Private class attributes:
        - __file_path
        - __objects

    Public instance methods
        - all
        - new
        - save
        - reload
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the __objects dictionary if no parameter is passed.
        Otherwise, it returns a list of objects of the class passed as an
        argument.
        """
        if cls is None:
            return self.__objects
        if isinstance(cls, str):
            cls = self.classes().get(cls)
        if cls is None:
            return{}
        return {key: value for key, value in self.__objects.items()
                if isinstance(value, cls)}

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes objects to a JSON file."""
        json_dict = {}
        for key, obj in self.__objects.items():
            obj_dict = obj.to_dict()
            obj_dict.pop('_sa_instance_state', None)
            json_dict[key] = obj_dict

        directory = os.path.dirname(self.__file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.__file_path, 'w') as f:
            json.dump(json_dict, f)

    def classes(self):
        """Return a dictionary mapping class names to their class objects. It serves to reconstruct objects during reload."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        class_dict = {"BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review
                }
        return class_dict

    def reload(self):
        """Deserializes the JSON file to __objects if the file exists."""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as f:
                json_dict = json.load(f)

                valid_classes = self.classes()
                for key, value in json_dict.items():
                    class_name, obj_id = key.split('.')
                    obj_class = valid_classes.get(class_name)
                    if obj_class:
                        self.__objects[key] = obj_class(**value)

    def delete(self, obj=None):
        """Deletes `obj` from `__objects` if it exists."""
        if obj == None:
            return
        key = f"{obj.__class__.__name__}.{obj.id}"
        if key in self.__objects.keys():
            del self.__objects[key]
            self.save()
