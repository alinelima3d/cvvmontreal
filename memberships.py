from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, Meetings, Memberships, get_payment_status
from webforms import MembershipForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os

# area, add, update, delete, view


@app.route('/add_membership/<int:member_id>', methods=['GET', 'POST'])
def add_membership(member_id):
    date = None
    form = MembershipForm()
    if form.validate_on_submit():
        membership = Memberships.query.filter_by(member_id=member_id, start=form.start.data).first()
        # Save file name to database
        secure_filename_var = secure_filename(request.files["file"].filename)
        name = request.files["file"].filename
        unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var
        # Save Image
        request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "memberships", unique_filename))
        form.file.data = unique_filename

        if membership is None:
            membership = Memberships(start=form.start.data, end=form.end.data, remembered=form.remembered.data,
            name=name, file=form.file.data, member_id=member_id)
            db.session.add(membership)
            db.session.commit()
            flash("Membership added successfully!")

            form.start.data = ''
            form.end.data = ''
            form.remembered.data = ''

    return render_template('/memberships/add_membership.html',
        form=form)

@app.route('/update_memberships/<int:id>')
def update_memberships(id):
    member = Members.query.filter_by(id=id).first()
    first_membership = Memberships.query.filter_by(member_id=id).order_by(Memberships.end).first()
    last_membership = Memberships.query.filter_by(member_id=id).order_by(Memberships.end.desc()).first()
    memberships = Memberships.query.filter_by(member_id=id)
    payment_status = get_payment_status(last_membership)
    return render_template('/memberships/update_memberships.html',
        member=member,
        first_membership=first_membership,
        last_membership=last_membership,
        memberships=memberships,
    )

@app.route('/update_membership/<int:id>', methods=['GET', 'POST'])
def update_membership(id):
    form = MembershipForm()
    membership = Memberships.query.filter_by(id=id).first()
    member = Members.query.filter_by(id=membership.member_id).first()
    if form.validate_on_submit():
        membership.start = form.start.data
        membership.end = form.end.data
        membership.remembered = form.remembered.data
        db.session.commit()
        flash("Membership updated successfully!")
    return render_template('/memberships/update_membership.html',
        form=form,
        member=member,
        membership=membership,
    )

@app.route('/remind/<int:id>')
def remind(id):
    member = Members.query.filter_by(id=id).first()
    last_membership = Memberships.query.filter_by(member_id=id).order_by(Memberships.end.desc()).first()
    return render_template('/memberships/reminder.html',
        member=member,
        last_membership=last_membership)

# Aline - Expired - jan
# 2020-2021
# 2021-2022
# 2022-2023
# 2023-2024 feb

# Sev - Paid nov
# 2022-2023
# 2023-2024
# 2024-2025
# 2025-2026

# Member 1 - Almost Expired - remembered
# 2024-2025 - jul

# Member 2 - Almost Expired - not remembered
# 2024-2025 - jul
