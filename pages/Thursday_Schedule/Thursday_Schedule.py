from flask import Blueprint, render_template
# about Blueprint definition
Thursday_Schedule = Blueprint(
    'Thursday_Schedule',
    __name__,
    static_folder='static',
    static_url_path='/Thursday_Schedule',
    template_folder='templates'
)

# Routs

@Thursday_Schedule.route('/Thursday_Schedule')
def index():
    return render_template('Thursday_Schedule.html')



