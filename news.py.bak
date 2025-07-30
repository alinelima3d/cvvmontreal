from flask import Flask, render_template, jsonify, flash, request
from app import app, db, Members, News, save_file
from webforms import NewsForm

from werkzeug.utils import secure_filename
import uuid as uuid
import os
from datetime import date

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
                date=date.today(),
                file=form.file.data,
                type=form.type.data,
                author=form.author.data,
            )
            db.session.add(news)
            db.session.commit()
            flash("News added successfully!")

            form.title.data = ''
            form.text.data = ''
            form.file.data = ''
            form.type.data = ''
            form.author.data = ''


    return render_template('content/add_news.html',
        form = form,
    )


@app.route('/update_news/<int:id>', methods=['GET', 'POST'])
def update_news(id):
    form = NewsForm()
    news_to_update = News.query.get_or_404(id)
    if request.method == "POST":
        if request.files["file"]:
            folder = os.path.join(app.config["UPLOAD_FOLDER"], "activities")
            file = os.path.join(folder, news_to_update.file)
            try:
                os.remove(file)
            except:
                print('Not possible to delete file ' + file)

            unique_filename = save_file(request.files["file"], "activities")

            news_to_update.file = unique_filename
            news_to_update.filename = request.files["file"].filename

        news_to_update.text = request.form.get('ckeditor')
        news_to_update.date = form.date.data
        news_to_update.author = form.author.data
        news_to_update.title = form.title.data
        news_to_update.type = form.type.data

        try:
            db.session.commit()
            flash("News updated successfully!")
            return render_template("content/update_news.html",
                form=form,
                news_to_update=news_to_update)
        except:
            flash("Error: Not possible to update news.")
            return render_template("content/update_news.html",
                form=form,
                news_to_update=news_to_update)
    else:
        return render_template("content/update_news.html",
            form=form,
            news_to_update=news_to_update)

@app.route('/delete_news/<int:id>', methods=['GET', 'POST'])
def delete_news(id):
    news_to_delete = News.query.get_or_404(id)
    print('news_to_delete', news_to_delete)
    form = NewsForm()
    try:
        db.session.delete(news_to_delete)
        db.session.commit()
        flash("News deleted successfully!")

        form.title.data = ''
        form.text.data = ''
        form.date.data = ''
        form.file.data = ''
        form.author.data = ''

        return render_template('content/update_news.html',
            form = form,
            news_to_update=news_to_delete)
    except:
        flash("Error: Not possible to delete news.")
        return render_template('content/update_news.html',
            form = form,
            news_to_update=news_to_delete)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
def view_news(id):
    news = News.query.filter_by(id=id).first()
    return render_template('content/view_news.html',
        news=news,
    )
