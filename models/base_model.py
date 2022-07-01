#!/usr/bin/python3
import uuid
from datetime import datetime
import models


class BaseModel():

    """ main class, it creates id, time the procces was created and  """
    def __init__(self, *args, **kwargs):
        if len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.update_at = datetime.now()

        else:
            form = "%Y-%m-%dT%H:%M:%S.%f"
            del kwargs['__class__']
            kwargs['created_at'] = datetime.strptime(kwargs["created_at"], form)
            kwargs['update_at'] = datetime.strptime(kwargs["update_at"], form)
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        name = self.__class__.__name__
        return f'BaseModel({name} ({self.id}) {self.__dict__})'

    def save(self):
        """ 
            updates the public instance attribute update_at with
            the current datetime 
        """
        self.update_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ returns a dictironaty containing all keys/values of __dict__"""
        n_dict = self.__dict__.copy()
        n_dict["created_at"] = self.created_at.isoformat()
        n_dict["update_at"] = self.update_at.isoformat()
        n_dict["__class__"] = self.__class__.__name__
        return n_dict
