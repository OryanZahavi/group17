from flask import Blueprint, render_template
# about Blueprint definition
Monday_Schedule = Blueprint(
    'Monday_Schedule',
    __name__,
    static_folder='static',
    static_url_path='/Monday_Schedule',
    template_folder='templates'
)

# Routs

@Monday_Schedule.route('/Monday_Schedule')
def index():
    return render_template('Monday_Schedule.html')

