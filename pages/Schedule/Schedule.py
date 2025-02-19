from flask import Blueprint, render_template
# about Blueprint definition
Schedule = Blueprint(
    'Schedule',
    __name__,
    static_folder='static',
    static_url_path='/Schedule',
    template_folder='templates'
)

# Routs

@Schedule.route('/Sunday_Schedule')
def sunday_schedule_page():
    return render_template('Sunday_Schedule.html')


@Schedule.route('/Monday_Schedule')
def monday_schedule_page():
    return render_template('Monday_Schedule.html')


@Schedule.route('/Tuesday_Schedule')
def tuesday_schedule_page():
    return render_template('Tuesday_Schedule.html')


@Schedule.route('/Wednesday_Schedule')
def wednesday_schedule_page():
    return render_template('Wednesday_Schedule.html')


@Schedule.route('/Thursday_Schedule')
def thursday_schedule_page():
    return render_template('Thursday_Schedule.html')