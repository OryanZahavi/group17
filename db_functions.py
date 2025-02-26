
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ofriap:Oa2712!@cluster0.vzg9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

Soul_Studio = client['Soul_Studio']  # שם הדאטהבייס
users_col = Soul_Studio['users']  # שם הקולקשן של המשתמשות
lessons_col = Soul_Studio['lessons']


# # ------------------- פונקציות ניהול משתמשים -------------------

#
# print("Hello, world!")
# def insert():
#     user1 = {
#         'name': 'shelly',
#         'lastname': 'bar',
#         'age': 27
#     }
#     result = users_col.insert_one(user1)  # הכנסת הנתונים
#     print(f"Inserted document ID: {result.inserted_id}")  # מדפיס את ה-ID של המסמך שנוסף
#     return result.inserted_id
#
#



def user_exist(user_email, user_password):
    user = users_col.find_one({"Email": user_email})
    if user and user_password == user["Password"]:
        return True
    return False

def insert_user(first_name,last_name, birth_date, email, phone,password,health_file):
    """ הוספת משתמש חדש למסד הנתונים """
    users_col.insert_one({

        'first_name': first_name,
        'last_name': last_name,
        'birth_date': birth_date,
        'email': email,
        'phone': phone,
        'password': password,
        'health_file': health_file

    })


# פונקציה לבדיקת קיום משתמשת במערכת
def get_user_by_email(email):
    return users_col.find_one({"email": email})

def get_all_users():
    """שליפת כל המשתמשות מהקולקשן Users"""
    users = list(users_col.find({}, {"_id": 0}))  # מוציאים את ה-_id מהתוצאה
    return users


def email_exists(email):
    if users_col.find_one({"email": email}):
        return True
    return False