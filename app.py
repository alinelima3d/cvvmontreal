from flask import Flask, render_template, jsonify, flash, request
from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor

from webforms import MemberForm, ExecutiveMemberForm, SurveyForm, MeetingForm
# from routes.members import members_page
# from yourapplication.simple_page import simple_page

from sqlalchemy import desc
from flask_migrate import Migrate

from flask_wtf.file import FileField
from datetime import datetime, timedelta
from datetime import date
import json

from werkzeug.utils import secure_filename
import uuid as uuid
import os

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
ckeditor = CKEditor(app)

app.config['SECRET_KEY'] = 'my super secret key that no one is suppose to know'
print('app.debug', app.debug)
# if app.debug:
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/cvv'
# else:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ucocfesi3a50sp:pd433ef3bdce54e70213c225eeb3635b196db7de24db82f7bad98f30d35820253@c34u0gd6rbe7bo.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6eq465ijvjihi'

UPLOAD_FOLDER = 'static/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)


attendance = db.Table('attendance',
    db.Column('member_id', db.Integer, db.ForeignKey('members.id')),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'))
)

# Database Model
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(50))
    telephone = db.Column(db.String(20))
    english = db.Column(db.Boolean)
    french = db.Column(db.Boolean)
    preferable = db.Column(db.String(100))
    organization = db.Column(db.String(100))
    volunteers = db.Column(db.Integer)
    member_since = db.Column(db.DateTime)
    member_pic = db.Column(db.String(400), nullable=True)
    password_hash = db.Column(db.String(128))
    meetings_attendance = db.relationship('Meetings', secondary=attendance, backref='member_attendance')

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # expiration_date = db.Column(db.DateTime)
    # an user can have many docs
    documents = db.relationship('Memberships', backref='membership')

    def __repr__(self):
        return '<Name %r>' % self.name

class ExecutiveMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(70))
    bio = db.Column(db.String(500))
    email = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(20))
    english = db.Column(db.Boolean)
    french = db.Column(db.Boolean)
    preferable = db.Column(db.String(100))
    organization = db.Column(db.String(100))
    order = db.Column(db.Integer)
    executive_member_pic = db.Column(db.String(400), nullable=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<Name %r>' % self.name

# Database Model
class Surveys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    responders = db.Column(db.Integer)
    file = db.Column(db.String(400), nullable=True)


    def __repr__(self):
        return '<Name %r>' % self.title

class Meetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    minute = db.Column(db.String(200))
    attendees = db.Column(db.Integer)
    file = db.Column(db.String(400), nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.date

class Memberships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    remembered = db.Column(db.Date)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    file = db.Column(db.String(400), nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name


class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)
    hour = db.Column(db.String(100))
    address = db.Column(db.String(200))
    file = db.Column(db.String(400))
    filename = db.Column(db.String(200))
    author = db.Column(db.String(100))

    def __repr__(self):
        return '<Name %r>' % self.title

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)
    file = db.Column(db.String(400))
    author = db.Column(db.String(100))
    type = db.Column(db.String(100))

    def add_like(self):
        self.likes += 1
        return True

    def __repr__(self):
        return '<Name %r>' % self.title

class AnnualReports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    file = db.Column(db.String(400))
    visible = db.Column(db.Boolean)

    def __repr__(self):
        return '<Title %r>' % self.title

class TaskRepartitionFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    file = db.Column(db.String(400))
    author = db.Column(db.String(100))

    def __repr__(self):
        return '<Title %r>' % self.title

class TaskRepartitionTexts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    text = db.Column(db.Text)
    author = db.Column(db.String(100))

    def __repr__(self):
        return '<Title %r>' % self.title

class Banners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    file = db.Column(db.String(400))
    visible = db.Column(db.Boolean)

    def __repr__(self):
        return '<Title %r>' % self.title

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100))
    organization = db.Column(db.String(200))
    visible = db.Column(db.Boolean)
    fontSize = db.Column(db.Float)

    def __repr__(self):
        return '<Title %r>' % self.title



## ERROR -----------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html"), 500


def get_payment_status(last_membership):
    result = {}
    today = date.today()
    status = "Membership Not Found"
    expiration_date = ""
    warning_icon = False
    if last_membership:
        diff = today - last_membership.end
        expiration_date = last_membership.end
        if last_membership.end > today:
            status = "Paid"
            if diff > timedelta(days=-30):
                status = "Almost Expired"
        else:
            status = "Expired"

        if status == "Almost Expired":
            warning_icon = True
            print('REMEMBERED', last_membership.remembered)
            if last_membership.remembered:
                warning_icon = False
            if not last_membership.remembered:
                warning_icon = True
    result['status'] = status
    result['warning_icon'] = warning_icon
    result['expiration_date'] = expiration_date
    if last_membership:
        result['remembered'] = last_membership.remembered
    else:
        result['remembered'] = 0
    return result


def save_file(file, folderName):
    # Save file name to database
    secure_filename_var = secure_filename(file.filename)
    unique_filename = str(uuid.uuid1()) + "_" + secure_filename_var

    # Save File
    folder = os.path.join(app.config["UPLOAD_FOLDER"], "taskRepartitions")
    try:
        os.makedirs(folder)
    except:
        print('Not possible to create folder' + folder)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], folderName, unique_filename))
    return unique_filename

# import declared routes
import general, members, executive_members, memberships, meetings, surveys, api, activities, annualReports, banners, news, quotes, taskRepartition

if __name__ == '__main__':
    app.run()
