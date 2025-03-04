from flask import Blueprint, render_template, request, jsonify, session
from db_functions import add_classes_if_not_exist, get_classes_by_day, register_user_to_class, add_to_waitlist, \
    cancel_registration

# הגדרת ה-Blueprint
Sunday_Schedule = Blueprint(
    'Sunday_Schedule',
    __name__,
    static_folder='static',
    static_url_path='/Sunday_Schedule',
    template_folder='templates'
)

# יצירת השיעורים במסד הנתונים (אם הם לא קיימים)
add_classes_if_not_exist()


@Sunday_Schedule.route('/Sunday_Schedule')
def index():
    classes = get_classes_by_day("Sunday")
    # מוסיף מספר נרשמים לכל שיעור
    for cls in classes:
        cls["spots_filled"] = len(cls["registered_users"])  # כמות רשומים
    return render_template('Sunday_Schedule.html', classes=classes)


# רישום משתמש לשיעור
@Sunday_Schedule.route('/Sunday_Schedule/register', methods=['POST'])
def register():
    data = request.get_json()  # ← שינוי כדי לקרוא JSON
    class_id = data.get('class_id')
    user_email = session.get('email')

    if not user_email:
        return jsonify({"status": "error", "message": "משתמש לא מחובר"})

    result = register_user_to_class(class_id, user_email)
    if result == "success":
        return jsonify({"status": "success", "message": "הרשמתך לשיעור אושרה!"})
    elif result == "full":
        return jsonify({"status": "full", "message": "השיעור מלא, נוספת לרשימת ההמתנה."})
    else:
        return jsonify({"status": "error", "message": "השיעור לא נמצא."})


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


# ביטול הרשמה
@Sunday_Schedule.route('/Sunday_Schedule/cancel', methods=['POST'])
def cancel():
    data = request.get_json()  # ← שינוי
    class_id = data.get('class_id')
    user_email = session.get('email')

    if not user_email:
        return jsonify({"status": "error", "message": "משתמש לא מחובר"})

    result = cancel_registration(class_id, user_email)
    if result == "success":
        return jsonify({"status": "success", "message": "ההרשמה שלך בוטלה בהצלחה!"})
    else:
        return jsonify({"status": "error", "message": "לא נמצאה הרשמה לשיעור זה."})


@Sunday_Schedule.route('/Sunday_Schedule/class_status/<class_id>', methods=['GET'])
def class_status(class_id):
    print(f"📢 בקשה לסטטוס שיעור: {class_id}")  # בדיקה - לראות שהקריאה מתבצעת
    from db_functions import get_class_status

    class_data = get_class_status(class_id)
    print(f"📌 קיבלנו מה-DB: {class_data}")  # לוודא שהתוכן תקין

    if not class_data:
        return jsonify({"error": "Class not found"}), 404

    return jsonify({
        "spotsFilled": class_data.get("spotsFilled", 0),
        "capacity": class_data.get("capacity", 10),
        "spotsLeft": class_data.get("spotsLeft", class_data.get("capacity", 10) - class_data.get("spotsFilled", 0))
    })




# @Sunday_Schedule.route('/class_status/<class_id>', methods=['GET'])
# def class_status(class_id):
#     from db_functions import get_class_status
#     class_data = get_class_status(class_id)
#     if class_data is None:
#         return jsonify({"error": "Class not found"}), 404
#
#     return jsonify({
#         "spotsFilled": len(class_data["registered_users"]),
#         "capacity": class_data["capacity"]
#     })


# from flask import Blueprint, render_template
# # about Blueprint definition
# Sunday_Schedule = Blueprint(
#     'Sunday_Schedule',
#     __name__,
#     static_folder='static',
#     static_url_path='/Sunday_Schedule',
#     template_folder='templates'
# )
#
# # Routs
#
# @Sunday_Schedule.route('/Sunday_Schedule')
# def index():
#     return render_template('Sunday_Schedule.html')
#
