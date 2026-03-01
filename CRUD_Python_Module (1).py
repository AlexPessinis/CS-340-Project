from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter(object):

    def __init__(self, username, password):
        USER = username
        PASS = password
        HOST = "localhost"
        PORT = 27017
        DB = "aac"
        COL = "animals"

        uri = f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource=admin"

        self.client = MongoClient(uri)
        self.database = self.client[DB]
        self.collection = self.database[COL]


    # -------------------------------------------------------------
    # CREATE
    # -------------------------------------------------------------
    def create(self, data):
        try:
            if data and isinstance(data, dict):
                result = self.collection.insert_one(data)
                return result.inserted_id is not None
            else:
                return False
        except PyMongoError:
            return False

    # -------------------------------------------------------------
    # READ
    # -------------------------------------------------------------
    def read(self, query):
        try:
            if query is None:
                query = {}

            cursor = self.collection.find(query)
            return list(cursor)
        except PyMongoError:
            return []

    # -------------------------------------------------------------
    # UPDATE
    # -------------------------------------------------------------
    def update(self, query, new_values, multiple=False):
        """
        Update document(s) in the collection.
        Returns the number of documents modified.
        """
        try:
            if multiple:
                result = self.collection.update_many(query, {"$set": new_values})
            else:
                result = self.collection.update_one(query, {"$set": new_values})
            return result.modified_count
        except PyMongoError:
            return 0

    # -------------------------------------------------------------
    # DELETE
    # -------------------------------------------------------------
    def delete(self, query, multiple=False):
        """
        Delete document(s) from the collection.
        Returns the number of documents removed.
        """
        try:
            if multiple:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        except PyMongoError:
            return 0