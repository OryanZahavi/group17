from flask import Blueprint, render_template
# about Blueprint definition
Tuesday_Schedule = Blueprint(
    'Tuesday_Schedule',
    __name__,
    static_folder='static',
    static_url_path='/Tuesday_Schedule',
    template_folder='templates'
)

# Routs

@Tuesday_Schedule.route('/Tuesday_Schedule')
def index():
    return render_template('Tuesday_Schedule.html')

