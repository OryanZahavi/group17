from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_functions import insert_user ,user_exists # ייבוא פונקציה להכנסת משתמשים

# יצירת ה-Blueprint
New_User_Account = Blueprint(
    'New_User_Account',
    __name__,
    static_folder='static',
    static_url_path='/New_User_Account',
    template_folder='templates'
)

# דף ההרשמה
@New_User_Account.route('/New_User_Account')
def new_user_account():
    return render_template('New_User_Account.html')

# נתיב שמטפל בשליחת הנתונים מהטופס ושמירתם במסד הנתונים
@New_User_Account.route('/register', methods=['POST'])
def register():
    # קבלת הנתונים מהטופס
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    birth_date = request.form.get('birth_date')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')
    health_form = request.files.get('health_form')

    # שימוש בפונקציה להוספת משתמש
    user_id = insert_user(first_name, last_name, birth_date, email, phone_number, password, health_form)

    if user_id is None:
        flash("כתובת הדוא\"ל כבר קיימת במערכת. נסי להתחבר.", "error")
        return redirect(url_for('New_User_Account.new_user_account'))

    # שמירת המשתמש ב-Session
    session['user_id'] = user_id
    session['user_name'] = first_name

    flash("ההרשמה בוצעה בהצלחה!", "success")
    return redirect(url_for('Home_Page.index'))

@New_User_Account.route('/log_out')
def log_out_func():
    session.clear()  # מוחק את הנתונים מה-Session
    return redirect(url_for('Home_Page.index'))  # מחזיר לדף הבית

#####################################
# from flask import Blueprint, render_template
# # about Blueprint definition
# New_User_Account = Blueprint(
#     'New_User_Account',
#     __name__,
#     static_folder='static',
#     static_url_path='/New_User_Account',
#     template_folder='templates'
# )
#
# # Routs
# @New_User_Account.route('/New_User_Account')
# def new_user_account():
#     return render_template('New_User_Account.html')

