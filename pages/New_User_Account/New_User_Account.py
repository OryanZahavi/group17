from flask import Blueprint, render_template
# about Blueprint definition
New_User_Account = Blueprint(
    'New_User_Account',
    __name__,
    static_folder='static',
    static_url_path='/New_User_Account',
    template_folder='templates'
)

# Routs
@New_User_Account.route('/New_User_Account')
def new_user_account():
    return render_template('New_User_Account.html')