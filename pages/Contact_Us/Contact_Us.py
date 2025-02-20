from flask import Blueprint, render_template

# about Blueprint definition
Contact_Us = Blueprint(
    'Contact_Us',
    __name__,
    static_folder='static',
    static_url_path='/Contact_Us',
    template_folder='templates'
)

# Routs
@Contact_Us.route('/Contact_Us')
def index():
    return render_template('Contact_Us.html')