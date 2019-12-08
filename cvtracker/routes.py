from cvtracker import app, db
from cvtracker.models import CV, Hirer, Role
from cvtracker.forms import MgrEntry, RoleEntry, CVEntry
from users import get_users
from flask import render_template, request, redirect, url_for, flash

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/cvlist')
def cv_list():
    cvs = CV.query.order_by(CV.reference)
    return render_template('cvlist.html', cvs=cvs)

@app.route('/cventry', methods=['GET', 'POST'])
def cv_entry():

    form = CVEntry()
    form.role.choices = [(role.id, role.title) for role in Role.query.all()]
    if form.validate_on_submit():
        roletitle = form.role.data
        cv = CV(reference=form.reference.data, status='active', cv_notes=form.cvnotes.data, date_entered=form.date_entered.data,
                        role_id=roletitle)
        db.session.add(cv)
        db.session.commit()
        flash("Successfully Added", 'success')
        return redirect(url_for('cv_entry'))
    return render_template('cventry.html', form=form, legend='Add new CV')


@app.route("/cvedit/<int:cv_id>/update", methods=['GET', 'POST'])
def cv_edit(cv_id):

    cvedit=CV.query.get(cv_id)

    form = CVEntry()
    form.role.choices = [(role.id, role.title) for role in Role.query.all()]
    if form.validate_on_submit():
        roletitle = form.role.data
        cvedit.reference = form.reference.data
        cvedit.status = 'active'
        cvedit.cv_notes = form.cvnotes.data
        cvedit.date_entered = form.date_entered.data
        cvedit.role_id = roletitle
        db.session.commit()
        flash("Successfully Updated", 'success')
        return redirect(url_for('cv_list'))

    elif request.method == 'GET':
        form.reference.data = cvedit.reference
        form.cvnotes.data = cvedit.cv_notes
        form.date_entered.data = cvedit.date_entered
        form.role.data = cvedit.role_id

    return render_template('cventry.html',form=form, legend='Update CV')
    
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
        role = Role(title=form.title.data, status='active', role_notes=form.notes.data, date_opened=form.date_opened.data,
                        mgr_id=mgrname)
        db.session.add(role)
        db.session.commit()
        flash("Successfully Added", 'success')
        return redirect(url_for('role_entry'))
    return render_template('roleentry.html', form=form, legend='Add new role')

@app.route("/roleedit/<int:role_id>/update", methods=['GET', 'POST'])
def role_edit(role_id):

    roleedit=Role.query.get(role_id)

    form = RoleEntry()
    form.manager.choices = [(hirer.id, hirer.name) for hirer in Hirer.query.all()]
    if form.validate_on_submit():
        mgrname = form.manager.data
        roleedit.title = form.title.data
        roleedit.status = 'active'
        roleedit.role_notes = form.notes.data
        roleedit.date_opened = form.date_opened.data
        roleedit.mgr_id = mgrname
        db.session.commit()
        flash("Successfully Updated", 'success')
        return redirect(url_for('role_list'))

    elif request.method == 'GET':
        form.title.data = roleedit.title
        form.notes.data = roleedit.role_notes
        form.date_opened.data = roleedit.date_opened
        form.manager.data = roleedit.mgr_id

    return render_template('roleentry.html',form=form, legend='Update role')

@app.route('/addsource')
def add_source():
    roles = Role.query.order_by(Role.status)
    return render_template('rolelist.html')

@app.route('/cvstatus')
def cv_status():
    cvs = CV.query.order_by(CV.reference)
    return render_template('cvstatus.html', cvs=cvs)

@app.route('/rolestatus')
def role_status():
    roles = Role.query.order_by(Role.status)
    return render_template('rolestatus.html', roles=roles)