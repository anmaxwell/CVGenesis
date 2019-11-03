from cvtracker import app
from users import get_users
from flask import render_template, request, redirect, url_for

@app.route('/')
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
            #if attempted_username = 'ania':
                return redirect(url_for('menu'))
				
            else:
                error = "Invalid credentials. Try Again."

         return render_template("errorlogin.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("errorlogin.html", error = error)  

@app.route('/dataentry')
def dataentry():
    #return "Ready to enter data"
    return render_template('cventry.html')

@app.route('/menu')
def menu():
    return render_template('cvmenu.html')