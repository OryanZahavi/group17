from flask import session
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
inquiries_col = Soul_Studio["inquiries"] # קולקשיין של הפניות

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
    print("Inserted IDs: {result.inserted_ids}")  # הדפסת ה-IDs שנוספו


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


from datetime import datetime


def get_user_data(email):
    user = users_col.find_one({"email": email})
    if user:
        birth_date = user.get("birth_date")
        formatted_birth_date_ymd = ""
        formatted_birth_date_dmy = ""

        if birth_date:
            try:
                # Try parsing as YYYY-MM-DD
                date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
                formatted_birth_date_ymd = date_obj.strftime("%Y-%m-%d")
                formatted_birth_date_dmy = date_obj.strftime("%d-%m-%Y")
            except ValueError:
                try:
                    # If that fails, try parsing as DD-MM-YYYY
                    date_obj = datetime.strptime(birth_date, "%d-%m-%Y")
                    formatted_birth_date_ymd = date_obj.strftime("%Y-%m-%d")
                    formatted_birth_date_dmy = date_obj.strftime("%d-%m-%Y")
                except ValueError:
                    # If both fail, leave as empty strings
                    pass

        return {
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "birth_date": formatted_birth_date_ymd,  # For Edit Details (YYYY-MM-DD)
            "birth_date_display": formatted_birth_date_dmy,  # For My Account (DD-MM-YYYY)
            "email": user.get("email"),
            "phone_number": user.get("phone_number"),
            "health_file": user.get("health_file")
        }
    return None


def update_user_data(email, updated_data):
    """Update user data in the database."""
    try:
        result = users_col.update_one(
            {"email": email},  # Find the user by email
            {"$set": updated_data}  # Update with new data
        )
        return result.modified_count > 0  # Return True if at least one document was modified
    except Exception as e:
        print(f"Error updating user data: {e}")
        return False

def update_user_password(email, new_password):
    """Update the user's password in the database."""
    try:
        result = users_col.update_one(
            {"email": email},
            {"$set": {"password": new_password}}  # Replace with hashed password in production
        )
        return result.modified_count > 0  # Return True if at least one document was modified
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
# --------------------------------- פונקציות לניהול שיעורים --------------------------

#  פונקציה ראשונית להכנסת משתמשים ------

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

# פקודות ליצירה ומחיקת שיעורים ידנית
# קריאה לפונקציה להוספת השיעורים ומחיקה ----
# insert_classes() # אחרי הכנסה ראשונית אין צורך להפעיל בשנית
# classes_collection.delete_many({})
# print("🗑️ כל המסמכים בקולקשן נמחקו!")


#  פונקציה לעדכון לוח הזמנים ------

def update_classes(day=None):
    """
    מעדכן את התאריך של שיעורי הסטודיו בשבוע קדימה ומרוקן רשימות נרשמים.
    - אם מצוין יום ספציפי (`Sunday`, `Monday` וכו'), יעדכן רק את אותו יום.
    - אם לא מצוין יום, יעדכן את כל השיעורים לכל הימים.
    """
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

    if day:  # אם ניתן יום ספציפי, מעדכן רק אותו
        if day not in days_of_week:
            print(f"⚠️ יום {day} אינו תקין. יש לבחור מתוך {days_of_week}.")
            return
        days_to_update = [day]
    else:  # אם לא ניתן יום, מעדכן את כל הימים
        days_to_update = days_of_week

    for day in days_to_update:
        classes = classes_collection.find({"day": day})

        for cls in classes:
            new_date = cls["date"] + timedelta(days=7)
            classes_collection.update_one(
                {"_id": cls["_id"]},
                {"$set": {
                    "date": new_date,
                    "registered_users": [],
                    "waitlist_users": []
                }}
            )
        print(f"🎯 שיעורי יום {day} עודכנו!")


#  יופעל ביום חמישי בשעה לאחר השיעור האחרון לאיפוס רשימות הרשמה והמתנה ועדכון התאריכים

def get_last_thursday_class():
    """
    Fetch the most recent Thursday class from the database.
    """
    pipeline = [
        {
            "$addFields": {
                "weekday": {"$dayOfWeek": "$date"}  # MongoDB: Sunday=1, Monday=2, ..., Saturday=7
            }
        },
        {
            "$match": {
                "weekday": 5  # Thursday is 5 in MongoDB's $dayOfWeek
            }
        },
        {
            "$sort": {"date": -1}  # Sort by date descending (most recent first)
        },
        {
            "$limit": 1  # Get only the most recent Thursday class
        }
    ]

    result = list(classes_collection.aggregate(pipeline))
    if result:
        return result[0]["date"]  # Return the date of the most recent Thursday class
    return None


def check_and_update():
    """
    Check if an update is needed and perform it. Recheck after updating.
    """
    while True:
        last_thursday_class = get_last_thursday_class()

        if last_thursday_class:
            last_thursday_class = last_thursday_class.replace(tzinfo=None)  # Remove timezone info if present
            today = datetime.now()

            if today > last_thursday_class:
                update_classes()
            else:
                print("No further updates are needed.")
                break  # Exit the loop if no update is needed
        else:
            print("No Thursday classes found in the database.")
            break  # Exit the loop if no Thursday classes exist

# Main logic
check_and_update()


#  פונקציה שמחזירה כמה זמן נשאר עוד עד לשיעור מסויים ------

def time_until_class(class_id):
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


#  פונקציה שבודקת האם המשתמשת שמחוברת רשומה לשיעור מסוים------

def is_user_registered(class_id):

    # שליפת השיעור מה-DB
    cls = classes_collection.find_one({"_id": ObjectId(class_id)})
    if not cls:
        print(f"❌ שגיאה: שיעור עם ID {class_id} לא נמצא!")
        return None  # השיעור לא נמצא במערכת

    # שליפת כתובת האימייל של המשתמשת המחוברת
    user_email = session.get("email")
    if not user_email:
        print("⚠️ משתמשת אינה מחוברת!")
        return False  # אין משתמשת מחוברת

    # רשימת הנרשמות לשיעור
    registered_users = cls.get("registered_users", [])
    print(f"📜 רשימת המשתמשות הרשומות מה-DB: {registered_users}")  # Debugging

    # בדיקה אם המשתמשת רשומה לשיעור (לא תלוי באותיות גדולות/קטנות)
    is_registered = any(user_email.strip().lower() == str(email).strip().lower() for email in registered_users)

    print(f"👤 האם המשתמשת רשומה לשיעור? {is_registered}")
    return is_registered  # מחזיר True אם רשומה, False אם לא


#  פונקציה שמחזירה מידע על מצב השיעור------

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



# פונקציה לקבלת שיעורי יום מסוים ------
def get_classes_by_day(day):
    return list(classes_collection.find({"day": day}))


# פונקציה לרישום משתמש לשיעור ------

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


# פונקציה לרישום לרשימת המתנה ------
def add_to_waitlist(class_id, user_email):
    cls = classes_collection.find_one({"_id": ObjectId(class_id)})
    if cls:
        classes_collection.update_one({"_id": ObjectId(class_id)}, {"$push": {"waitlist_users": user_email}})
        return "success"
    return "not_found"


# פונקציה שמבטלת הרשמה של המשתמשת המחוברת לשיעור במסד הנתונים. ------

def cancel_registration(class_id):

    user_email = session.get('email')  # שליפת האימייל מתוך הסשן
    if not user_email:
        return "not_logged_in"

    cls = classes_collection.find_one({"_id": ObjectId(class_id)})

    if not cls:
        return "not_found"

    if user_email in cls["registered_users"]:
        classes_collection.update_one({"_id": ObjectId(class_id)}, {"$pull": {"registered_users": user_email}})
        return "success"

    elif user_email in cls["waitlist_users"]:
        classes_collection.update_one({"_id": ObjectId(class_id)}, {"$pull": {"waitlist_users": user_email}})
        return "success"

    return "not_registered"

# פונקציה שבודקת האם משתמשת מחוברת יכולה לבטל הרשמה לשיעור ------

def can_cancel_class(class_id):
  
    # שליפת האימייל של המשתמשת המחוברת מתוך ה-session
    user_email = session.get('email')
    if not user_email:
        return {"status": "error", "message": "משתמשת לא מחוברת."}

    # שליפת נתוני השיעור מה-DB
    cls = classes_collection.find_one({"_id": ObjectId(class_id)})
    if not cls:
        return {"status": "error", "message": "השיעור לא נמצא."}

    # בדיקה אם המשתמשת רשומה לשיעור
    registered_users = cls.get("registered_users", [])
    if user_email not in registered_users:
        return {"status": "not_registered", "message": "המשתמשת אינה רשומה לשיעור."}

    # שליפת זמן השיעור וחישוב הזמן שנותר
    class_time = cls.get("date")
    if not class_time:
        return {"status": "error", "message": "נתוני השיעור חסרים."}

    now = datetime.now()
    time_difference_hours = (class_time - now).total_seconds() / 3600  # הפרש בשעות

    # תנאי ביטול
    if time_difference_hours <= 0:
        return {"status": "too_late", "message": "❌ לא ניתן לבטל - זמן השיעור כבר עבר."}

    if time_difference_hours < 7:
        return {"status": "late_cancel", "message": "⚠️ ביטול כרוך בתשלום, מאחר והזמן הנותר קטן מ-7 שעות."}

    return {"status": "allowed", "message": "ביטול אפשרי ללא תשלום"}

def insert_inquiry (first_name, last_name, email, phone_number,description):
     inquiry_data ={
         "firstName": first_name,
         "lastName": last_name,
         "email": email,
         "phoneNumber": phone_number,
         "description": description
         }
     inquiries_col.insert_one(inquiry_data)
     return ()