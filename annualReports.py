from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, AnnualReports, save_file
from webforms import AnnualReportForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os


@app.route('/add_annualReport', methods=['GET', 'POST'])
def add_annualReport():
    form = AnnualReportForm()
    if form.validate_on_submit():
        annualReport = AnnualReports.query.filter_by(filename=form.filename.data).first()
        if annualReport is None:
            # Save file name to database
            secure_filename_var = secure_filename(request.files["file"].filename)
            form.filename.data = request.files["file"].filename
            unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var

            # Save File
            request.files["file"].save(os.path.join(app.config["UPLOAD_FOLDER"], "annualReports", unique_filename))
            form.file.data = unique_filename

            # Save in database
            annualReport = AnnualReports(
                filename=form.filename.data,
                file=form.file.data,
                visible=form.visible.data,
            )
            db.session.add(annualReport)
            db.session.commit()
            flash("Annual Report added successfully!")

            form.filename.data = ''
            form.file.data = ''
            form.visible.data = ''


    return render_template('content/add_annualReport.html',
        form = form,
    )


@app.route('/update_annualReport/<int:id>', methods=['GET', 'POST'])
def update_annualReport(id):
    form = AnnualReportForm()
    annualReport_to_update = AnnualReports.query.get_or_404(id)
    if request.method == "POST":
        if request.files["file"]:
            folder = os.path.join(app.config["UPLOAD_FOLDER"], "activities")
            file = os.path.join(folder, annualReport_to_update.file)
            try:
                os.remove(file)
            except:
                print('Not possible to delete file ' + file)

            unique_filename = save_file(request.files["file"], "activities")

            annualReport_to_update.file = unique_filename
            annualReport_to_update.filename = request.files["file"].filename

        annualReport_to_update.visible = form.visible.data

        try:
            db.session.commit()
            flash("Annual Report updated successfully!")
            return render_template("content/update_annualReport.html",
                form=form,
                annualReport_to_update=annualReport_to_update)
        except:
            flash("Error")
            return render_template("content/update_annualReport.html",
                form=form,
                annualReport_to_update=annualReport_to_update)
    else:
        return render_template("content/update_annualReport.html",
            form=form,
            annualReport_to_update=annualReport_to_update)

@app.route('/delete_annualReport/<int:id>', methods=['GET', 'POST'])
def delete_annualReport(id):
    annualReport_to_update = AnnualReports.query.get_or_404(id)
    form = AnnualReportForm()
    try:
        db.session.delete(annualReport_to_update)
        db.session.commit()
        flash("Annual Report deleted successfully!")

        form.file.data = ''
        form.visible.data = ''

        return render_template('content/update_annualReport.html',
            form = form,
            annualReport_to_update=annualReport_to_update)
    except:
        flash("Error: Not possible to delete Annual Report.")
        return render_template('content/update_annualReport.html',
            form = form,
            annualReport_to_update=annualReport_to_update)
