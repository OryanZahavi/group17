import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from werkzeug.utils import secure_filename


uri = "mongodb+srv://ofriap:Oa2712!@cluster0.vzg9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# יצירת חיבור למונגו
client = MongoClient(uri, server_api=ServerApi('1'))

# חיבור לדאטהבייס ולקולקשן
Soul_Studio = client['Soul_Studio']  # שם הדאטהבייס
users_col = Soul_Studio['users']  # שם הקולקשן של המשתמשים

# פונקציה להכנסת כמה משתמשים
def insert_users_test():
    users = [
        {'name': 'shelly', 'lastname': 'bar', 'age': 27},
        {'name': 'david', 'lastname': 'cohen', 'age': 30},
        {'name': 'lea', 'lastname': 'levi', 'age': 25}
    ]
    result = users_col.insert_many(users)  # הכנסת הנתונים
    print(f"Inserted IDs: {result.inserted_ids}")  # הדפסת ה-IDs שנוספו

# קריאה לפונקציה כדי להכניס את הנתונים
if __name__ == "__main__":
    insert_users_test()
# ---- יצירת תיקייה לשמירת קבצים ----
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---- פונקציות לניהול משתמשים ----

def user_exists(email):
    """בודק האם המשתמש כבר קיים במערכת לפי כתובת הדוא"ל"""
    return users_col.find_one({"email": email}) is not None


def authenticate_user(user_email, user_password):
    """בודק אם המשתמש קיים במסד הנתונים עם הסיסמה הנכונה (לצורך התחברות)"""
    user = users_col.find_one({"email": user_email})
    if user and user_password == user["password"]:
        return user  # מחזיר את המשתמש אם הפרטים תקינים
    return None

def insert_user(first_name, last_name, birth_date, email, phone_number, password, health_file):
    """מוסיף משתמש חדש למסד הנתונים"""
    if user_exists(email):
        return None  # המשתמש כבר קיים

    # טיפול בשמירת הקובץ
    health_file_path = None
    if health_file:
        filename = secure_filename(health_file.filename)  # מאבטח את שם הקובץ
        health_file_path = os.path.join(UPLOAD_FOLDER, filename)  # יצירת נתיב שמירה
        health_file.save(health_file_path)  # שמירת הקובץ בשרת
    # יצירת מסמך משתמש חדש
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date,
        "email": email,
        "phone_number": phone_number,
        "password": password,  # ⚠️ בעתיד עדיף להצפין את הסיסמה!
        "health_file": health_file_path  # שמירת הנתיב במקום האובייקט
    }

    result = users_col.insert_one(user_data)
    return str(result.inserted_id)  # מחזיר את ה-ID של המשתמש החדש



################################################################################
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