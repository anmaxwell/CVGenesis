from cvtracker import app
from cvtracker.models import CV, Hirer, Role
from users import get_users
from flask import render_template, request, redirect, url_for

@app.route('/')
@app.route('/home')
def index():
    return render_template('login.html')

@app.route('/login', methods=["GET","POST"])
def login_page():

    error = ''
    valid_user = get_users()

    try:
         if request.method == "POST":
            attempted_username = request.form['username']

            if attempted_username in valid_user:
                return redirect(url_for('menu'))				
            else:
                error = "Invalid credentials. Try Again."

         return render_template("errorlogin.html", error = error)

    except Exception:
        return render_template("errorlogin.html", error = error)  

@app.route('/cventry')
def cv_entry():
   return render_template('cventry.html')

@app.route('/cvedit')
def cv_edit():
   return render_template('cvedit.html')
    
@app.route('/mgrlist')
def mgr_list():
   return render_template('mgrlist.html')