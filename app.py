from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # לתמיכה בעברית
app.secret_key = '123'


## Contact_Us
from pages.Contact_Us.Contact_Us import Contact_Us
app.register_blueprint(Contact_Us)

## Edit_Details
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

from pages.log_out.log_out import log_out
app.register_blueprint(log_out)

from pages.Edit_Password.Edit_Password import Edit_Password
app.register_blueprint(Edit_Password)


import os

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
