from cvtracker import app
from flask import render_template, request, redirect, url_for

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=["GET","POST"])
def login_page():

    error = ''
    try:
         if request.method == "POST":
		
            attempted_username = request.form['username']

            #flash(attempted_username)

            if attempted_username == "ania":
                #return "Hurray"
                return redirect(url_for('dataentry'))
				
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