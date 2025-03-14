from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_functions import authenticate_user, user_exists

# יצירת ה-Blueprint
Entry_Screen = Blueprint('Entry_Screen', __name__,
                         static_folder='static',
                         static_url_path='/Entry_Screen',
                         template_folder='templates')

@Entry_Screen.route('/Entry_Screen', methods=['GET', 'POST'])
def entry_screen():
    if request.method == 'POST':
        email = request.form.get("user_Email")  # קבלת האימייל מהטופס
        password = request.form.get("user_Password")  # קבלת הסיסמה מהטופס
        user = authenticate_user(email, password)  # בדיקת התחברות
        if user :
            # שמירת המשתמש ב-Session
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['first_name']
            session['email'] = user['email']
            session['logged_in'] = True

            flash("התחברת בהצלחה!", "success")  # הודעה למשתמש
            return redirect(url_for('Home_Page.index'))  # העברה לדף הבית

        flash("שם משתמש או סיסמה שגויים", "error")  # הודעת שגיאה
        return redirect(url_for('Entry_Screen.Entry_Screen'))

    return render_template('Entry_Screen.html')


#
# # Ensure you have a logout route to clear the session
# @Entry.route('/logout')
# def logout():
#     session.pop('user_email', None)
#     return redirect(url_for('Entry.index'))
