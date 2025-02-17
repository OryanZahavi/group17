from flask import Flask, redirect, url_for, render_template, request, session
import json

app = Flask(__name__)
app.secret_key = '123'


# @app.route('/')
# @app.route('/Home_Page')
# def home_page():
#     return render_template('Home_Page.html')
#

@app.route('/My_Account')
def my_account_page():
    return render_template('My_Account.html')


@app.route('/Edit_Details')
def edit_details_page():
    return render_template('Edit_Details.html')


@app.route('/Contact_Us')
def contact_us_page():
    return render_template('pages/Contact_Us/templates/Contact_Us.html')


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


@app.route('/Entry_Screen')
def entry_screen_page():
    if request.method == 'GET':
        return render_template('pages/Entry_Screen/templates/Entry_Screen.html')
    username = request.form['username']
    password = request.form['password']
    # check DB
    session['username'] = username
    session['logged_in'] = True
    return redirect('/')


@app.route('/New_User_Account')
def new_user_account_page():
    return render_template('New_User_Account.html')


###############################################################
# @app.route('/costomer')
# def go_to_contact():
#     return redirect(url_for('contact_page'))  # מפנה לעמוד Contact


@app.route('/index')
@app.route('/home')
@app.route('/')
def home_page():
    return render_template('index.html')




# import from DB
# first_name = ''
# last_name = 'Applebaum'
# age = 28
#
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


################################
@app.route('/fetch_page')
def fetch_page_func():
    return render_template('fetch_example.html')

@app.route('/fetch_example',methods=['GET','POST'])
def fetch_example_func():
    if request.method == 'GET':
        data= {'message': 'this is message from /fetch_example'}
        return json.dumps(data)
    elif request.method == 'POST':
        data= request.json
        # check DB  פה עושים פעולות עם הבסיס נתונים לדוגמא האם היוזר קיים/לא קיים ומחזירים תשובה
        res= {'message': 'success'}
        return json.dumps(res)
    else:
        raise RuntimeError()



@app.route('/Block_example')
def block_example_func():
    return render_template('Block_example.html')



@app.route('/contacts')
def contacts_func():
    if session['logged_in']:
        pass
        username = session['username']
        # DB
        contacts = ['ofri', 'orian']
        # print(contacts)
        return render_template('contacts.html', contacts=contacts)
    return redirect('login')


@app.route('/get_post_example', methods=['GET', 'POST'])
def get_post_example_func():
    request_method = request.method
    if request.method == 'GET':
        # GET method
        if 'first_name' in request.args:
            first_name = request.args['first_name']
            last_name = request.args['last_name']
            # check DB
            return render_template(
                'get_post_example.html',
                request_method=request_method,
                first_name=first_name,
                last_name=last_name
            )
        return render_template(
            'get_post_example.html',
            request_method=request_method
        )
    else:
        # POST method
        username = request.form['username']
        password = request.form['password']
        # check DB
        # return redirect('/')
        return render_template(
            'get_post_example.html',
            request_method=request_method,
            username=username,
            password=password
        )


@app.route('/login', methods=['GET', 'POST'])
def login_func():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    # check DB
    session['username'] = username
    session['logged_in'] = True
    return redirect('/')


@app.route('/logout')
def logout_func():
    session['username'] = None
    session['logged_in'] = False
    return redirect('/')

