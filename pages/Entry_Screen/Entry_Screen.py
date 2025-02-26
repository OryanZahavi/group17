from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db_functions import get_user_by_email, user_exist  # וודאי שהפונקציה מיובאת נכון

# יצירת ה-Blueprint
Entry_Screen = Blueprint('Entry_Screen', __name__,
                         static_folder='static',
                         static_url_path='/Entry_Screen',
                         template_folder='templates')


@Entry_Screen.route('/Entry_Screen', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('Entry_Screen.html')

    if request.is_json:
        data = request.get_json()  # קבלת הנתונים מה-Frontend בפורמט JSON
        email = data.get("user_email")
        password = data.get("user_password")

        if user_exist(email, password):
            session['email'] = email
            session['logged_in'] = True

            return jsonify({"message": "התחברות הצליחה", "status": "success", "redirect": "/Home_Page"})

    return jsonify({"message": "שם משתמש או סיסמה שגויים", "status": "error"}), 401  # שגיאה 401 = לא מורשה

#
#
#
# @Entry_Screen.route('/Entry_Screen', methods=['GET', 'POST'])
#
# def sign_in_web():
#     if request.method == 'POST':
#         email = request.form.get('user_Email')
#         password = request.form.get('user_Password')
#
#         user = get_user_by_email(email)  # נבדוק אם המשתמשת קיימת
#
#         if user and user["password"] == password:  # בדיקת סיסמה
#             session['user_email'] = email  # שמירת המשתמשת בסשן
#             return redirect('/Home_Page')  # הפניה לדף הבית
#
#         # אם המשתמשת לא קיימת או שהסיסמה לא נכונה - הצגת הודעה
#         return render_template('Entry_Screen.html', error="שם משתמש או סיסמה שגויים")
#
#     return render_template('Entry_Screen.html')  # הצגת הדף במצב GET
