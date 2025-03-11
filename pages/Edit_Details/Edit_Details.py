from flask import Blueprint, render_template, request, redirect, url_for, session
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
def update_user_data_route():
    user_email = session.get('email')

    # Get updated data from the form
    updated_data = {
        "first_name": request.form.get('first_name'),
        "last_name": request.form.get('last_name'),
        "birth_date": request.form.get('birth_date'),
        "email": request.form.get('email'),
        "phone_number": request.form.get('phone_number'),
        "health_file": request.files.get('health_file')  # Handle file upload
    }

    # Save health file (if uploaded)
    if updated_data["health_file"]:
        health_file_path = f'static/uploads/{updated_data["health_file"].filename}'
        updated_data["health_file"].save(health_file_path)
        updated_data["health_file"] = health_file_path  # Save the file path in the database

    # Call the update_user_data function with email and updated data
    update_result = update_user_data(user_email, updated_data)

    if update_result:
        return redirect(url_for('My_Account.index'))  # Redirect to My Account after successful update
    else:
        return "Failed to update data", 500







# from flask import Blueprint, render_template, request, redirect, url_for
#
# # about Blueprint definition
# Edit_Details = Blueprint(
#     'Edit_Details',
#     __name__,
#     static_folder='static',
#     static_url_path='/Edit_Details',
#     template_folder='templates'
# )
#
# # Routs
# @Edit_Details.route('/Edit_Details')
# def index():
#     return render_template('Edit_Details.html')