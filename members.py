from flask import Flask, render_template, jsonify, flash, request

from app import app, db, Members, Meetings, Memberships
from webforms import MemberForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os

# area, add, update, delete, view

@app.route('/member_area/<int:id>')
def member_area(id):
    form = MemberForm()
    ## TODO: PEGAR ESSE ID DO APP
    current_user_id = 1
    our_members = Members.query.order_by(Members.name)
    meetings = Meetings.query.order_by(Meetings.date)
    member = Members.query.filter_by(id=id).first()
    memberships = Memberships.query.filter_by(member_id=current_user_id)
    first_membership = Memberships.query.filter_by(member_id=current_user_id).order_by(Memberships.end).first()
    last_membership = Memberships.query.filter_by(member_id=current_user_id).order_by(Memberships.end.desc()).first()
    buttons = [
        {"name": "My Info", "anchor": "myInfo"},
        {"name": "My Membership", "anchor": "myMembership"},
        {"name": "Meetings", "anchor": "meetings_list"},
        {"name": "Contact Other Members", "anchor": "member_list"},
    ]
    return render_template('members/member_area.html',
        our_members=our_members,
        executive_member=False,
        buttons=buttons,
        meetings=meetings,
        member=member,
        form=form,
        Memberships=memberships,
        first_membership=first_membership,
        last_membership=last_membership,
        deletable=False,
        title="Contact Other Members")


@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    # name = None
    form = MemberForm()
    if request.method == "POST":
        user = Members.query.filter_by(email=form.email.data).first()
        # Save file name to database
        pic_filename = secure_filename(request.files["member_pic"].filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save Image
        request.files["member_pic"].save(os.path.join(app.config["UPLOAD_FOLDER"], "member_pics", pic_name))
        form.member_pic.data = pic_name

        if user is None:
            user = Members(
            name=form.name.data,
            role=form.role.data,
            email=form.email.data,
            telephone=form.telephone.data,
            english=form.english.data,
            french=form.french.data,
            preferable=form.preferable.data,
            organization=form.organization.data,
            volunteers=form.volunteers.data,
            member_pic=form.member_pic.data,
            )
            db.session.add(user)
            db.session.commit()
            flash('Member <strong>%s</strong> added successfully!' % form.name.data)
        # name = form.name.data
        form.name.data = ''
        form.role.data = ''
        form.email.data = ''
        form.telephone.data = ''
        form.english.data = ''
        form.french.data = ''
        form.preferable.data = ''
        form.organization.data = ''
        form.volunteers.data = ''
        form.member_pic.data = ''

    our_members = Members.query.order_by(Members.name)
    return render_template('members/add_member.html',
        form = form,
        our_members=our_members)


@app.route('/update_member/<int:id>', methods=['GET', 'POST'])
def update_member(id):
    form = MemberForm()
    member_to_update = Members.query.get_or_404(id)
    if request.method == "POST":
        member_to_update.name = request.form["name"]
        member_to_update.role = request.form["role"]
        member_to_update.email = request.form["email"]
        member_to_update.telephone = request.form["telephone"]
        member_to_update.organization = request.form["organization"]
        member_to_update.volunteers = request.form["volunteers"]
        member_to_update.member_pic = request.files["member_pic"]

        # Save file name to database
        pic_filename = secure_filename(member_to_update.member_pic.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save Image
        member_to_update.member_pic.save(os.path.join(app.config["UPLOAD_FOLDER"], "member_pics", pic_name))
        member_to_update.member_pic = pic_name

        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("members/update_member.html",
                form=form,
                member_to_update=member_to_update)
        except:
            flash("Error")
            return render_template("members/update_member.html",
                form=form,
                member_to_update=member_to_update)
    else:
        return render_template("members/update_member.html",
            form=form,
            member_to_update=member_to_update)


@app.route('/delete_member/<int:id>', methods=['GET', 'POST'])
def delete_member(id):
    member_to_delete = Members.query.get_or_404(id)
    name = None
    form = MemberForm()
    try:
        db.session.delete(member_to_delete)
        db.session.commit()
        flash("Member deleted successfully!")

        name=member_to_delete.name

        our_members = Members.query.order_by(Members.name)
        return render_template('members/update_member.html',
            form = form,
            name=name,
            our_members=our_members,
            member_to_update=member_to_delete)
    except:
        flash("Error")
        our_members = Members.query.order_by(Members.name)
        return render_template('members/update_member.html',
            form = form,
            name=name,
            our_members=our_members,
            member_to_update=member_to_delete)

@app.route('/view_member/<int:id>')
def view_member(id):
    member = Members.query.get_or_404(id)
    return render_template("members/view_member.html",
        member=member)
