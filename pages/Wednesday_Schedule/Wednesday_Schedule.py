from flask import Blueprint, render_template
# about Blueprint definition
Wednesday_Schedule = Blueprint(
    'Wednesday_Schedule',
    __name__,
    static_folder='static',
    static_url_path='/Wednesday_Schedule',
    template_folder='templates'
)

# Routs

@Wednesday_Schedule.route('/Wednesday_Schedule')
def index():
    return render_template('Wednesday_Schedule.html')

