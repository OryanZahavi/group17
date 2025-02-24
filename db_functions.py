import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# חיבור ל-MongoDB Atlas
uri = "mongodb+srv://ofriap:<db_password>@cluster0.vzg9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
cluster = MongoClient(uri, server_api=ServerApi('1'))
db = cluster["Soul_Studio"]  # שם הדאטהבייס
users_col = db["Users"]  # שם הקולקשן של המשתמשות

# ------------------- פונקציות ניהול משתמשים -------------------

# פונקציה לבדיקת קיום משתמשת במערכת
def get_user_by_email(email):
    return users_col.find_one({"email": email})






# import pymongo
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
#
# uri= "mongodb+srv://ofriap:<db_password>@cluster0.vzg9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#
# cluster = MongoClient(uri, server_api=ServerApi('1'))
# mydatabase = cluster['mydatabase']
# customers_col = mydatabase['customers']
# product_col = mydatabase['products']
