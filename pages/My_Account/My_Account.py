from flask import Blueprint, render_template
# about Blueprint definition
My_Account = Blueprint(
    'My_Account',
    __name__,
    static_folder='static',
    static_url_path='/My_Account',
    template_folder='templates'
)

# Routs

@My_Account.route('/My_Account')
def index():
    return render_template('My_Account.html')

