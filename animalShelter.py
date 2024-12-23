#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MOngoDB """
    
    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'SNHU1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 33363
        DB = 'aac'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]
        
# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            # validating that the data is a dictionary
            insert = self.collection.insert_one(data)  # data should be dictionary
            if insert is not None:
                return True
            else:
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            

# Create method to implement the R in CRUD.
    def read(self, searchData):
        if searchData:
            data = self.collection.find(searchData, {"_id": False})
        else:
            data = self.collection.find({}, {"_id": False})
        return data
    
# Create method to implement the U in CRUD
    def update(self, searchData, updateData):
        if searchData is not None:
            result = self.collection.update_many(searchData, {"$set": updateData})
        else:
            return "{}"
        return result.raw_result
    
# Create method to implement the D in CRUD
    def delete(self, deleteData):
        if deleteData is not None:
            result = self.collection.delete_many(deleteData)
        else:
            return "{}"
        return result.raw_result


# In[3]:


shelter = AnimalShelter("aacuser", "SNHU1234")

data = {"animal_type": "Dog", "name" : "Lucy", "age": 2, "breed" : "Labrador"}
print(shelter.create(data))

query = {"name" : "Lucy"}
print (shelter.read(query))

update_query = {"name" : "Lucy"}
new_data = {"age" : 3}
print(shelter.update(update_query, new_data))

delete_query = {"name" : "Lucy"}
print(shelter.delete(delete_query))


# In[ ]:




