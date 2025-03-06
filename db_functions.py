import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, timezone
from bson.objectid import ObjectId
import schedule
import time


uri = "mongodb+srv://ofriap:Oa2712!@cluster0.vzg9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# יצירת חיבור למונגו
client = MongoClient(uri, server_api=ServerApi('1'))

# חיבור לדאטהבייס ולקולקשן
Soul_Studio = client['Soul_Studio']  # שם הדאטהבייס
users_col = Soul_Studio['users']  # קולקשן של המשתמשים
classes_collection = Soul_Studio["classes"]  # קולקשן של השיעורים


# פונקציה להכנסת כמה משתמשים
def insert_users_test():
    users = [
        {
            "first_name": "shelly",
            "last_name": "bar",
            "birth_date": "1997-03-15",
            "email": "shelly.bar@email.com",
            "phone_number": "0541234567",
            "password": "password123",
            "health_file": None
        },
        {
            "first_name": "david",
            "last_name": "cohen",
            "birth_date": "1995-08-10",
            "email": "david.cohen@email.com",
            "phone_number": "0523456789",
            "password": "securePass!",
            "health_file": None
        },
        {
            "first_name": "lea",
            "last_name": "levi",
            "birth_date": "1998-11-25",
            "email": "lea.levi@email.com",
            "phone_number": "0509876543",
            "password": "LeaPass123",
            "health_file": None
        },
        {
            "first_name": "ofri",
            "last_name": "applebaum",
            "birth_date": "1995-06-06",
            "email": "ofriapple2712@gmail.com",
            "phone_number": "0523457487",
            "password": "Rsdf123!",
            "health_file": "static/uploads/2.pdf"
        }
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


def insert_classes():
    classes = [
        {"day": "Sunday", "title": "יוגה אשטנגה - מתחילות", "capacity": 10, "date": datetime(2025, 3, 2, 7, 0)},
        {"day": "Sunday", "title": "יוגה ויניאסה - מתחילות", "capacity": 10, "date": datetime(2025, 3, 2, 8, 0)},
        {"day": "Sunday", "title": "יוגה אשטנגה - מתקדמות", "capacity": 10, "date": datetime(2025, 3, 2, 18, 0)},
        {"day": "Sunday", "title": "Power yoga", "capacity": 10, "date": datetime(2025, 3, 2, 19, 0)},
        {"day": "Sunday", "title": "יוגה ויניאסה - כל הרמות", "capacity": 10, "date": datetime(2025, 3, 2, 20, 0)},

        {"day": "Monday", "title": "Power yoga", "capacity": 10, "date": datetime(2025, 3, 3, 7, 0)},
        {"day": "Monday", "title": "יוגה קונדליני", "capacity": 10, "date": datetime(2025, 3, 3, 8, 0)},
        {"day": "Monday", "title": "יוגה ויניאסה - כל הרמות", "capacity": 10, "date": datetime(2025, 3, 3, 18, 0)},
        {"day": "Monday", "title": "Power yoga", "capacity": 10, "date": datetime(2025, 3, 3, 19, 0)},
        {"day": "Monday", "title": "שיעור מתיחות", "capacity": 10, "date": datetime(2025, 3, 3, 20, 0)},

        {"day": "Tuesday", "title": "שיעור נשימות", "capacity": 10, "date": datetime(2025, 3, 4, 7, 0)},
        {"day": "Tuesday", "title": "יוגה קונדליני", "capacity": 10, "date": datetime(2025, 3, 4, 8, 0)},
        {"day": "Tuesday", "title": "Power yoga", "capacity": 10, "date": datetime(2025, 3, 4, 10, 0)},
        {"day": "Tuesday", "title": "יוגה אשטנגה - מתחילות", "capacity": 10, "date": datetime(2025, 3, 4, 18, 0)},
        {"day": "Tuesday", "title": "יוגה אשטנגה - מתקדמות", "capacity": 10, "date": datetime(2025, 3, 4, 19, 0)},

        {"day": "Wednesday", "title": "Power yoga", "capacity": 10, "date": datetime(2025, 3, 5, 7, 0)},
        {"day": "Wednesday", "title": "יוגה ויניאסה - מתקדמות", "capacity": 10, "date": datetime(2025, 3, 5, 8, 0)},
        {"day": "Wednesday", "title": "יוגה אשטנגה - מתחילות", "capacity": 10, "date": datetime(2025, 3, 5, 9, 0)},
        {"day": "Wednesday", "title": "שיעור מתיחות", "capacity": 10, "date": datetime(2025, 3, 5, 19, 0)},
        {"day": "Wednesday", "title": "יוגה קונדליני", "capacity": 10, "date": datetime(2025, 3, 5, 20, 0)},

        {"day": "Thursday", "title": "שיעור נשימות", "capacity": 10, "date": datetime(2025, 3, 6, 7, 0)},
        {"day": "Thursday", "title": "יוגה אשטנגה - מתחילות", "capacity": 10, "date": datetime(2025, 3, 6, 8, 0)},
        {"day": "Thursday", "title": "יוגה קונדליני", "capacity": 10, "date": datetime(2025, 3, 6, 9, 0)},
        {"day": "Thursday", "title": "יוגה ויניאסה - כל הרמות", "capacity": 10, "date": datetime(2025, 3, 6, 17, 0)},
        {"day": "Thursday", "title": "Power yoga", "capacity": 10, "date": datetime(2025, 3, 6, 18, 0)}
    ]

    for cls in classes:
        existing_class = classes_collection.find_one({"day": cls["day"], "date": cls["date"]})
        if not existing_class:
            cls["registered_users"] = []
            cls["waitlist_users"] = []
            classes_collection.insert_one(cls)

    print("✅ השיעורים נוספו בהצלחה עם תאריך ושעה מדויקים!")



# קריאה לפונקציה להוספת השיעורים
insert_classes()
# classes_collection.delete_many({})
# print("🗑️ כל המסמכים בקולקשן נמחקו!")



def update_sunday_classes():
    """ מעדכן את התאריך של שיעורי יום ראשון בשבוע קדימה ומרוקן רשימות """
    classes = classes_collection.find({"day": "Sunday"})  # שולפים את כל השיעורים של יום ראשון

    for cls in classes:
        new_date = cls["date"] + timedelta(days=7)  # מוסיפים שבוע
        classes_collection.update_one(
            {"_id": cls["_id"]},  # מזהה השיעור
            {"$set": {
                "date": new_date,  # עדכון התאריך
                "registered_users": [],  # ריקון רשימת המשתמשים הרשומים
                "waitlist_users": []  # ריקון רשימת ההמתנה
            }}
        )

    print("🎯 שיעורי יום ראשון עודכנו!")


def update_monday_classes():
    """ מעדכן את התאריך של שיעורי יום שני בשבוע קדימה ומרוקן רשימות """
    classes = classes_collection.find({"day": "Monday"})

    for cls in classes:
        new_date = cls["date"] + timedelta(days=7)
        classes_collection.update_one(
            {"_id": cls["_id"]},
            {"$set": {"date": new_date, "registered_users": [], "waitlist_users": []}}
        )
    print("🎯 שיעורי יום שני עודכנו!")


def update_tuesday_classes():
    """ מעדכן את התאריך של שיעורי יום שלישי בשבוע קדימה ומרוקן רשימות """
    classes = classes_collection.find({"day": "Tuesday"})

    for cls in classes:
        new_date = cls["date"] + timedelta(days=7)
        classes_collection.update_one(
            {"_id": cls["_id"]},
            {"$set": {"date": new_date, "registered_users": [], "waitlist_users": []}}
        )
    print("🎯 שיעורי יום שלישי עודכנו!")


def update_wednesday_classes():
    """ מעדכן את התאריך של שיעורי יום רביעי בשבוע קדימה ומרוקן רשימות """
    classes = classes_collection.find({"day": "Wednesday"})

    for cls in classes:
        new_date = cls["date"] + timedelta(days=7)
        classes_collection.update_one(
            {"_id": cls["_id"]},
            {"$set": {"date": new_date, "registered_users": [], "waitlist_users": []}}
        )
    print("🎯 שיעורי יום רביעי עודכנו!")


def update_thursday_classes():
    """ מעדכן את התאריך של שיעורי יום חמישי בשבוע קדימה ומרוקן רשימות """
    classes = classes_collection.find({"day": "Thursday"})

    for cls in classes:
        new_date = cls["date"] + timedelta(days=7)
        classes_collection.update_one(
            {"_id": cls["_id"]},
            {"$set": {"date": new_date, "registered_users": [], "waitlist_users": []}}
        )
    print("🎯 שיעורי יום חמישי עודכנו!")


from datetime import datetime, timedelta
from bson.objectid import ObjectId

def time_until_class(class_id):
    """
    מקבלת ID של שיעור, שולפת את תאריך השיעור מה-DB,
    ובודקת כמה זמן נשאר עד אליו.
    מחזירה False אם השיעור כבר עבר, אחרת מחזירה את הזמן שנותר בפורמט קריא.
    """
    cls = classes_collection.find_one({"_id": ObjectId(class_id)})  # שליפת שיעור לפי ID

    if not cls:
        print(f"❌ שגיאה: שיעור עם ID {class_id} לא נמצא!")
        return None  # אם השיעור לא קיים, מחזירים None

    class_date = cls.get("date")  # שליפת תאריך השיעור
    if not class_date:
        print(f"⚠️ שגיאה: לשיעור {class_id} אין שדה 'date'!")
        return None

    now = datetime.now()  # הזמן הנוכחי
    time_difference = class_date - now  # מחשבים את ההפרש המלא

    if time_difference.total_seconds() <= 0:
        return False  # השיעור כבר עבר

    # חישוב ימים, שעות, דקות ושניות
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        "timeLeft": f"נותרו {days} ימים, {hours} שעות, {minutes} דקות, {seconds} שניות",
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

# דוגמה לשימוש:
# class_id = "67c96a489c9c494eda9bd5f7"  # דוגמה ל-ID של שיעור
# result = time_until_class(class_id)
#
# if result:
#     print(f"⏳ זמן שנותר לשיעור: {result['timeLeft']}")
# else:
#     print("❌ השיעור כבר עבר!")
#
#










def get_class_status(class_id):
    cls = classes_collection.find_one({"_id": ObjectId(class_id)})

    if not cls:
        return None  # השיעור לא נמצא

    registered_users = cls.get("registered_users", [])
    capacity = cls.get("capacity", 10)
    class_date = cls.get("date")  # תאריך השיעור מהדאטהבייס

    # **אם `class_date` ריק, נציג הודעת שגיאה**
    if not class_date:
        print("❌ שגיאה: השדה `date` לא נמצא במסד הנתונים!")
        return {
            "classId": class_id,
            "status": "error",
            "message": "⏳ נתוני השיעור חסרים!",
            "datetime": None
        }

    # 📌 הדפסת זמן למטרות דיבאגינג
    now = datetime.now()  # משתמשים בזמן המקומי של המחשב
    time_difference = class_date - now  # מחשבים הפרש מלא

    # חישוב ימים, שעות, דקות ושניות
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # 📌 הדפסת נתונים לזיהוי בעיות
    print(f"📅 תאריך שיעור: {class_date}")
    print(f"⏳ עכשיו: {now}")
    print(f"📏 הפרש זמן: {days} ימים, {hours} שעות, {minutes} דקות, {seconds} שניות")

    # אם השיעור כבר עבר
    if time_difference.total_seconds() <= 0:
        return {
            "classId": class_id,
            "status": "expired",
            "message": "⏳ זמן הביטול עבר!",
            "datetime": class_date.isoformat(),
            "timeLeft": f"עבר לפני {-days} ימים, {-hours} שעות, {-minutes} דקות, {-seconds} שניות"
        }

    return {
        "classId": class_id,
        "spotsLeft": capacity - len(registered_users),
        "spotsFilled": len(registered_users),
        "capacity": capacity,
        "datetime": class_date.isoformat(),
        "status": "available",
        "timeLeft": f"נותרו {days} ימים, {hours} שעות, {minutes} דקות, {seconds} שניות"
    }



###############################################################
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


# פונקציה להבאת סטטוס שיעור (כמה מקומות נשארו) עובד !!!!!!!!!!!



# def get_class_status(class_id):
#     cls = classes_collection.find_one({"_id": ObjectId(class_id)})
#
#     if not cls:
#         return None  # השיעור לא נמצא
#
#     registered_users = cls.get("registered_users", [])
#     capacity = cls.get("capacity", 10)
#     date = cls.get("date")  # מושכים את תאריך השיעור
#
#     return {
#         "classId": class_id,
#         "spotsLeft": capacity - len(registered_users),
#         "spotsFilled": len(registered_users),
#         "capacity": capacity,
#         "date": date  # מחזירים גם את תאריך השיעור
#     }


def can_cancel_class(class_id, user_email):
    from datetime import datetime, timedelta
    from bson.objectid import ObjectId

    def can_cancel_class(class_id, user_email):
        """
        בודקת האם אפשר לבטל שיעור מסוים על פי הזמן שנותר עד לשיעור.
        """
        cls = classes_collection.find_one({"_id": ObjectId(class_id)})

        if not cls:
            return {"status": "error", "message": "השיעור לא נמצא."}

        class_time = datetime.fromisoformat(cls["date"])  # תאריך ושעה של השיעור מה-DB
        now = datetime.now()

        time_difference = (class_time - now).total_seconds() / 3600  # פער בשעות

        if time_difference <= 0:
            return {"status": "too_late", "message": "לא ניתן לבטל - זמן השיעור כבר עבר."}

        if time_difference < 7:
            return {"status": "late_cancel", "message": "ביטול כרוך בתשלום, מאחר והזמן הנותר קטן מ-7 שעות."}

        return {"status": "allowed", "message": "ביטול אפשרי ללא תשלום."}

# ------------

################################################################################


# import pymongo
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# import os
# from werkzeug.utils import secure_filename
#
#
# uri = "mongodb+srv://ofriap:Oa2712!@cluster0.vzg9o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#
# # יצירת חיבור למונגו
# client = MongoClient(uri, server_api=ServerApi('1'))
#
# # חיבור לדאטהבייס ולקולקשן
# Soul_Studio = client['Soul_Studio']  # שם הדאטהבייס
# users_col = Soul_Studio['users']  # שם הקולקשן של המשתמשים
#
# # פונקציה להכנסת כמה משתמשים
# def insert_users_test():
#     users = [
#         {'name': 'shelly', 'lastname': 'bar', 'age': 27},
#         {'name': 'david', 'lastname': 'cohen', 'age': 30},
#         {'name': 'lea', 'lastname': 'levi', 'age': 25}
#     ]
#     result = users_col.insert_many(users)  # הכנסת הנתונים
#     print(f"Inserted IDs: {result.inserted_ids}")  # הדפסת ה-IDs שנוספו
#
# # קריאה לפונקציה כדי להכניס את הנתונים
# if __name__ == "__main__":
#     insert_users_test()
# # ---- יצירת תיקייה לשמירת קבצים ----
# UPLOAD_FOLDER = "static/uploads/"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#
# # ---- פונקציות לניהול משתמשים ----
#
# def user_exists(email):
#     """בודק האם המשתמש כבר קיים במערכת לפי כתובת הדוא"ל"""
#     return users_col.find_one({"email": email}) is not None
#
#
# def authenticate_user(user_email, user_password):
#     """בודק אם המשתמש קיים במסד הנתונים עם הסיסמה הנכונה (לצורך התחברות)"""
#     user = users_col.find_one({"email": user_email})
#     if user and user_password == user["password"]:
#         return user  # מחזיר את המשתמש אם הפרטים תקינים
#     return None
#
# def insert_user(first_name, last_name, birth_date, email, phone_number, password, health_file):
#     """מוסיף משתמש חדש למסד הנתונים"""
#     if user_exists(email):
#         return None  # המשתמש כבר קיים
#
#     # טיפול בשמירת הקובץ
#     health_file_path = None
#     if health_file:
#         filename = secure_filename(health_file.filename)  # מאבטח את שם הקובץ
#         health_file_path = os.path.join(UPLOAD_FOLDER, filename)  # יצירת נתיב שמירה
#         health_file.save(health_file_path)  # שמירת הקובץ בשרת
#     # יצירת מסמך משתמש חדש
#     user_data = {
#         "first_name": first_name,
#         "last_name": last_name,
#         "birth_date": birth_date,
#         "email": email,
#         "phone_number": phone_number,
#         "password": password,  # ⚠️ בעתיד עדיף להצפין את הסיסמה!
#         "health_file": health_file_path  # שמירת הנתיב במקום האובייקט
#     }
#
#     result = users_col.insert_one(user_data)
#     return str(result.inserted_id)  # מחזיר את ה-ID של המשתמש החדש
#
# # --------------------------------- פונקציות לניהול שיעורים --------------------------
# from bson.objectid import ObjectId
# # חיבור למסד הנתונים
#
# registrations_col = Soul_Studio["registrations"]
# classes_collection = Soul_Studio["classes"]
#
# # פונקציה להוספת שיעורים (אם לא קיימים)
# def add_classes_if_not_exist():
#     classes = [
#         {"day": "Sunday", "time": "07:00", "title": "יוגה אשטנגה - מתחילות", "capacity": 10, "registered_users": [], "waitlist_users": []},
#         {"day": "Sunday", "time": "08:00", "title": "יוגה ויניאסה - מתחילות", "capacity": 10, "registered_users": [], "waitlist_users": []},
#         {"day": "Sunday", "time": "18:00", "title": "יוגה אשטנגה - מתקדמות", "capacity": 10, "registered_users": [], "waitlist_users": []},
#         {"day": "Sunday", "time": "19:00", "title": "Power yoga", "capacity": 10, "registered_users": [], "waitlist_users": []},
#         {"day": "Sunday", "time": "20:00", "title": "יוגה ויניאסה - כל הרמות", "capacity": 10, "registered_users": [], "waitlist_users": []}
#     ]
#     for cls in classes:
#         if not classes_collection.find_one({"day": cls["day"], "time": cls["time"]}):
#             classes_collection.insert_one(cls)
#
# # פונקציה לקבלת שיעורי יום מסוים
# def get_classes_by_day(day):
#     return list(classes_collection.find({"day": day}))
#
# # פונקציה לרישום משתמש לשיעור
# from bson import ObjectId
#
# def register_user_to_class(class_id, user_email):
#     cls = classes_collection.find_one({"_id": ObjectId(class_id)})
#     if not cls:
#         return "not_found"
#
#     # בדיקה אם המשתמש כבר רשום
#     if user_email in cls["registered_users"]:
#         return "already_registered"
#
#     if len(cls["registered_users"]) < cls["capacity"]:
#         classes_collection.update_one(
#             {"_id": ObjectId(class_id)},
#             {"$push": {"registered_users": user_email}}
#         )
#         return "success"
#     else:
#         return "full"
#
# # פונקציה לרישום לרשימת המתנה
# def add_to_waitlist(class_id, user_email):
#     cls = classes_collection.find_one({"_id": ObjectId(class_id)})
#     if cls:
#         classes_collection.update_one({"_id": ObjectId(class_id)}, {"$push": {"waitlist_users": user_email}})
#         return "success"
#     return "not_found"
#
# # פונקציה לביטול הרשמה
# def cancel_registration(class_id, user_email):
#     cls = classes_collection.find_one({"_id": ObjectId(class_id)})
#     if cls:
#         if user_email in cls["registered_users"]:
#             classes_collection.update_one({"_id": ObjectId(class_id)}, {"$pull": {"registered_users": user_email}})
#             return "success"
#         elif user_email in cls["waitlist_users"]:
#             classes_collection.update_one({"_id": ObjectId(class_id)}, {"$pull": {"waitlist_users": user_email}})
#             return "success"
#     return "not_found"
#
# # פונקציה להבאת סטטוס שיעור (כמה מקומות נשארו) עובד !!!!!!!!!!!
# def get_class_status(class_id):
#     cls = classes_collection.find_one({"_id": ObjectId(class_id)})
#
#     print(f"📌 מסמך מה-DB: {cls}")  # הדפסה כדי לוודא שקיבלנו נתונים
#
#     if not cls:
#         print("❌ השיעור לא נמצא!")
#         return None  # מחזירה None אם השיעור לא נמצא
#
#     # מבטיחים שהשדות תמיד יהיו קיימים
#     registered_users = cls.get("registered_users", [])  # אם חסר - מחזירים רשימה ריקה
#     capacity = cls.get("capacity", 10)  # אם חסר - ברירת מחדל של 10 מקומות
#
#     print(f"✅ רשומים: {registered_users}, קיבולת: {capacity}")  # לוודא שהתוכן תקין
#
#     spots_left = capacity - len(registered_users)
#     return {
#         "classId": class_id,
#         "spotsLeft": spots_left,
#         "spotsFilled": len(registered_users),  # מספר הנרשמים בפועל
#         "capacity": capacity
#     }
#
# # ------------
#
# ################################################################################
# # פונקציה לבדיקת קיום משתמשת במערכת
# def get_user_by_email(email):
#     return users_col.find_one({"email": email})
#
# def get_all_users():
#     """שליפת כל המשתמשות מהקולקשן Users"""
#     users = list(users_col.find({}, {"_id": 0}))  # מוציאים את ה-_id מהתוצאה
#     return users
#
#
# def email_exists(email):
#     if users_col.find_one({"email": email}):
#         return True
#     return False
