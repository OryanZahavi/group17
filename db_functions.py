import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# חיבור ל-MongoDB Atlas
uri = "mongodb+srv://ofriap:<db_password>@cluster0.vzg9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
cluster = MongoClient(uri, server_api=ServerApi('1'))
db = cluster["Soul_Studio"]  # שם הדאטהבייס
users_col = db["Users"]  # שם הקולקשן של המשתמשות

# ------------------- פונקציות ניהול משתמשים -------------------

def user_exist(user_email,user_password):
    user = users_col.find_one({"Email": user_email})
    if user and user_password == user["Password"]:
        return True
    return False



def insert_user(email, password, first_name, last_name, birth_date, phone_number):
    """ הוספת משתמש חדש למסד הנתונים """
    user_data = {
        "name": email,
        "password": password,  # יש להצפין בעתיד!
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date,
        "phone_number": phone_number
    }
    users_col.insert_one(user_data)

# פונקציה לבדיקת קיום משתמשת במערכת
def get_user_by_email(email):
    return users_col.find_one({"email": email})

def get_all_users():
    """שליפת כל המשתמשות מהקולקשן Users"""
    users = list(users_col.find({}, {"_id": 0}))  # מוציאים את ה-_id מהתוצאה
    return users



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
