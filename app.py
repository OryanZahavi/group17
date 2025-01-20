from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/Home_Page')
def home_page():
    return render_template('Home_Page.html')

# @app.route('/My_Account')
# def my_account_page():
#     return render_template('My_Account.html')
@app.route('/Contact_Us')
def contact_us_page():
    return render_template('Contact_Us.html')
@app.route('/Meet_Us')
def meet_us_page():
    return render_template('Meet_Us.html')
@app.route('/Sunday_Schedule')
def sunday_schedule_page():
    return render_template('Sunday_Schedule.html')

@app.route('/Monday_Schedule')
def monday_schedule_page():
    return render_template('Monday_Schedule.html')
@app.route('/Tuesday_Schedule')
def tuesday_schedule_page():
    return render_template('Tuesday_Schedule.html')
@app.route('/Wednesday_Schedule')
def wednesday_schedule_page():
    return render_template('Wednesday_Schedule.html')
@app.route('/Thursday_Schedule')
def thursday_schedule_page():
    return render_template('Thursday_Schedule.html')

##############################
@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/costomer')
def go_to_contact():
    return redirect(url_for('contact_page'))  # מפנה לעמוד Contact

#
# @app.route('/index')
# @app.route('/home')
# @app.route('/')
# def Home_page():
#     # import from DB
    # first_name = ''
    # last_name = 'Applebaum'
    # age = 28

    # user = {
    #     'first_name': 'ofri',
    #     'last_name': 'Applebaum',
    #     'age': 50,
    # }
    # hobbies = ['Dance','sing','eat']
    # degrees = ('M.Sc')
    #
    # return render_template(
    #     'index.html',
    #    user= user,
    #     hobbies=hobbies,
    #     degrees=degrees,
    # )

################################

@app.route('/Block_example')
def block_example_func():
    return render_template('Block_example.html')


@app.route('/contacts')
def contacts_func():
    return render_template('contacts.html')

# if __name__ == '__main__':
#     app.run(debug=True)
