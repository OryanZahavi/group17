from flask import Blueprint, render_template, request, jsonify, session
from db_functions import insert_classes, get_classes_by_day, register_user_to_class, add_to_waitlist, \
    cancel_registration, get_class_status, can_cancel_class, update_class_dates

# הגדרת ה-Blueprint
Sunday_Schedule = Blueprint(
    'Sunday_Schedule',
    __name__,
    static_folder='static',
    static_url_path='/Sunday_Schedule',
    template_folder='templates'
)

# יצירת השיעורים במסד הנתונים (אם הם לא קיימים)
insert_classes()
update_class_dates()

@Sunday_Schedule.route('/Sunday_Schedule')
def index():
    classes = get_classes_by_day("Sunday")
    # מוסיף מספר נרשמים לכל שיעור
    for cls in classes:
        cls["spots_filled"] = len(cls["registered_users"])  # כמות רשומים
    return render_template('Sunday_Schedule.html', classes=classes)


# רישום משתמש לשיעור- עובד!!
@Sunday_Schedule.route('/Sunday_Schedule/register', methods=['POST'])
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


@Sunday_Schedule.route('/Sunday_Schedule/class_status/<class_id>', methods=['GET'])
def class_status(class_id):
    class_data = get_class_status(class_id)

    if not class_data:
        return jsonify({"error": "Class not found"}), 404

    return jsonify({
        "spotsFilled": class_data.get("spotsFilled", 0),
        "capacity": class_data.get("capacity", 10),
        "spotsLeft": class_data.get("capacity", 10) - class_data.get("spotsFilled", 0),
        "datetime": class_data.get("date")  # מחזירים גם את זמן השיעור
    })

# הוספה לרשימת המתנה
@Sunday_Schedule.route('/Sunday_Schedule/waitlist', methods=['POST'])
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

# ביטול הרשמה עם בדיקת זמן
@Sunday_Schedule.route('/Sunday_Schedule/cancel', methods=['POST'])
def cancel():
    data = request.get_json()
    class_id = data.get('class_id')
    user_email = session.get('email')

    if not user_email:
        return jsonify({"status": "error", "message": "משתמש לא מחובר"})

    cancel_status = can_cancel_class(class_id, user_email)

    if cancel_status["status"] == "too_late":
        return jsonify({"status": "error", "message": cancel_status["message"]})

    if cancel_status["status"] == "late_cancel":
        return jsonify({"status": "warning", "message": cancel_status["message"]})  # התרעה לפני חיוב

    result = cancel_registration(class_id, user_email)
    if result == "success":
        return jsonify({"status": "success", "message": "ההרשמה שלך בוטלה בהצלחה!"})
    else:
        return jsonify({"status": "error", "message": "לא נמצאה הרשמה לשיעור זה."})

# # ביטול הרשמה
# @Sunday_Schedule.route('/Sunday_Schedule/cancel', methods=['POST'])
# def cancel():
#     data = request.get_json()  # ← שינוי
#     class_id = data.get('class_id')
#     user_email = session.get('email')
#
#     if not user_email:
#         return jsonify({"status": "error", "message": "משתמש לא מחובר"})
#
#     result = cancel_registration(class_id, user_email)
#     if result == "success":
#         return jsonify({"status": "success", "message": "ההרשמה שלך בוטלה בהצלחה!"})
#     else:
#         return jsonify({"status": "error", "message": "לא נמצאה הרשמה לשיעור זה."})
#
#
