#!/usr/bin/env python
# coding: utf-8

# In[3]:


from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MOngoDB """
    
    def __init__(self):
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
            self.database.animals.insert_one(data)  # data should be dictionary
            # self.collection.insert_one(data)
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            # self.database.animals.find({})
            # return list()

# Create method to implement the R in CRUD.


# In[6]:


crud = AnimalShelter()


# In[7]:


Monkey = { "animal_id": "A999901", "animal_type": "Emperor tamarin", "breed": "tamarin", "color": "brown" }


# In[8]:


print(Monkey)


# In[10]:


crud.create(Monkey)


# In[ ]:




