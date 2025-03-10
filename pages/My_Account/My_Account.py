from flask import Blueprint, render_template, session, redirect, url_for
from db_functions import get_user_data

My_Account = Blueprint(
    'My_Account',
    __name__,
    static_folder='static',
    static_url_path='/My_Account',
    template_folder='templates'
)

@My_Account.route('/My_Account')
def index():
    user_email = session.get('email')
    if not user_email:
        return redirect(url_for('Entry_Screen.entry_screen'))  # Redirect to login if not logged in

    user_data = get_user_data(user_email)

    if not user_data:
        return "User not found", 404

    return render_template('My_Account.html', user_data=user_data)
