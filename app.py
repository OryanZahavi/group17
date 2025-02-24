from flask import Flask, render_template

from flask import session
from flask import request
import json


app = Flask(__name__)
app.secret_key = '123'
# app.config.from_pyfile('settings.py')
#
# ##### Pages
#
## Contact_Us
from pages.Contact_Us.Contact_Us import Contact_Us
app.register_blueprint(Contact_Us)

# ## Edit_Details
from pages.Edit_Details.Edit_Details import Edit_Details
app.register_blueprint(Edit_Details)

## Entry_Screen
from pages.Entry_Screen.Entry_Screen import Entry_Screen
app.register_blueprint(Entry_Screen)
#
## Home_Page
from pages.Home_Page.Home_Page import Home_Page
app.register_blueprint(Home_Page)

## Meet_Us
from pages.Meet_Us.Meet_Us import Meet_Us
app.register_blueprint(Meet_Us)
#
## New_User_account
from pages.New_User_Account.New_User_Account import New_User_Account
app.register_blueprint(New_User_Account)


## Sunday_Schedule
from pages.Sunday_Schedule.Sunday_Schedule import Sunday_Schedule
app.register_blueprint(Sunday_Schedule)

## Monday_Schedule
from pages.Monday_Schedule.Monday_Schedule import Monday_Schedule
app.register_blueprint(Monday_Schedule)

## Tuesday_Schedule
from pages.Tuesday_Schedule.Tuesday_Schedule import Tuesday_Schedule
app.register_blueprint(Tuesday_Schedule)

## Wednesday_Schedule
from pages.Wednesday_Schedule.Wednesday_Schedule import Wednesday_Schedule
app.register_blueprint(Wednesday_Schedule)

## Thursday_Schedule
from pages.Thursday_Schedule.Thursday_Schedule import Thursday_Schedule
app.register_blueprint(Thursday_Schedule)

## Navigation
from components.Navigation.Navigation import Navigation
app.register_blueprint(Navigation)

from pages.My_Account.My_Account import My_Account
app.register_blueprint(My_Account)


from db_functions import *

#################################

import pymongo


@app.route('/mongodb')
def mongodb_func():
    message = 'good'
    return render_template('mongodb_lecture.html', message=message)














#####################################################################


# @app.route('/')
# @app.route('/Home_Page')
# def home_page():
#     return render_template('Home_Page.html')
#
#
# @app.route('/My_Account')
# def my_account_page():
#     return render_template('My_Account.html')
#
#
# @app.route('/Edit_Details')
# def edit_details_page():
#     return render_template('Edit_Details.html')
#
#
# @app.route('/Contact_Us')
# def contact_us_page():
#     return render_template('contacts.html')
#
#
# @app.route('/Meet_Us')
# def meet_us_page():
#     return render_template('Meet_Us.html')
#
#
# @app.route('/static')
# def sunday_schedule_page():
#     return render_template('static.html')
#
#
# @app.route('/Monday_Schedule')
# def monday_schedule_page():
#     return render_template('Monday_Schedule.html')
#
#
# @app.route('/Tuesday_Schedule')
# def tuesday_schedule_page():
#     return render_template('Tuesday_Schedule.html')
#
#
# @app.route('/Wednesday_Schedule')
# def wednesday_schedule_page():
#     return render_template('Wednesday_Schedule.html')
#
#
# @app.route('/Thursday_Schedule')
# def thursday_schedule_page():
#     return render_template('Thursday_Schedule.html')
#
#
# @app.route('/Entry_Screen')
# def entry_screen_page():
#     if request.method == 'GET':
#         return render_template('pages/Entry_Screen/templates/Entry_Screen.html')
#     username = request.form['username']
#     password = request.form['password']
#     # check DB
#     session['username'] = username
#     session['logged_in'] = True
#     return redirect('/')
#
#
# @app.route('/New_User_Account')
# def new_user_account_page():
#     return render_template('New_User_Account.html')


####################### in class- old ########################################
# @app.route('/costomer')
# def go_to_contact():
#     return redirect(url_for('contact_page'))  # מפנה לעמוד Contact
#
#
#
#
#
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
#
#
# ###############in class-final#################
@app.route('/index')
@app.route('/home')
@app.route('/')
def home_page():
    return render_template('index.html')
#
#
# @app.route('/fetch_page')
# def fetch_page_func():
#     return render_template('fetch_example.html')
#
# @app.route('/fetch_example',methods=['GET','POST'])
# def fetch_example_func():
#     if request.method == 'GET':
#         data= {'message': 'this is message from /fetch_example'}
#         return json.dumps(data)
#     elif request.method == 'POST':
#         data= request.json
#         # check DB  פה עושים פעולות עם הבסיס נתונים לדוגמא האם היוזר קיים/לא קיים ומחזירים תשובה
#         res= {'message': 'success'}
#         return json.dumps(res)
#     else:
#         raise RuntimeError()
#
#
#
# @app.route('/Block_example')
# def block_example_func():
#     return render_template('Block_example.html')
#
#
#
# @app.route('/contacts')
# def contacts_func():
#     if session['logged_in']:
#         pass
#         username = session['username']
#         # DB
#         contacts = ['ofri', 'orian']
#         # print(contacts)
#         return render_template('contacts.html', contacts=contacts)
#     return redirect('login')
#
#
# @app.route('/get_post_example', methods=['GET', 'POST'])
# def get_post_example_func():
#     request_method = request.method
#     if request.method == 'GET':
#         # GET method
#         if 'first_name' in request.args:
#             first_name = request.args['first_name']
#             last_name = request.args['last_name']
#             # check DB
#             return render_template(
#                 'get_post_example.html',
#                 request_method=request_method,
#                 first_name=first_name,
#                 last_name=last_name
#             )
#         return render_template(
#             'get_post_example.html',
#             request_method=request_method
#         )
#     else:
#         # POST method
#         username = request.form['username']
#         password = request.form['password']
#         # check DB
#         # return redirect('/')
#         return render_template(
#             'get_post_example.html',
#             request_method=request_method,
#             username=username,
#             password=password
#         )
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login_func():
#     if request.method == 'GET':
#         return render_template('login.html')
#     username = request.form['username']
#     password = request.form['password']
#     # check DB
#     session['username'] = username
#     session['logged_in'] = True
#     return redirect('/')
#
#
# @app.route('/logout')
# def logout_func():
#     session['username'] = None
#     session['logged_in'] = False
#     return redirect('/')
#
