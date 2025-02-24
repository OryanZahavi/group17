from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_functions import insert_user, email_exists

New_User_Account = Blueprint('New_User_Account', __name__,
                             static_folder='static',
                             static_url_path='/New_User_Account',
                             template_folder='templates')

@New_User_Account.route('/New_User_Account', methods=['GET', 'POST'])
def new_user_account():
    if request.method == 'POST':
        first_name = request.form['user_FirstName']
        last_name = request.form['user_LastName']
        birth_date = request.form['user_Date']
        email = request.form['user_Email']
        phone = request.form['user_PhoneNumber']
        password = request.form['user_Password']
        health_file = request.form['user_Health']

        if email_exists(email):
            flash("האימייל כבר קיים במערכת.")
        elif insert_user(first_name, last_name, birth_date, email, phone, password, health_file):
            flash("הרשמה הושלמה בהצלחה!")
            return redirect(url_for('Entry_Screen.entry_screen'))  # חזרה למסך הכניסה

    return render_template('New_User_Account.html')

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