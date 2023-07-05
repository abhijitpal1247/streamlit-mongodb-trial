import pymongo
import bcrypt
from abc import ABC, abstractmethod


class DbConn:
    def __init__(self, dblink):
        self.dblink = dblink
        self.client = pymongo.MongoClient(self.dblink)
        self.database_name = None
        self.database = None

    def get_client(self):
        return self.client

    def get_database(self, database_name):
        self.database_name = database_name
        self.database = self.client[database_name]
        return self.database

    def create_database(self, database_name):
        self.database_name = database_name
        self.database = self.client[database_name]


class Model:
    def __init__(self, db_conn: DbConn, database_name: str):
        self.db_conn = db_conn
        self.database_name = database_name
        self.database = self.db_conn.get_database(self.database_name)
        self.collection_name = self.__class__.__name__
        self.collection = self.database[self.__class__.__name__]


class User(Model):
    def __init__(self, db_conn: DbConn, database_name: str):
        super().__init__(db_conn, database_name)
        if "unique email" not in self.collection.list_indexes():
            self.collection.create_index("email", name="unique email", unique=True)

    def add_user(self, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.collection.insert_one({"email": email, "password": hashed_password})

    def delete_user(self, email):
        self.collection.delete_one({"email": email})

    def get_user(self, email):
        return self.collection.find({"email": email})

    def update_user(self, email: str, new_email: str = None, new_password: str = None):
        if new_email is not None:
            self.collection.update_one({"email": email}, {"$set": {"email": new_email}})
        if new_password is not None:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self.collection.update_one({"email": email}, {"$set": {"password": hashed_password}})


class Dataset(Model):
    def __init__(self, db_conn: DbConn, database_name: str):
        super().__init__(db_conn, database_name)

    def add_image_to_dataset(self, image, dataset_name, user_email):
        self.collection.insert_one({"image": image, "dataset_name": dataset_name, "user_email": user_email})

    def delete_dataset(self, dataset_name):
        self.collection.delete_many({"dataset_name": dataset_name})

    def get_dataset(self, dataset_name, email, count):
        return self.collection.find({"dataset_name": dataset_name, "user_email": email}).limit(count)

    def get_datasets_per_email(self, email):
        return self.collection.find({"user_email": email}).distinct('dataset_name')

    def update_dataset(self, dataset_name: str, new_dataset_name: str = None):
        self.collection.update_many({"dataset_name": dataset_name}, {"$set": {"dataset_name": new_dataset_name}})
