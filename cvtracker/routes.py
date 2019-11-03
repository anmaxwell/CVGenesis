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

                return redirect(url_for('menu'))
				
            else:
                error = "Invalid credentials. Try Again."

         return render_template("errorlogin.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("errorlogin.html", error = error)  

@app.route('/menu', methods=["GET","POST"])
def menu():

    if request.method == "POST":

        selected = request.form.to_dict()

        if "create" in selected:
            print("success create")
            return redirect(url_for('dataentry'))


        if "update" in selected:
            print("success update")
            return redirect(url_for('dataedit'))

		
    else:
        return render_template('cvmenu.html')


@app.route('/dataentry')
def dataentry():
   return render_template('cventry.html')


@app.route('/dataedit')
def dataedit():
   return render_template('cvedit.html')
    