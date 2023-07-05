import os
import bcrypt
import streamlit as st
from models import User, DbConn, Dataset

db_conn = DbConn('mongodb://' + os.environ['MONGO_DB_USERNAME'] + ':' + os.environ['MONGO_DB_PASSWORD'] + '@' + os.environ['MONGO_DB_HOSTNAME'] + ':27017/')
database_name = "my_database"
db_conn.create_database(database_name)
user = User(db_conn=db_conn, database_name=database_name)
dataset = Dataset(db_conn=db_conn, database_name=database_name)


def check_password(email, password):
    hashed_password = None
    for i in user.get_user(email):
        hashed_password = i['password']
    if hashed_password is not None:
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            st.session_state['logged_in'] = True
        else:
            st.session_state["logged_in"] = False
    else:
        st.session_state["logged_in"] = False


def email_exists(email):
    for i in user.get_user(email):
        if i['email'] == email:
            return True
    return False


def create_account(email, password):
    user.add_user(email=email, password=password)


def save_image(image, dataset_name, email):
    dataset.add_image_to_dataset(image, dataset_name, email)


def query_datasets(email):
    return dataset.get_datasets_per_email(email)


def get_preview_images(dataset_name, email, count):
    image_list = []
    for i in dataset.get_dataset(dataset_name, email, count):
        image_list.append(i['image'])
    return image_list
