from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, Meetings, Memberships
from webforms import MeetingForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


#  add, update, delete


@app.route('/add_meeting', methods=['GET', 'POST'])
def add_meeting():
    date = None
    form = MeetingForm()
    if form.validate_on_submit():
        meeting = Meetings.query.filter_by(date=form.date.data).first()
        # Save file name to database
        secure_filename_var = secure_filename(request.files["file"].filename)
        form.minute.data = request.files["file"].filename
        unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var
        # Save Image
        unique_filename = save_file(form.file.data, "docs/meetings/")
        # app.config['S3'].upload_fileobj(form.file.data, "cvvmontreal", ("docs/meetings/" + unique_filename))
        # request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "meetings", unique_filename))
        form.file.data = unique_filename

        if meeting is None:
            meeting = Meetings(date=form.date.data, minute=form.minute.data,
            attendees=form.attendees.data, file=form.file.data)
            db.session.add(meeting)
            db.session.commit()
            flash("Meeting added successfully!")

            date = form.date.data
            form.date.data = ''
            form.minute.data = ''
            form.attendees.data = ''


    return render_template('meetings/add_meeting.html',
        form = form,
        date=date,
        )

@app.route('/update_meeting/<int:id>', methods=['GET', 'POST'])
def update_meeting(id):
    form = MeetingForm()
    date = None
    meeting_to_update = Meetings.query.get_or_404(id)
    if request.method == "POST":
        meeting_to_update.date = request.form["date"]

        meeting_to_update.attendees = request.form["attendees"]

        # Save file name to database
        # secure_filename_var = secure_filename(request.files["file"].filename)
        form.minute.data = request.files["file"].filename
        # unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var
        # Save Image
        # request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "meetings", unique_filename))
        # s3_client.upload_fileobj(form.file.data, "cvvmontreal", ("docs/meetings/" + unique_filename))
        unique_filename = save_file(form.file.data, "docs/meetings/")
        form.file.data = unique_filename
        meeting_to_update.minute = request.files["file"].filename
        meeting_to_update.file = unique_filename

        try:
            db.session.commit()
            flash("Meeting updated successfully!")
            form.date.data = ''
            form.minute.data = ''
            form.attendees.data = ''
            return render_template("meetings/update_meeting.html",
                form=form,
                meeting_to_update=meeting_to_update)
        except:
            flash("Error")
            return render_template("meetings/update_meeting.html",
                form=form,
                meeting_to_update=meeting_to_update)
    else:
        return render_template("meetings/update_meeting.html",
            form=form,
            meeting_to_update=meeting_to_update)

@app.route('/delete_meeting/<int:id>', methods=['GET', 'POST'])
def delete_meeting(id):
    meeting_to_delete = Meetings.query.get_or_404(id)
    date = None
    form = MeetingForm()
    try:
        db.session.delete(meeting_to_delete)
        db.session.commit()
        flash("Meeting deleted successfully!")

        date=meeting_to_delete.date
        form.date.data = ''
        form.minute.data = ''
        form.attendees.data = ''

        return render_template('meetings/update_meeting.html',
            form = form,
            date=date,
            meeting_to_update=meeting_to_delete)
    except:
        flash("Error")
        return render_template('meetings/update_meeting.html',
            form = form,
            date=date,
            meeting_to_update=meeting_to_delete)
