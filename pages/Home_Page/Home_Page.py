from flask import Blueprint, render_template, request, redirect, url_for

# about Blueprint definition
Home_Page = Blueprint(
    'Home_Page',
    __name__,
    static_folder='static',
    static_url_path='/Home_Page',
    template_folder='templates'
)

# Routs
@Home_Page.route('/Home_Page')
def index():
    return render_template('Home_Page.html')