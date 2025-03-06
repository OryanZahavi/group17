from flask import Blueprint, render_template, request, jsonify, session
from db_functions import get_classes_by_day, register_user_to_class, add_to_waitlist, \
    get_class_status, can_cancel_class, classes_collection, \
    time_until_class, is_user_registered, cancel_registration
import schedule
import time
from bson.objectid import ObjectId

# הגדרת ה-Blueprint
Monday_Schedule = Blueprint(
    'Monday_Schedule',
    __name__,
    static_folder='static',
    static_url_path='/Monday_Schedule',
    template_folder='templates'
)


@Monday_Schedule.route('/Monday_Schedule')
def index():
    classes = get_classes_by_day("Monday")
    # מוסיף מספר נרשמים לכל שיעור
    for cls in classes:
        cls["spots_filled"] = len(cls["registered_users"])  # כמות רשומים
        print(f"📌 מספר השיעורים המועברים ל-HTML: {len(classes)}")

    return render_template('Monday_Schedule.html', classes=classes)


@Monday_Schedule.route('/Monday_Schedule/time_until/<class_id>', methods=['GET'])
def get_time_until_class(class_id):
    result = time_until_class(class_id)
    if result is None:
        return jsonify({"error": "שיעור לא נמצא"}), 404
    if result is False:
        return jsonify({"expired": True, "message": "⏳ זמן השיעור עבר"}), 200

    return jsonify(result)


# רישום משתמש לשיעור
@Monday_Schedule.route('/Monday_Schedule/register', methods=['POST'])
def register():
    data = request.get_json()
    class_id = data.get('class_id')
    user_email = session.get('email')

    if not user_email:
        return jsonify({"status": "error", "message": "משתמש לא מחובר"})

    result = register_user_to_class(class_id, user_email)
    if result == "success":
        return jsonify({"status": "success", "message": "הרשמתך לשיעור אושרה!"})
    elif result == "already_registered":
        return jsonify({"status": "error", "message": "את/ה כבר רשום/ה לשיעור הזה!"})
    elif result == "full":
        return jsonify({"status": "full", "message": "השיעור מלא, נוספת לרשימת ההמתנה."})
    else:
        return jsonify({"status": "error", "message": "השיעור לא נמצא."})


@Monday_Schedule.route('/Monday_Schedule/class_status/<class_id>', methods=['GET'])
def class_status(class_id):
    class_data = get_class_status(class_id)

    if not class_data:
        return jsonify({"error": "Class not found"}), 404

    # בדיקה אם המשתמשת המחוברת רשומה לשיעור
    user_registered = is_user_registered(class_id)

    return jsonify({
        "spotsFilled": class_data.get("spotsFilled", 0),
        "capacity": class_data.get("capacity", 10),
        "spotsLeft": class_data.get("capacity", 10) - class_data.get("spotsFilled", 0),
        "datetime": class_data.get("datetime"),  # מחזירים גם את זמן השיעור
        "userRegistered": user_registered  # מחזירים אם המשתמשת רשומה
    })


# הוספה לרשימת המתנה
@Monday_Schedule.route('/Monday_Schedule/waitlist', methods=['POST'])
def waitlist():
    data = request.get_json()  # ← שינוי
    class_id = data.get('class_id')
    user_email = session.get('email')

    if not user_email:
        return jsonify({"status": "error", "message": "משתמש לא מחובר"})

    result = add_to_waitlist(class_id, user_email)
    if result == "success":
        return jsonify({"status": "success", "message": "נוספת לרשימת ההמתנה!"})
    else:
        return jsonify({"status": "error", "message": "השיעור לא נמצא."})


@Monday_Schedule.route('/Monday_Schedule/cancel_status/<class_id>', methods=['GET'])
def cancel_status(class_id):
    """ מחזירה סטטוס ביטול השיעור למשתמשת המחוברת """
    result = can_cancel_class(class_id)
    return jsonify(result)


# ביטול הרשמה עם בדיקת זמן
@Monday_Schedule.route('/Monday_Schedule/cancel', methods=['POST'])
def cancel():
    data = request.get_json()
    class_id = data.get('class_id')

    print(f"🔹 בקשת ביטול התקבלה! Class ID: {class_id}")

    cancel_status = can_cancel_class(class_id)
    print(f"🔸 סטטוס ביטול: {cancel_status}")  # ✅ מדפיס את הסטטוס

    if cancel_status["status"] in ["error", "too_late", "not_registered"]:
        return jsonify(cancel_status), 403

    if cancel_status["status"] == "late_cancel":
        return jsonify(cancel_status), 200

    result = cancel_registration(class_id)
    print(f"🔹 תוצאת ביטול בפועל: {result}")  # ✅ בודקים האם המחיקה הצליחה

    if result == "success":
        return jsonify({"status": "success", "message": "✅ ההרשמה שלך בוטלה בהצלחה!"}), 200
    else:
        return jsonify({"status": "error", "message": "❌ שגיאה בביטול ההרשמה"}), 500
