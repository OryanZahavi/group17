from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db_functions import get_user_by_email  # פונקציה שתבדוק אם המשתמשת קיימת

Entry_Screen = Blueprint(
    'Entry_Screen',
    __name__,
    static_folder='static',
    static_url_path='/Entry_Screen',
    template_folder='templates'
)

# הצגת דף הכניסה
@Entry_Screen.route('/Entry_Screen', methods=['GET'])
def entry_screen():
    return render_template('Entry_Screen.html')

# טיפול בהתחברות משתמשת
@Entry_Screen.route('/Entry_Screen', methods=['POST'])
def login():
    email = request.form.get('user_Email')
    password = request.form.get('user_Password')

    user = get_user_by_email(email)  # נבדוק אם המשתמשת קיימת

    if user and user["password"] == password:  # בדיקת סיסמה
        session['user_email'] = email  # שמירת המשתמשת בסשן
        return redirect(url_for('Home_Page.home_page'))  # הפניה לדף הבית

    # אם המשתמשת לא קיימת או שהסיסמה לא נכונה - הצגת הודעה
    return render_template('Entry_Screen.html', error="שם משתמש או סיסמה שגויים")


# from flask import Blueprint, render_template
#
# # about Blueprint definition
# Entry_Screen = Blueprint(
#     'Entry_Screen',
#     __name__,
#     static_folder='static',
#     static_url_path='/Entry_Screen',
#     template_folder='templates'
# )
#
# # Routs
# @Entry_Screen.route('/Entry_Screen')
# def entry_screen():
#     return render_template('Entry_Screen.html')