from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'something secret' #TODO make this secret
DB_NAME = 'noteworthington'

DATABASE = MongoClient()[DB_NAME]
USERS_COLLECTION = DATABASE.users
NOTES_COLLECTION = DATABASE.notes

DEBUG = False
