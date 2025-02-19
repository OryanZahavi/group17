from flask import Blueprint, render_template
# about Blueprint definition
Meet_Us = Blueprint(
    'Meet_Us',
    __name__,
    static_folder='static',
    static_url_path='/Meet_Us',
    template_folder='templates'
)

# Routs
@Meet_Us.route('/Meet_Us')
def meet_us():
    return render_template('Meet_Us.html')