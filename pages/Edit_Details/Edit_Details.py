from flask import Blueprint, render_template, request, redirect, url_for

# about Blueprint definition
Edit_Details = Blueprint(
    'Edit_Details',
    __name__,
    static_folder='static',
    static_url_path='/Edit_Details',
    template_folder='templates'
)

# Routs
@Edit_Details.route('/Edit_Details')
def index():
    return render_template('Edit_Details.html')