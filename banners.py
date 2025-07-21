from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, Banners, save_file
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
    form = BannerForm()
    banner_to_update = Banners.query.get_or_404(id)
    if request.method == "POST":
        if request.files["file"]:
            folder = os.path.join(app.config["UPLOAD_FOLDER"], "activities")
            file = os.path.join(folder, banner_to_update.file)
            try:
                os.remove(file)
            except:
                print('Not possible to delete file ' + file)

            unique_filename = save_file(request.files["file"], "activities")

            banner_to_update.file = unique_filename
            banner_to_update.filename = request.files["file"].filename

        banner_to_update.visible = form.visible.data

        try:
            db.session.commit()
            flash("Banner updated successfully!")
            return render_template("content/update_banner.html",
                form=form,
                banner_to_update=banner_to_update)
        except:
            flash("Error")
            return render_template("content/update_banner.html",
                form=form,
                banner_to_update=banner_to_update)
    else:
        return render_template("content/update_banner.html",
            form=form,
            banner_to_update=banner_to_update)

@app.route('/delete_banner/<int:id>', methods=['GET', 'POST'])
def delete_banner(id):
    banner_to_update = Banners.query.get_or_404(id)
    form = BannerForm()
    try:
        db.session.delete(banner_to_update)
        db.session.commit()
        flash("Banner deleted successfully!")

        form.file.data = ''
        form.visible.data = ''

        return render_template('content/update_banner.html',
            form = form,
            banner_to_update=banner_to_update)
    except:
        flash("Error: Not possible to delete Banner.")
        return render_template('content/update_banner.html',
            form = form,
            banner_to_update=banner_to_update)
