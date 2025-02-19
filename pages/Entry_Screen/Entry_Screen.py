from flask import Blueprint, render_template

# about Blueprint definition
Entry_Screen = Blueprint(
    'Entry_Screen',
    __name__,
    static_folder='static',
    static_url_path='/Entry_Screen',
    template_folder='templates'
)

# Routs
@Entry_Screen.route('/Entry_Screen')
def entry_screen():
    return render_template('Entry_Screen.html')