from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, Quotes
from webforms import QuoteForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


@app.route('/add_quote', methods=['GET', 'POST'])
def add_quote():
    form = QuoteForm()
    if form.validate_on_submit():
        quote = Quotes.query.filter_by(title=form.title.data).first()
        if quote is None:

            # Save in database
            quote = Quotes(
                title=form.title.data,
                text=form.text.data,
                author=form.author.data,
                organization=form.organization.data,
                visible=form.visible.data,
                fontSize=form.fontSize.data,
            )
            db.session.add(quote)
            db.session.commit()
            flash("Quote added successfully!")

            form.title.data = ''
            form.text.data = ''
            form.author.data = ''
            form.organization.data = ''
            form.visible.data = ''
            form.fontSize.data = ''


    return render_template('content/add_quote.html',
        form = form,
    )


@app.route('/update_quote/<int:id>', methods=['GET', 'POST'])
def update_quote(id):
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
