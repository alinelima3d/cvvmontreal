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
    form = QuoteForm()
    quote_to_update = Quotes.query.get_or_404(id)
    if request.method == "POST":
        print("get text", request.form.get('text'))
        quote_to_update.title = form.title.data
        quote_to_update.text = request.form.get('text')
        quote_to_update.author = form.author.data
        quote_to_update.organization = form.organization.data
        quote_to_update.visible = form.visible.data
        quote_to_update.fontSize = form.fontSize.data

        try:
            db.session.commit()
            flash("Quote updated successfully!")
            return render_template("content/update_quote.html",
                form=form,
                quote_to_update=quote_to_update)
        except:
            flash("Error: Not possible to update quote.")
            return render_template("content/update_quote.html",
                form=form,
                quote_to_update=quote_to_update)
    else:
        return render_template("content/update_quote.html",
            form=form,
            quote_to_update=quote_to_update)

@app.route('/delete_quote/<int:id>', methods=['GET', 'POST'])
def delete_quote(id):
    quote_to_update = Quotes.query.get_or_404(id)
    form = QuoteForm()
    try:
        db.session.delete(quote_to_update)
        db.session.commit()
        flash("Quote deleted successfully!")

        form.title.data = ''
        form.text.data = ''
        form.author.data = ''
        form.organization.data = ''
        form.visible.data = ''
        form.fontSize.data = ''


        return render_template('content/update_quote.html',
            form = form,
            quote_to_update=quote_to_update)
    except:
        flash("Error: Not possible to delete quote.")
        return render_template('content/update_quote.html',
            form = form,
            quote_to_update=quote_to_update)
