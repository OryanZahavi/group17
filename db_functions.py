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

# --------------------------------- פונקציות לניהול שיעורים --------------------------
from bson.objectid import ObjectId
# חיבור למסד הנתונים

registrations_col = Soul_Studio["registrations"]
classes_collection = Soul_Studio["classes"]

# פונקציה להוספת שיעורים (אם לא קיימים)
def add_classes_if_not_exist():
    classes = [
        {"day": "Sunday", "time": "07:00", "title": "יוגה אשטנגה - מתחילות", "capacity": 10, "registered_users": [], "waitlist_users": []},
        {"day": "Sunday", "time": "08:00", "title": "יוגה ויניאסה - מתחילות", "capacity": 10, "registered_users": [], "waitlist_users": []},
        {"day": "Sunday", "time": "18:00", "title": "יוגה אשטנגה - מתקדמות", "capacity": 10, "registered_users": [], "waitlist_users": []},
        {"day": "Sunday", "time": "19:00", "title": "Power yoga", "capacity": 10, "registered_users": [], "waitlist_users": []},
        {"day": "Sunday", "time": "20:00", "title": "יוגה ויניאסה - כל הרמות", "capacity": 10, "registered_users": [], "waitlist_users": []}
    ]
    for cls in classes:
        if not classes_collection.find_one({"day": cls["day"], "time": cls["time"]}):
            classes_collection.insert_one(cls)

# פונקציה לקבלת שיעורי יום מסוים
def get_classes_by_day(day):
    return list(classes_collection.find({"day": day}))

# פונקציה לרישום משתמש לשיעור
def register_user_to_class(class_id, user_email):
    cls = classes_collection.find_one({"_id": ObjectId(class_id)})
    if not cls:
        return "not_found"

    # בדיקה אם המשתמש כבר רשום
    if user_email in cls["registered_users"]:
        return "already_registered"

    # בדיקה אם יש מקום פנוי
    if len(cls["registered_users"]) < cls["capacity"]:
        classes_collection.update_one(
            {"_id": ObjectId(class_id)},
            {"$push": {"registered_users": user_email}}
        )
        return "success"
    else:
        return "full"


# פונקציה לרישום לרשימת המתנה
def add_to_waitlist(class_id, user_email):
    cls = classes_collection.find_one({"_id": ObjectId(class_id)})
    if cls:
        classes_collection.update_one({"_id": ObjectId(class_id)}, {"$push": {"waitlist_users": user_email}})
        return "success"
    return "not_found"

# פונקציה לביטול הרשמה
def cancel_registration(class_id, user_email):
    cls = classes_collection.find_one({"_id": ObjectId(class_id)})
    if cls:
        if user_email in cls["registered_users"]:
            classes_collection.update_one({"_id": ObjectId(class_id)}, {"$pull": {"registered_users": user_email}})
            return "success"
        elif user_email in cls["waitlist_users"]:
            classes_collection.update_one({"_id": ObjectId(class_id)}, {"$pull": {"waitlist_users": user_email}})
            return "success"
    return "not_found"

# פונקציה להבאת סטטוס שיעור (כמה מקומות נשארו)
def get_class_status(class_id):
    cls = classes_collection.find_one({"_id": ObjectId(class_id)})

    print(f"📌 מסמך מה-DB: {cls}")  # הדפסה כדי לוודא שקיבלנו נתונים

    if not cls:
        print("❌ השיעור לא נמצא!")
        return None  # מחזירה None אם השיעור לא נמצא

    # מבטיחים שהשדות תמיד יהיו קיימים
    registered_users = cls.get("registered_users", [])  # אם חסר - מחזירים רשימה ריקה
    capacity = cls.get("capacity", 10)  # אם חסר - ברירת מחדל של 10 מקומות

    print(f"✅ רשומים: {registered_users}, קיבולת: {capacity}")  # לוודא שהתוכן תקין

    spots_left = capacity - len(registered_users)
    return {
        "classId": class_id,
        "spotsLeft": spots_left,
        "spotsFilled": len(registered_users),  # מספר הנרשמים בפועל
        "capacity": capacity
    }













#
# def get_classes_by_day(day):
#     """
#     שליפת כל השיעורים של יום מסוים, כולל כמה אנשים רשומים בכל שיעור.
#     """
#     classes = list(classes_col.find({"day": day}))
#
#     for class_obj in classes:
#         class_id = class_obj["_id"]
#         registered_count = registrations_col.count_documents({"class_id": str(class_id), "status": "registered"})
#         class_obj["registered"] = registered_count  # נוסיף את כמות הנרשמות
#     return classes
#
#
# def register_user_to_class(class_id, user_email):
#     """
#     רישום משתמש לשיעור (אם יש מקום פנוי)
#     """
#     class_data = classes_col.find_one({"_id": ObjectId(class_id)})
#
#     if not class_data:
#         return {"status": "error", "message": "השיעור לא נמצא."}
#
#     registered_count = registrations_col.count_documents({"class_id": class_id, "status": "registered"})
#
#     if registered_count < class_data["capacity"]:
#         registrations_col.insert_one({"class_id": class_id, "user_email": user_email, "status": "registered"})
#         return {"status": "success", "message": "נרשמת בהצלחה לשיעור!"}
#     else:
#         registrations_col.insert_one({"class_id": class_id, "user_email": user_email, "status": "waitlist"})
#         return {"status": "waitlist", "message": "השיעור מלא, נוספת לרשימת ההמתנה."}
#
#
# def reset_weekly_registrations():
#     """
#     איפוס כל ההרשמות בתחילת שבוע חדש
#     """
#     registrations_col.delete_many({})  # מוחק את כל הנתונים מהקולקשן


#
# # מביא את כל השיעורים של יום ראשון
# def get_sunday_classes():
#     return list(classes_col.find({"day": "Sunday"}))
#
#
# # רישום משתמש לשיעור
# def register_to_class(class_id, user_email):
#     class_info = classes_col.find_one({"_id": class_id})
#
#     if not class_info:
#         return False, "השיעור לא נמצא"
#
#     if class_info["registered"] >= class_info["capacity"]:
#         return False, "השיעור מלא, ניתן להצטרף לרשימת המתנה"
#
#     classes_col.update_one({"_id": class_id}, {"$inc": {"registered": 1}, "$push": {"participants": user_email}})
#     return True, "נרשמת בהצלחה!"
#
#
# # ביטול הרשמה מהשיעור
# def cancel_registration(class_id, user_email):
#     class_info = classes_col.find_one({"_id": class_id})
#
#     if not class_info or user_email not in class_info["participants"]:
#         return False, "לא נמצאת רשומה לשיעור"
#
#     classes_col.update_one({"_id": class_id}, {"$inc": {"registered": -1}, "$pull": {"participants": user_email}})
#     return True, "הרשמתך בוטלה"
#
#
# # הצטרפות לרשימת המתנה
# def join_waitlist(class_id, user_email):
#     existing_waitlist = waitlist_col.find_one({"class_id": class_id, "email": user_email})
#
#     if existing_waitlist:
#         return False, "כבר נמצאת ברשימת ההמתנה"
#
#     waitlist_col.insert_one({"class_id": class_id, "email": user_email})
#     return True, "נוספת לרשימת ההמתנה"
#

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