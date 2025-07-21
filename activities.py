from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, Activities, save_file
from webforms import ActivityForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


@app.route('/add_activity', methods=['GET', 'POST'])
def add_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activities.query.filter_by(title=form.title.data).first()
        if activity is None:
            # Save file name to database
            secure_filename_var = secure_filename(request.files["file"].filename)
            form.filename.data = request.files["file"].filename
            unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var

            # Save File
            request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "activities", unique_filename))
            form.file.data = unique_filename

            # Save in database
            activity = Activities(
                title=form.title.data,
                text=form.text.data,
                date=form.date.data,
                hour=form.hour.data,
                address=form.address.data,
                file=form.file.data,
            )
            db.session.add(activity)
            db.session.commit()
            flash("Activity added successfully!")

            form.title.data = ''
            form.text.data = ''
            form.date.data = ''
            form.hour.data = ''
            form.address.data = ''
            form.file.data = ''
        flash("Error: An activity with this title already exists.")


    return render_template('content/add_activity.html',
        form = form,
    )


@app.route('/update_activity/<int:id>', methods=['GET', 'POST'])
def update_activity(id):
    form = ActivityForm()
    activity_to_update = Activities.query.get_or_404(id)
    if request.method == "POST":
        if request.files["file"]:
            folder = os.path.join(app.config["UPLOAD_FOLDER"], "activities")
            file = os.path.join(folder, activity_to_update.file)
            try:
                os.remove(file)
            except:
                print('Not possible to delete file ' + file)

            unique_filename = save_file(request.files["file"], "activities")

            activity_to_update.file = unique_filename
            activity_to_update.filename = request.files["file"].filename

        activity_to_update.text = request.form.get('ckeditor')
        activity_to_update.date = form.date.data
        activity_to_update.hour = form.hour.data
        activity_to_update.address = form.address.data
        activity_to_update.title = form.title.data

        try:
            db.session.commit()
            flash("Activity updated successfully!")
            return render_template("content/update_activity.html",
                form=form,
                activity_to_update=activity_to_update)
        except:
            flash("Error")
            return render_template("content/update_activity.html",
                form=form,
                activity_to_update=activity_to_update)
    else:
        return render_template("content/update_activity.html",
            form=form,
            activity_to_update=activity_to_update)


@app.route('/delete_activity/<int:id>', methods=['GET', 'POST'])
def delete_activity(id):
    activity_to_delete = Activities.query.get_or_404(id)
    form = ActivityForm()
    try:
        db.session.delete(activity_to_delete)
        db.session.commit()
        flash("Activity deleted successfully!")

        form.title.data = ''
        form.text.data = ''
        form.date.data = ''
        form.hour.data = ''
        form.address.data = ''
        form.file.data = ''

        return render_template('content/update_activity.html',
            form = form,
            activity_to_delete=activity_to_delete)
    except:
        flash("Error: Not possible to delete activity.")
        return render_template('content/update_activity.html',
            form = form,
            activity_to_delete=activity_to_delete)
