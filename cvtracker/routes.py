from cvtracker import app, db
from cvtracker.models import CV, Hirer, Role
from cvtracker.forms import MgrEntry, RoleEntry
from users import get_users
from flask import render_template, request, redirect, url_for, flash

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

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

@app.route('/cvlist')
def cv_list():
    cvs = CV.query.order_by(CV.reference)
    return render_template('cvlist.html', cvs=cvs)

@app.route('/cventry')
def cv_entry():
   return render_template('cventry.html')

@app.route('/cvedit')
def cv_edit():
   return render_template('cvedit.html')
    
@app.route('/mgrlist')
def mgr_list():
    mgrs = Hirer.query.order_by(Hirer.status)
    return render_template('mgrlist.html', mgrs=mgrs)

@app.route('/mgrentry', methods=['GET', 'POST'])
def mgr_entry():

    form = MgrEntry()
    if form.validate_on_submit():
        mgr = Hirer(name=form.name.data, status='active')
        db.session.add(mgr)
        db.session.commit()
        flash("Successfully Added", 'success')
        return redirect(url_for('mgr_entry'))
    return render_template('mgrentry.html', form=form)

@app.route('/rolelist')
def role_list():
    roles = Role.query.order_by(Role.status)
    return render_template('rolelist.html', roles=roles)

@app.route('/roleentry', methods=['GET', 'POST'])
def role_entry():

    form = RoleEntry()
    form.manager.choices = [(hirer.id, hirer.name) for hirer in Hirer.query.all()]
    if form.validate_on_submit():
        mgrname = form.manager.data
        mgrid = Hirer.query.filter_by(name=mgrname).first()
        #mgrid = 3
        role = Role(title=form.title.data, status='active', role_notes=form.notes.data, date_opened=form.date_opened.data,
                        mgr_id=mgrname)
        db.session.add(role)
        db.session.commit()
        flash("Successfully Added", 'success')
        return redirect(url_for('role_entry'))
    return render_template('roleentry.html', form=form)