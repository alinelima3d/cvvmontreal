from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, News
from webforms import NewsForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News.query.filter_by(title=form.title.data).first()
        if news is None:
            # Save file name to database
            secure_filename_var = secure_filename(request.files["file"].filename)
            form.filename.data = request.files["file"].filename
            unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var

            # Save File
            request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "news", unique_filename))
            form.file.data = unique_filename

            # Save in database
            news = News(
                title=form.title.data,
                text=form.text.data,
                date=form.date.data,
                file=form.file.data,
                type=form.type.data,
                likes=0,
            )
            db.session.add(news)
            db.session.commit()
            flash("News added successfully!")

            form.title.data = ''
            form.text.data = ''
            form.date.data = ''
            form.file.data = ''
            form.type.data = ''


    return render_template('content/add_news.html',
        form = form,
    )


@app.route('/update_news/<int:id>', methods=['GET', 'POST'])
def update_news(id):
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


@app.route('/news/<int:id>', methods=['GET', 'POST'])
def view_news(id):
    comments = []
    comments.append({'member_id': 1, 'pic': 'ee647976-4d3b-11f0-9790-7cb566a2ae99_11.jpg', 'name': 'Aline Lima', 'time': '2025-07-01 15:03', 'text': 'Amazing news. Thank you for sharing.' })
    comments.append({'member_id': 2, 'pic': 'ae2a1f28-4d3b-11f0-95a6-7cb566a2ae99_12.jpg', 'name': 'Sev Rovera','time': '2025-07-03 10:20', 'text': 'This is a fantastic overview of how volunteerism is evolving globally! Its especially encouraging to see the rise of virtual volunteering and corporate involvement, making it easier for more people to contribute. The focus on flexibility and DEI is also key to ensuring volunteer efforts are inclusive and far-reaching.' })
    comments.append({'member_id': 3, 'pic': '4126c020-4d3f-11f0-b592-7cb566a2ae99_Gemini_Generated_Image_6hodoi6hodoi6hod.png', 'name': 'George Digger','time': '2025-07-08 08:14', 'text': 'This is a really insightful article, Aline! Its great to see how volunteerism is adapting and thriving with new trends like virtual engagement and corporate programs. The emphasis on flexibility and DEI is particularly encouraging for the future of global giving.' })
    comments.append({'member_id': 4, 'pic': '3ab582af-4d3f-11f0-b45c-7cb566a2ae99_daisy.jpg', 'name': 'Daisy Digger','time': '2025-07-10 20:08', 'text': 'Amazing news. Thank you for sharing.' })
    comments.append({'member_id': 1, 'pic': 'ee647976-4d3b-11f0-9790-7cb566a2ae99_11.jpg', 'name': 'Aline Lima','time': '2025-07-12 22:09', 'text': 'Amazing news. Thank you for sharing.' })
    comments.append({'member_id': 2, 'pic': 'ae2a1f28-4d3b-11f0-95a6-7cb566a2ae99_12.jpg', 'name': 'Sev Rovera','time': '2025-07-12 15:18', 'text': 'Amazing news. Thank you for sharing.' })
    news = News.query.filter_by(id=id).first()
    return render_template('content/view_news.html',
        news=news,
        comments=comments,
    )
