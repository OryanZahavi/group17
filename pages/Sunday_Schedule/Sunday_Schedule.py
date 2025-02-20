from flask import Blueprint, render_template
# about Blueprint definition
Sunday_Schedule = Blueprint(
    'Sunday_Schedule',
    __name__,
    static_folder='static',
    static_url_path='/Sunday_Schedule',
    template_folder='templates'
)

# Routs

@Sunday_Schedule.route('/Sunday_Schedule')
def index():
    return render_template('Sunday_Schedule.html')

