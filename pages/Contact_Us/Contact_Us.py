from flask import Blueprint, render_template, request, redirect, url_for
from db_functions import insert_inquiry

Contact_Us = Blueprint('Contact_Us', __name__,
                       static_folder='static',
                       static_url_path='/Contact_Us',
                       template_folder='templates')


@Contact_Us.route('/Contact_Us')
def index():
    return render_template('Contact_Us.html')


@Contact_Us.route('/new_inquiry', methods=['POST'])
def new_inquiry():
    first_name = request.form.get('user_FirstName')
    last_name = request.form.get('user_LastName')
    email = request.form.get('user_Email')
    phone_number = request.form.get('user_PhoneNumber')
    description = request.form.get('Description')

    insert_inquiry(first_name, last_name, email, phone_number, description)

    return redirect(url_for('Home_Page.index'))
