from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/Home_Page')
def Home_page():
    return render_template('Home_Page.html')

@app.route('/My_Account')
def My_Account_page():
    return render_template('My_Account.html')




@app.route('/Contact_Us')
def Contact_Us_page():
    return render_template('Contact_Us.html')


@app.route('/Meet_Us')
def Meet_Us_page():
    return render_template('Meet_Us.html')

# @app.route('/Sunday_Schedule')
# def Sunday_Schedule_page():
#     return render_template('Sunday_Schedule.html')

@app.route('/Monday_Schedule')
def Monday_Schedule_page():
    return render_template('Monday_Schedule.html')
@app.route('/Tuesday_Schedule')
def Tuesday_Schedule_page():
    return redirect(url_for('Tuesday_Schedule.html'))
@app.route('/Wednesday_Schedule')
def Wednesday_Schedule_page():
    return redirect(url_for('Wednesday_Schedule.html'))
@app.route('/Thursday_Schedule')
def Thursday_Schedule_page():
    return redirect(url_for('Thursday_Schedule.html'))



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
    # degrees = ('B.Sc','M.Sc')
    #
    # return render_template(
    #     'index.html',
    #    user= user,
    #     hobbies=hobbies,
    #     degrees=degrees,
    # )

################################

@app.route('/Block_example')
def Block_example_func():
    return render_template('Block_example.html')


@app.route('/contacts')
def contacts_func():
    return render_template('contacts.html')

# if __name__ == '__main__':
#     app.run(debug=True)
