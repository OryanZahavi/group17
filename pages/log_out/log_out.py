from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db_functions import get_user_by_email, user_exists  # וודאי שהפונקציה מיובאת נכון

# יצירת ה-Blueprint
log_out = Blueprint('log_out', __name__,
                         static_folder='static',
                         static_url_path='/log_out',
                         template_folder='templates')
@log_out.route('/log_out')
def log_out_func():
    session['email'] = None
    session['logged_in'] = False
    return render_template('Entry_Screen.html')