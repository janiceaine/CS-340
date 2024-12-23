#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """
    
    def __init__(self):
        # Initializing the MongoClient to access MongoDB
        USER = 'aacuser'
        PASS = 'SNHU1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 33363
        DB = 'aac'
        COL = 'animals'

        # Initializing the Connection
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
        self.database = self.client[DB]
        self.collection = self.database[COL]
        
    # Creating method to insert a document into MongoDB
    def create(self, data):
        """ Inserts a new document into the collection. """
        if data:
            try:
                self.collection.insert_one(data)
                print("Document inserted successfully!")
                return True
            except Exception as e:
                print(f"Error inserting document: {e}")
                return False
        else:
            raise Exception("Nothing to save, data parameter is empty")

    # Read method to query documents from MongoDB
    def read(self, query):
        """ Queries the collection based on the input query. """
        try:
            documents = self.collection.find(query)  # Use find() for multiple documents
            result = list(documents)  # Convert the cursor to a list
            return result
        except Exception as e:
            print(f"Error querying documents: {e}")
            return []

# Create an instance of the AnimalShelter class
animal_shelter = AnimalShelter()

# Create a new document (animal record) to insert
new_animal = {
    "animal_id": "A999902",
    "name": "Billy",
    "species": "Goat",
    "age": 2,
    "outcome_type": "Adoption",
    "date_outcome": "2024-11-24"
}

# Testing the Create functionality by inserting the new animal record
insert_result = animal_shelter.create(new_animal)
if insert_result:
    print("Document inserted successfully!")
else:
    print("Failed to insert document.")

# Testing the Read functionality by querying for all animals of species 'Dog'
query = {"species": "Goat"}
animals = animal_shelter.read(query)

# Display the results of the query
if animals:
    print("Found animals:")
    for animal in animals:
        print(animal)
else:
    print("No animals found.")


# In[ ]:




