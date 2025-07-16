from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, TaskRepartitionTexts, TaskRepartitionFiles, save_file

from webforms import TaskRepartitionTextForm, TaskRepartitionFileForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os

@app.route('/add_task_repartition_file', methods=['GET', 'POST'])
def add_task_repartition_file():
    form = TaskRepartitionFileForm()
    if form.validate_on_submit():
        taskRepartition = TaskRepartitionFiles.query.filter_by(filename=form.filename.data).first()
        if taskRepartition is None:
            unique_filename = save_file(request.files["file"], "taskRepartitions")
            form.file.data = unique_filename
            form.filename.data = request.files["file"].filename

            # Save in database
            taskRepartition = TaskRepartitionFiles(
                filename=form.filename.data,
                file=form.file.data,
            )

            db.session.add(taskRepartition)
            db.session.commit()
            flash("Task Repartition File added successfully!")

            form.filename.data = ''
            form.file.data = ''


    return render_template('content/add_task_repartition_file.html',
        form = form,
    )


@app.route('/update_task_repartition_file/<int:id>', methods=['GET', 'POST'])
def update_task_repartition_file(id):
    form = TaskRepartitionFileForm()
    date = None
    task_to_update = TaskRepartitionFiles.query.get_or_404(id)
    if request.method == "POST":
        # task_to_update.text = request.form["text"]
        folder = os.path.join(app.config["UPLOAD_FOLDER"], "taskRepartitions")
        file = os.path.join(folder, task_to_update.file)
        try:
            os.remove(file)
        except:
            print('Not possible to delete file ' + file)

        unique_filename = save_file(request.files["file"], "taskRepartitions")

        task_to_update.file = unique_filename
        task_to_update.filename = request.files["file"].filename

        try:
            db.session.commit()
            flash("Task Repartition File updated successfully!")
            return render_template("content/update_task_repartition_file.html",
                form=form,
                task_to_update=task_to_update)
        except:
            flash("Error")
            return render_template("content/update_task_repartition_file.html",
                form=form,
                task_to_update=task_to_update)
    else:
        return render_template("content/update_task_repartition_file.html",
            form=form,
            task_to_update=task_to_update)


@app.route('/delete_task_repartition_file/<int:id>', methods=['GET', 'POST'])
def delete_task_repartition_file(id):
    task_to_update = TaskRepartitionFiles.query.get_or_404(id)
    form = TaskRepartitionFileForm()
    folder = os.path.join(app.config["UPLOAD_FOLDER"], "taskRepartitions")
    file = os.path.join(folder, task_to_update.file)
    try:
        os.remove(file)
    except:
        print('Not possible to delete file ' + file)
    try:
        db.session.delete(task_to_update)
        db.session.commit()
        flash('Task Repartition deleted successfully!')

        return render_template('content/update_task_repartition_file.html',
            form = form,
            task_to_update=task_to_update)
    except:
        return render_template('content/update_task_repartition_file.html',
            form = form,
            task_to_update=task_to_update)


@app.route('/update_task_repartition/<int:id>', methods=['GET', 'POST'])
def update_task_repartition(id):
    form = TaskRepartitionTextForm()
    task_to_update = TaskRepartitionTexts.query.get_or_404(1)
    print('task_to_update', task_to_update)
    if request.method == "POST":

        task_to_update.text = request.form.get('ckeditor')
        try:
            db.session.commit()
            flash("Task Repartition Text updated successfully!")

            return render_template("content/update_task_repartition_text.html",
                form=form,
                task_to_update=task_to_update)
        except:
            flash("Error")
            return render_template("content/update_task_repartition_text.html",
                form=form,
                task_to_update=task_to_update)
    else:
        return render_template("content/update_task_repartition_text.html",
            form=form,
            task_to_update=task_to_update)
