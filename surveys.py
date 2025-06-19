from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, Meetings, Memberships, Surveys
from webforms import SurveyForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os
#  add, update, delete


# SURVEY FORM/DATABASE ----------------------------------------------------
@app.route('/add_survey', methods=['GET', 'POST'])
def add_survey():
    title = None
    form = SurveyForm()
    if form.validate_on_submit():
        survey = Surveys.query.filter_by(title=form.title.data).first()
        # Save file name to database
        secure_filename_var = secure_filename(request.files["file"].filename)
        # form.minute.data = request.files["file"].filename
        unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var
        # Save Image
        request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "surveys", unique_filename))
        form.file.data = unique_filename

        if survey is None:
            survey = Surveys(title=form.title.data, start=form.start.data,
            end=form.end.data, responders=form.responders.data,
            file=form.file.data)
            db.session.add(survey)
            db.session.commit()
            flash("Survey added successfully!")

            title = form.title.data
            form.title.data = ''
            form.start.data = ''
            form.end.data = ''

    return render_template('surveys/add_survey.html',
        form = form,
        title=title,
        )

@app.route('/update_survey/<int:id>', methods=['GET', 'POST'])
def update_survey(id):
    form = SurveyForm()
    title = None
    survey_to_update = Surveys.query.get_or_404(id)
    if request.method == "POST":
        survey_to_update.title = request.form["title"]
        survey_to_update.start = request.form["start"]
        survey_to_update.end = request.form["end"]
        survey_to_update.responders = request.form["responders"]

        # Save file name to database
        secure_filename_var = secure_filename(request.files["file"].filename)
        unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var
        # Save Image
        request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "meetings", unique_filename))
        form.file.data = unique_filename
        survey_to_update.file = unique_filename


        try:
            db.session.commit()
            flash("Meeting updated successfully!")
            return render_template("surveys/update_survey.html",
                form=form,
                survey_to_update=survey_to_update)
        except:
            flash("Error")
            return render_template("surveys/update_survey.html",
                form=form,
                survey_to_update=survey_to_update)
    else:
        return render_template("surveys/update_survey.html",
            form=form,
            survey_to_update=survey_to_update)

@app.route('/delete_survey/<int:id>', methods=['GET', 'POST'])
def delete_survey(id):
    survey_to_delete = Surveys.query.get_or_404(id)
    title = None
    form = SurveyForm()
    try:
        db.session.delete(survey_to_delete)
        db.session.commit()
        flash("Survey deleted successfully!")

        title=survey_to_delete.title

        return render_template('surveys/update_survey.html',
            form = form,
            title=title,
            survey_to_update=survey_to_delete)
    except:
        flash("Error")
        return render_template('surveys/update_survey.html',
            form = form,
            title=title,
            survey_to_update=survey_to_delete)
