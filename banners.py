from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, Banners
from webforms import BannerForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


@app.route('/add_banner', methods=['GET', 'POST'])
def add_banner():
    form = BannerForm()
    if form.validate_on_submit():
        banner = Banners.query.filter_by(filename=form.filename.data).first()
        if banner is None:
            # If visible uncheck others
            if form.visible.data == True:
                banners = Banners.query.filter_by(visible=True)
                for banner in banners:
                    banner.visible = False
                    db.session.commit()
                    
            # Save file name to database
            secure_filename_var = secure_filename(request.files["file"].filename)
            form.filename.data = request.files["file"].filename
            unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var

            # Save File
            request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "banners", unique_filename))
            form.file.data = unique_filename



            # Save in database
            banner = Banners(
                filename=form.filename.data,
                file=form.file.data,
                visible=form.visible.data,
            )
            db.session.add(banner)
            db.session.commit()
            flash("Banner added successfully!")

            form.filename.data = ''
            form.file.data = ''
            form.visible.data = ''


    return render_template('content/add_banner.html',
        form = form,
    )


@app.route('/update_banner/<int:id>', methods=['GET', 'POST'])
def update_banner(id):
    form = MeetingForm()
    date = None
    meeting_to_update = Meetings.query.get_or_404(id)
    if request.method == "POST":
        meeting_to_update.date = request.form["date"]

        meeting_to_update.attendees = request.form["attendees"]

        # Save file name to database
        secure_filename_var = secure_filename(request.files["file"].filename)
        form.minute.data = request.files["file"].filename
        unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var
        # Save Image
        request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "meetings", unique_filename))
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
