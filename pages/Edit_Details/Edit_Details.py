from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_functions import get_user_data, update_user_data

# Blueprint definition
Edit_Details = Blueprint(
    'Edit_Details',
    __name__,
    static_folder='static',
    static_url_path='/Edit_Details',
    template_folder='templates'
)

# Route to display the Edit Details form
@Edit_Details.route('/Edit_Details', methods=['GET', 'POST'])
def index():
    user_email = session.get('email')
    if not user_email:
        return redirect(url_for('Entry_Screen.entry_screen'))  # Redirect to login if not logged in

    # Fetch user data from the database
    user_data = get_user_data(user_email)
    if not user_data:
        return "User not found", 404

    return render_template('Edit_Details.html', user_data=user_data)

# Route to handle form submission and update user data
@Edit_Details.route('/update', methods=['POST'])
def update_user():
    # Get updated data from the form
    user_email = session.get('email')
    user_data = get_user_data(user_email)

    updated_data = {
        "first_name": request.form.get('first_name'),
        "last_name": request.form.get('last_name'),
        "birth_date": request.form.get('birth_date'),
        "email": request.form.get('email'),
        "phone_number": request.form.get('phone_number'),
    }

    # Check if any data has changed
    changes_made = any(updated_data[key] != user_data.get(key) for key in updated_data)

    if not changes_made:
        flash('לא בוצעו שינויים בפרטים', 'info')
        return redirect(url_for('Home_Page.index'))


    # Update the user's data in the database
    update_result = update_user_data(session['email'], updated_data)

    if update_result:
        # Update session with new user data
        session['user_name'] = updated_data['first_name']
        session['email'] = updated_data['email']
        session.modified = True  # Mark the session as modified

        flash('פרטי המשתמש עודכנו בהצלחה', 'success')
        return redirect(url_for('Home_Page.index'))  # Redirect to Home Page
    else:
        flash('אירעה שגיאה בעדכון הפרטים', 'error')
        return redirect(url_for('Edit_Details.index'))