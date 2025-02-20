from flask import Blueprint, render_template

# Navigation blueprint definition
Navigation = Blueprint(
    'Navigation',
    __name__, static_folder='static',
    static_url_path='/Navigation',
    template_folder='templates'
)
