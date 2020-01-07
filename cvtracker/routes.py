from cvtracker import app, db, bcrypt
from cvtracker.models import CV, Hirer, Role, Source, Cvstatus, Rolestatus, Statuschange, User
from cvtracker.forms import MgrEntry, RoleEntry, CVEntry, SourceEntry, CVStatus, RoleStatus, LoginForm
from users import get_users
from flask import render_template, request, redirect, url_for, flash, json
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, distinct 
import urllib.parse


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def index():
    cvcount = db.session.query(CV.cvstatus_id, Cvstatus.name, func.count(CV.cvstatus_id)).group_by(CV.cvstatus_id).join(Cvstatus).all()
    cvchartdata = {'labels': [], 'data': []}
    for item in cvcount:
        cvchartdata['labels'].append(item[1])
        cvchartdata['data'].append(item[2])
    convcvcount = json.dumps(cvchartdata)

    rolecount = db.session.query(Role.rolestatus_id, Rolestatus.name, func.count(Role.rolestatus_id)).group_by(Role.rolestatus_id).join(Rolestatus).all()
    rolechartdata = {'labels': [], 'data': []}
    for item in rolecount:
        rolechartdata['labels'].append(item[1])
        rolechartdata['data'].append(item[2])
    convrolecount = json.dumps(rolechartdata)
    return render_template('home.html', convcvcount=convcvcount, convrolecount=convrolecount)

@app.route('/cvlist')
@login_required
def cv_list():
    if request.args:
        args = request.args.get('role')
        cvs = CV.query.order_by(CV.reference).filter_by(role_id=args)
    else:
        cvs = CV.query.order_by(CV.reference)
    return render_template('cvlist.html', cvs=cvs)

@app.route("/cvhistory/<int:cv_id>")
@login_required
def cv_history(cv_id):
    cvs = Statuschange.query.order_by(Statuschange.id).filter_by(cv_id=cv_id).all()
    cvlist = []
    for item in cvs:
        cvlist.append({'date':item.date_changed, 'statusfrom':item.statuschange.name, 'statusto':None})

    idx = 0
    for row in cvlist:
        while idx < len(cvlist)-1:
            cvlist[idx]["statusto"] = cvlist[idx+1]["statusfrom"]
            idx += 1
 
    cvlist[idx]["statusto"] = db.session.query(CV).get(cv_id).cvstatus.name

    cv_query = db.session.query(CV.reference, CV.date_entered).filter_by(id=cv_id).first()
    cv_ref = cv_query[0]
    cv_date = cv_query[1]
    return render_template('cvhistory.html', cvs=cvs, cv_ref=cv_ref, cv_date=cv_date, cvlist=cvlist)

@app.route('/cventry', methods=['GET', 'POST'])
@login_required
def cv_entry():

    form = CVEntry()
    form.role.choices = [(role.id, role.title) for role in Role.query.order_by(Role.title).all()]
    form.source.choices = [(source.id, source.name) for source in Source.query.order_by(Source.name).all()]
    form.cvstatus.choices = [(cvstatus.id, cvstatus.name) for cvstatus in Cvstatus.query.order_by(Cvstatus.name).all()]
    if form.validate_on_submit():
        cv = CV(reference=form.reference.data, cvstatus_id=form.cvstatus.data, cv_notes=form.cvnotes.data, date_entered=form.date_entered.data,
                        role_id=form.role.data, source_id=form.source.data)
        db.session.add(cv)
        db.session.commit()
        flash("Successfully Added", 'success')
        return redirect(url_for('cv_entry'))
    return render_template('cventry.html', form=form, legend='Add new CV')


@app.route("/cvedit/<int:cv_id>/update", methods=['GET', 'POST'])
@login_required
def cv_edit(cv_id):

    cvedit=CV.query.get(cv_id)

    form = CVEntry()
    form.role.choices = [(role.id, role.title) for role in Role.query.all()]
    form.source.choices = [(source.id, source.name) for source in Source.query.order_by(Source.name).all()]
    form.cvstatus.choices = [(cvstatus.id, cvstatus.name) for cvstatus in Cvstatus.query.order_by(Cvstatus.name).all()]
    if form.validate_on_submit():

        if cvedit.cvstatus_id != form.cvstatus.data:

            cvchange = Statuschange(status_id=cvedit.cvstatus_id, cv_id=cv_id)
            db.session.add(cvchange)

        cvedit.reference = form.reference.data
        cvedit.cv_notes = form.cvnotes.data
        cvedit.cvstatus_id = form.cvstatus.data
        cvedit.date_entered = form.date_entered.data
        cvedit.role_id = form.role.data
        cvedit.source_id = form.source.data

        db.session.commit()
        flash("Successfully Updated", 'success')
        return redirect(url_for('cv_list'))

    elif request.method == 'GET':
        form.reference.data = cvedit.reference
        form.cvnotes.data = cvedit.cv_notes
        form.date_entered.data = cvedit.date_entered
        form.role.data = cvedit.role_id
        form.source.data = cvedit.source_id
        form.role.data = cvedit.role_id
        form.cvstatus.data = cvedit.cvstatus_id

    return render_template('cventry.html',form=form, legend='Update CV')
    
@app.route('/mgrlist')
@login_required
def mgr_list():
    mgrs = Hirer.query.order_by(Hirer.status)
    return render_template('mgrlist.html', mgrs=mgrs)

@app.route('/mgrentry', methods=['GET', 'POST'])
@login_required
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
@login_required
def role_list():
    roles = Role.query.order_by(Role.title)
    return render_template('rolelist.html', roles=roles)

@app.route('/roleentry', methods=['GET', 'POST'])
@login_required
def role_entry():

    form = RoleEntry()
    form.manager.choices = [(hirer.id, hirer.name) for hirer in Hirer.query.order_by(Hirer.name).all()]
    form.rolestatus.choices = [(rolestatus.id, rolestatus.name) for rolestatus in Rolestatus.query.order_by(Rolestatus.name).all()]
    if form.validate_on_submit():
        role = Role(title=form.title.data, rolestatus_id=form.rolestatus.data, role_notes=form.notes.data, date_opened=form.date_opened.data,
                        mgr_id=form.manager.data)
        db.session.add(role)
        db.session.commit()
        flash("Successfully Added", 'success')
        return redirect(url_for('role_entry'))
    return render_template('roleentry.html', form=form, legend='Add new role')

@app.route("/roleedit/<int:role_id>/update", methods=['GET', 'POST'])
@login_required
def role_edit(role_id):

    roleedit=Role.query.get(role_id)

    form = RoleEntry()
    form.manager.choices = [(hirer.id, hirer.name) for hirer in Hirer.query.all()]
    form.rolestatus.choices = [(rolestatus.id, rolestatus.name) for rolestatus in Rolestatus.query.order_by(Rolestatus.name).all()]
    if form.validate_on_submit():
        mgrname = form.manager.data
        roleedit.title = form.title.data
        roleedit.rolestatus_id = form.rolestatus.data
        roleedit.role_notes = form.notes.data
        roleedit.date_opened = form.date_opened.data
        roleedit.mgr_id = mgrname
        db.session.commit()
        flash("Successfully Updated", 'success')
        return redirect(url_for('role_list'))

    elif request.method == 'GET':
        form.title.data = roleedit.title
        form.notes.data = roleedit.role_notes
        form.rolestatus.data = roleedit.rolestatus_id
        form.date_opened.data = roleedit.date_opened
        form.manager.data = roleedit.mgr_id

    return render_template('roleentry.html',form=form, legend='Update role')

@app.route('/addsource', methods=['GET', 'POST'])
@login_required
def add_source():

    sources = Source.query.order_by(Source.name)
    form = SourceEntry()
    if form.validate_on_submit():
        sourcename = Source(name=form.name.data)
        db.session.add(sourcename)
        db.session.commit()
        flash("Successfully Added", 'success')
        return redirect(url_for('add_source'))
    return render_template('sourceentry.html', form=form, sources=sources)

@app.route('/cvstatus', methods=['GET', 'POST'])
@login_required
def cv_status():

    statuses = Cvstatus.query.order_by(Cvstatus.name)
    form = CVStatus()
    if form.validate_on_submit():
        statusname = Cvstatus(name=form.name.data)
        db.session.add(statusname)
        db.session.commit()
        flash("Successfully Added", 'success')
        return redirect(url_for('cv_status'))
    return render_template('cvstatus.html', form=form, statuses=statuses)

@app.route('/rolestatus', methods=['GET', 'POST'])
@login_required
def role_status():

    statuses = Rolestatus.query.order_by(Rolestatus.name)
    form = RoleStatus()
    if form.validate_on_submit():
        statusname = Rolestatus(name=form.name.data)
        db.session.add(statusname)
        db.session.commit()
        flash("Successfully Added", 'success')
        return redirect(url_for('role_status'))
    return render_template('rolestatus.html', form=form, statuses=statuses)


@app.route('/cvquery')
@login_required
def cvquery():

    idname = urllib.parse.unquote(request.args.get('id'))
    idval =  db.session.query(Cvstatus.id).filter_by(name=idname).all()
    cvquery = CV.query.order_by(CV.reference).filter_by(cvstatus_id=idval[0][0])

    return render_template('cvquery.html', cvquery=cvquery, idval=idval)


@app.route('/rolequery')
@login_required
def rolequery():

    idname = urllib.parse.unquote(request.args.get('id'))
    idval = db.session.query(Rolestatus.id).filter_by(name=idname).all()
    rolequery = Role.query.order_by(Role.title).filter_by(rolestatus_id=idval[0][0])

    return render_template('rolequery.html', rolequery=rolequery)

