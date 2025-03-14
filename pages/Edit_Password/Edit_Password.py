from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_functions import authenticate_user, update_user_password

# Blueprint definition
Edit_Password = Blueprint(
    'Edit_Password',
    __name__,
    static_folder='static',
    static_url_path='/Edit_Password',
    template_folder='templates'
)

@Edit_Password.route('/Edit_Password', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_email = session.get('email')
        if not user_email:
            return redirect(url_for('Entry_Screen.Entry_Screen'))  # Redirect to login if not logged in

        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Verify old password using authenticate_user
        if not authenticate_user(user_email, old_password):
            flash('הסיסמה הישנה אינה נכונה', 'error')
            return redirect(url_for('Edit_Password.index'))

        # Check if new passwords match
        if new_password != confirm_password:
            flash('הסיסמאות החדשות אינן תואמות', 'error')
            return redirect(url_for('Edit_Password.index'))

        # Update password
        if update_user_password(user_email, new_password):
            flash('הסיסמה שונתה בהצלחה', 'success')
            return redirect(url_for('My_Account.index'))
        else:
            flash('אירעה שגיאה בעת שינוי הסיסמה', 'error')
            return redirect(url_for('Edit_Password.index'))

    return render_template('Edit_Password.html')
