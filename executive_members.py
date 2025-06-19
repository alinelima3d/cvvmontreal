from flask import Flask, render_template, jsonify, flash, request

from app import app, db, Members, ExecutiveMembers, Meetings, Memberships, Surveys, get_payment_status
from webforms import ExecutiveMemberForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os

# area, add, update, delete

@app.route('/executive_member_area/<int:id>')
def executive_member_area(id):
    our_executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.name)
    our_members = Members.query.order_by(Members.name)
    form = ExecutiveMemberForm()
    executive_member = ExecutiveMembers.query.filter_by(id=id).first()
    surveys = Surveys.query.order_by(Surveys.title)
    meetings = Meetings.query.order_by(Meetings.date.desc())
    member_payments = []
    for member in our_members:

        memberships = Memberships.query.filter_by(id=member.id).order_by(Memberships.start)
        first_membership = Memberships.query.filter_by(member_id=member.id).order_by(Memberships.end).first()
        last_membership = Memberships.query.filter_by(member_id=member.id).order_by(Memberships.end.desc()).first()
        payment_status = get_payment_status(last_membership)
        member_since = ""
        if first_membership:
            member_since = first_membership.start
        member_payment = {
            'id': member.id,
            'name': member.name,
            'role': member.role,
            'organization': member.organization,
            'status': payment_status['status'],
            'warning_icon': payment_status['warning_icon'],
            'remembered': payment_status['remembered'],
            'member_since': member_since,
            'expiration_date': payment_status['expiration_date'],
            'member_pic': member.member_pic,
        }
        member_payment['memberships'] = memberships
        member_payments.append(member_payment)
    buttons = [
        {"name": "My Info", "anchor": "myInfo"},
        {"name": "Task Repartition", "anchor": "taskRepartition"},
        {"name": "Payment Status", "anchor": "paymentList"},
        {"name": "Member Attendance", "anchor": "attendanceList"},
        {"name": "Surveys", "anchor": "surveysList"},
        {"name": "Meetings", "anchor": "meetings_list"},
        {"name": "Executive Members", "anchor": "executive_member_list"},
        {"name": "Members", "anchor": "member_list"},
    ]
    return render_template('executive_members/executive_member_area.html',
        our_members=our_members,
        our_executive_members=our_executive_members,
        is_executive_member=True,
        buttons=buttons,
        surveys=surveys,
        meetings=meetings,
        title="Members",
        executive_member=executive_member,
        member_payments=member_payments,
        deletable=True,
        form=form)

@app.route('/add_executive_member', methods=['GET', 'POST'])
def add_executive_member():
    name = None
    form = ExecutiveMemberForm()
    if form.validate_on_submit():
        user = ExecutiveMembers.query.filter_by(email=form.email.data).first()
        # Save file name to database

        if user is None:
            if request.files["executive_member_pic"].filename:
                pic_filename = secure_filename(request.files["executive_member_pic"].filename)
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                # Save Image
                request.files["executive_member_pic"].save(os.path.join(app.config["UPLOAD_FOLDER"], "executive_member_pics", pic_name))
            executiveMember = ExecutiveMembers(
                name=form.name.data,
                email=form.email.data,
                # english=form.english.data,
                # french=form.french.data,
                role=form.role.data,
                order=form.order.data,
                telephone=form.telephone.data,
                organization=form.organization.data,
                executive_member_pic=pic_name,
                )
            db.session.add(executiveMember)
            db.session.commit()
            flash('Executive Member <strong>%s</strong> added successfully!' % form.name.data)

        name = form.name.data
        form.name.data = ''
        form.email.data = ''

    our_executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.name)
    return render_template('executive_members/add_executive_member.html',
        form = form,
        name=name,
        our_executive_members=our_executive_members)

@app.route('/update_executive_member/<int:id>', methods=['GET', 'POST'])
def update_executive_member(id):
    form = ExecutiveMemberForm()
    executive_member_to_update = ExecutiveMembers.query.get_or_404(id)
    if request.method == "POST":
        executive_member_to_update.name = request.form["name"]
        executive_member_to_update.role = request.form["role"]
        executive_member_to_update.bio = request.form["bio"]
        executive_member_to_update.email = request.form["email"]
        executive_member_to_update.telephone = request.form["telephone"]
        executive_member_to_update.order = request.form["order"]
        executive_member_to_update.organization = request.form["organization"]

        executive_member_to_update.executive_member_pic = request.files["executive_member_pic"]

        # Save file name to database
        if request.files["executive_member_pic"]:
            pic_filename = secure_filename(executive_member_to_update.executive_member_pic.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save Image
            executive_member_to_update.executive_member_pic.save(os.path.join(app.config["UPLOAD_FOLDER"], "executive_member_pics", pic_name))
            executive_member_to_update.executive_member_pic = pic_name

        try:
            db.session.commit()
            flash('Executive Member <strong>%s</strong> updated successfully!' % executive_member_to_update.name)
            return render_template("executive_members/update_executive_member.html",
                form=form,
                executive_member_to_update=executive_member_to_update,
                deletable=True)
        except:
            flash("Error")
            return render_template("executive_members/update_executive_member.html",
                form=form,
                executive_member_to_update=executive_member_to_update,
                deletable=True)
    else:
        return render_template("executive_members/update_executive_member.html",
            form=form,
            executive_member_to_update=executive_member_to_update,
            deletable=True)

@app.route('/delete_executive_member/<int:id>', methods=['GET', 'POST'])
def delete_executive_member(id):
    executive_member_to_delete = ExecutiveMembers.query.get_or_404(id)
    name = None
    form = ExecutiveMemberForm()
    try:
        db.session.delete(executive_member_to_delete)
        db.session.commit()
        flash('Executive Member <strong>%s</strong> deleted successfully!' % executive_member_to_delete.name)

        name=executive_member_to_delete.name

        return render_template('executive_members/update_executive_member.html',
            form = form,
            name=name,
            executive_member_to_update=executive_member_to_delete)
    except:
        return render_template('executive_members/update_executive_member.html',
            form = form,
            name=name,
            executive_member_to_update=executive_member_to_delete)


@app.route('/content_management')
def content_management():
    return render_template('executive_members/content_management.html')
