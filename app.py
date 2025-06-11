from flask import Flask, render_template, jsonify, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my super secret key that no one is suppose to know'
if app.debug:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/cvv'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ue9r2df1jcvfh2:p77d7215e49ae55f05cdd9aeceb8bbd3d601d18cd9fba706bac3c09e836b2575d@c2hbg00ac72j9d.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6igtkis6hsviv'
db = SQLAlchemy(app)


# MEMBERS FORM/DATABASE ----------------------------------------------------

# Flask form
class MemberForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    role = StringField("Role:", validators=[DataRequired()])
    telephone = StringField("Phone Number:")
    english = BooleanField("English")
    french = BooleanField("French")
    preferable = IntegerField("Preferable:")
    # preferable = SelectField('Preferable:', choices=[('1', 'English'), ('2', 'French')], validators=[InputRequired()])
    organization = StringField("Organization:")
    volunteers = IntegerField("Number Voluntters I manage:")
    submit = SubmitField("Submit")


# Database Model
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(50))
    telephone = db.Column(db.String(20))
    english = db.Column(db.Boolean)
    french = db.Column(db.Boolean)
    preferable = db.Column(db.Integer)
    organization = db.Column(db.String(100))
    volunteers = db.Column(db.Integer)
    member_since = db.Column(db.DateTime)
    # expiration_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    # name = None
    form = MemberForm()
    if form.validate_on_submit():
        user = Members.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Members(
            name=form.name.data,
            role=form.role.data,
            email=form.email.data,
            telephone=form.telephone.data,
            english=form.english.data,
            french=form.french.data,
            preferable=form.preferable.data,
            organization=form.organization.data,
            volunteers=form.volunteers.data,
            )
            db.session.add(user)
            db.session.commit()
            flash('Member <strong>%s</strong> added successfully!' % form.name.data)
        # name = form.name.data
        form.name.data = ''
        form.role.data = ''
        form.email.data = ''
        form.telephone.data = ''
        form.english.data = ''
        form.french.data = ''
        form.preferable.data = ''
        form.organization.data = ''
        form.volunteers.data = ''

    our_members = Members.query.order_by(Members.name)
    return render_template('members/add_member.html',
        form = form,
        # name=name,
        our_members=our_members)

@app.route('/update_member/<int:id>', methods=['GET', 'POST'])
def update_member(id):
    form = MemberForm()
    member_to_update = Members.query.get_or_404(id)
    if request.method == "POST":
        member_to_update.name = request.form["name"]
        member_to_update.role = request.form["role"]
        member_to_update.email = request.form["email"]
        member_to_update.telephone = request.form["telephone"]
        member_to_update.english = request.form["english"]
        member_to_update.french = request.form["french"]
        member_to_update.preferable = request.form["preferable"]
        member_to_update.organization = request.form["organization"]
        member_to_update.volunteers = request.form["volunteers"]
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("members/update_member.html",
                form=form,
                member_to_update=member_to_update)
        except:
            flash("Error")
            return render_template("members/update_member.html",
                form=form,
                member_to_update=member_to_update)
    else:
        return render_template("members/update_member.html",
            form=form,
            member_to_update=member_to_update)

@app.route('/view_member/<int:id>')
def view_member(id):
    member = Members.query.get_or_404(id)
    return render_template("members/view_member.html",
        member=member)

@app.route('/delete_member/<int:id>', methods=['GET', 'POST'])
def delete_member(id):
    member_to_delete = Members.query.get_or_404(id)
    name = None
    form = MemberForm()
    try:
        db.session.delete(member_to_delete)
        db.session.commit()
        flash("Member deleted successfully!")

        name=member_to_delete.name

        our_members = Members.query.order_by(Members.name)
        return render_template('members/update_member.html',
            form = form,
            name=name,
            our_members=our_members,
            member_to_update=member_to_delete)
    except:
        flash("Error")
        our_members = Members.query.order_by(Members.name)
        return render_template('members/update_member.html',
            form = form,
            name=name,
            our_members=our_members,
            member_to_update=member_to_delete)

@app.route('/become_member')
def become_member():
    return render_template('members/become_member.html')



@app.route('/member_area/<int:id>')
def member_area(id):
    form = MemberForm()
    our_members = Members.query.order_by(Members.name)
    meetings = Meetings.query.order_by(Meetings.date)
    member_to_update = Members.query.filter_by(id=id).first()
    buttons = [
        {"name": "My Info", "anchor": "myInfo"},
        {"name": "My Membership", "anchor": "myMembership"},
        {"name": "Meetings", "anchor": "meetings_list"},
        {"name": "Contact Other Members", "anchor": "member_list"},
    ]
    return render_template('members/member_area.html',
        our_members=our_members,
        executive_member=False,
        buttons=buttons,
        meetings=meetings,
        member_to_update=member_to_update,
        form=form,
        deletable=False,
        title="Contact Other Members")
# EXECUTIVE MEMBERS FORM/DATABASE ----------------------------------------------------

# Flask form
class ExecutiveMemberForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    role = StringField("Role:", validators=[DataRequired()])
    telephone = StringField("Telephone:")
    english = BooleanField("English:")
    french = BooleanField("French:")
    preferable = IntegerField("Preferable:")
    organization = StringField("Organization:")
    order = IntegerField("Order:")
    submit = SubmitField("Update")


# Database Model
class ExecutiveMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(70), nullable=False)
    roleDescription = db.Column(db.String(200))
    email = db.Column(db.String(50))
    telephone = db.Column(db.String(20))
    english = db.Column(db.Boolean)
    french = db.Column(db.Boolean)
    preferable = db.Column(db.Integer)
    organization = db.Column(db.String(100))
    order = db.Column(db.Integer)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/add_executive_member', methods=['GET', 'POST'])
def add_executive_member():
    name = None
    form = ExecutiveMemberForm()
    if form.validate_on_submit():
        user = ExecutiveMembers.query.filter_by(email=form.email.data).first()
        if user is None:
            executiveMember = ExecutiveMembers(
                name=form.name.data,
                email=form.email.data,
                # english=form.english.data,
                # french=form.french.data,
                role=form.role.data,
                order=form.order.data,
                telephone=form.telephone.data,
                organization=form.organization.data,


                )
            db.session.add(executiveMember)
            db.session.commit()
            flash('Executive Member <strong>%s</strong> added successfully!' % form.name.data)

        name = form.name.data
        form.name.data = ''
        form.email.data = ''

    our_executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.name)
    return render_template('executive_members/add_executive_member.html',
        form = form,
        name=name,
        our_executive_members=our_executive_members)

@app.route('/update_executive_member/<int:id>', methods=['GET', 'POST'])
def update_executive_member(id):
    form = ExecutiveMemberForm()
    executive_member_to_update = ExecutiveMembers.query.get_or_404(id)
    if request.method == "POST":
        executive_member_to_update.name = request.form["name"]
        executive_member_to_update.role = request.form["role"]
        executive_member_to_update.email = request.form["email"]
        executive_member_to_update.telephone = request.form["telephone"]
        executive_member_to_update.order = request.form["order"]
        # executive_member_to_update.english = request.form["english"]
        # executive_member_to_update.french = request.form["french"]
        # executive_member_to_update.preferable = request.form["preferable"]
        executive_member_to_update.organization = request.form["organization"]
        try:
            db.session.commit()
            flash('Executive Member <strong>%s</strong> updated successfully!' % executive_member_to_update.name)
            return render_template("executive_members/update_executive_member.html",
                form=form,
                executive_member_to_update=executive_member_to_update,
                deletable=True)
        except:
            flash("Error")
            return render_template("executive_members/update_executive_member.html",
                form=form,
                executive_member_to_update=executive_member_to_update,
                deletable=True)
    else:
        return render_template("executive_members/update_executive_member.html",
            form=form,
            executive_member_to_update=executive_member_to_update,
            deletable=True)

@app.route('/delete_executive_member/<int:id>', methods=['GET', 'POST'])
def delete_executive_member(id):
    executive_member_to_delete = ExecutiveMembers.query.get_or_404(id)
    name = None
    form = ExecutiveMemberForm()
    try:
        db.session.delete(executive_member_to_delete)
        db.session.commit()
        flash('Executive Member <strong>%s</strong> deleted successfully!' % executive_member_to_delete.name)

        name=executive_member_to_delete.name

        return render_template('executive_members/update_executive_member.html',
            form = form,
            name=name,
            executive_member_to_update=executive_member_to_delete)
    except:
        return render_template('executive_members/update_executive_member.html',
            form = form,
            name=name,
            executive_member_to_update=executive_member_to_delete)

@app.route('/executive_member_area/<int:id>')
def executive_member_area(id):
    our_executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.name)
    our_members = Members.query.order_by(Members.name)
    form = ExecutiveMemberForm()
    executive_member_to_update = ExecutiveMembers.query.filter_by(id=id).first()
    surveys = Surveys.query.order_by(Surveys.title)
    meetings = Meetings.query.order_by(desc(Meetings.date))
    buttons = [
        {"name": "My Info", "anchor": "myInfo"},
        {"name": "Task Repartition", "anchor": "taskRepartition"},
        {"name": "Payment Status", "anchor": "paymentList"},
        {"name": "Member Attendance", "anchor": "attendanceList"},
        {"name": "Surveys", "anchor": "surveysList"},
        {"name": "Meetings", "anchor": "meetings_list"},
        {"name": "Executive Members", "anchor": "executive_member_list"},
        {"name": "Members", "anchor": "member_list"},
    ]
    return render_template('executive_members/executive_member_area.html',
        our_members=our_members,
        our_executive_members=our_executive_members,
        executive_member=True,
        buttons=buttons,
        surveys=surveys,
        meetings=meetings,
        title="Members",
        executive_member_to_update=executive_member_to_update,
        deletable=True,
        form=form)


@app.route('/executive_members')
def executive_members():
    our_executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.order)
    return render_template('executive_members/executive_members.html',
        our_executive_members=our_executive_members)

# SURVEY FORM/DATABASE ----------------------------------------------------

# Survey form
class SurveyForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    start = DateField("Start")
    end = DateField("End")
    responders = IntegerField("Responders")
    file = StringField("File")
    submit = SubmitField("Submit")

# Database Model
class Surveys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    responders = db.Column(db.Integer)
    file = db.Column(db.String(200))

    def __repr__(self):
        return '<Name %r>' % self.title

@app.route('/survey/add', methods=['GET', 'POST'])
def add_survey():
    title = None
    form = SurveyForm()
    if form.validate_on_submit():
        survey = Surveys.query.filter_by(title=form.title.data).first()
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

    return render_template('general/add_survey.html',
        form = form,
        title=title,
        )

@app.route('/update_survey/<int:id>', methods=['GET', 'POST'])
def update_survey(id):
    form = SurveyForm()
    title = None
    survey_to_update = Surveys.query.get_or_404(id)
    if request.method == "POST":
        survey_to_update.date = request.form["date"]
        survey_to_update.minute = request.form["minute"]
        survey_to_update.attendees = request.form["attendees"]
        try:
            db.session.commit()
            flash("Meeting updated successfully!")
            return render_template("executive_members/update_survey.html",
                form=form,
                survey_to_update=survey_to_update)
        except:
            flash("Error")
            return render_template("executive_members/update_survey.html",
                form=form,
                survey_to_update=survey_to_update)
    else:
        return render_template("executive_members/update_survey.html",
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

        return render_template('executive_members/update_survey.html',
            form = form,
            title=title,
            survey_to_update=survey_to_delete)
    except:
        flash("Error")
        return render_template('executive_members/update_survey.html',
            form = form,
            title=title,
            survey_to_update=survey_to_delete)

# MEETINGS ----------------------------------------------------
# Database Model
class Meetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    minute = db.Column(db.String(200))
    attendees = db.Column(db.Integer)

    def __repr__(self):
        return '<Name %r>' % self.date

# Meeting form
class MeetingForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    minute = StringField("Minute")
    attendees = IntegerField("Attendees")
    submit = SubmitField("Submit")

@app.route('/meeting/add', methods=['GET', 'POST'])
def add_meeting():
    date = None
    form = MeetingForm()
    if form.validate_on_submit():
        meeting = Meetings.query.filter_by(date=form.date.data).first()
        if meeting is None:
            meeting = Meetings(date=form.date.data, minute=form.minute.data,
            attendees=form.attendees.data)
            db.session.add(meeting)
            db.session.commit()
            flash("Meeting added successfully!")

            date = form.date.data
            form.date.data = ''
            form.minute.data = ''
            form.attendees.data = ''


    return render_template('general/add_meeting.html',
        form = form,
        date=date,
        )

@app.route('/update_meeting/<int:id>', methods=['GET', 'POST'])
def update_meeting(id):
    form = MeetingForm()
    date = None
    meeting_to_update = Meetings.query.get_or_404(id)
    if request.method == "POST":
        meeting_to_update.date = request.form["date"]
        meeting_to_update.minute = request.form["minute"]
        meeting_to_update.attendees = request.form["attendees"]
        try:
            db.session.commit()
            flash("Meeting updated successfully!")
            form.date.data = ''
            form.minute.data = ''
            form.attendees.data = ''
            return render_template("executive_members/update_meeting.html",
                form=form,
                meeting_to_update=meeting_to_update)
        except:
            flash("Error")
            return render_template("executive_members/update_meeting.html",
                form=form,
                meeting_to_update=meeting_to_update)
    else:
        return render_template("executive_members/update_meeting.html",
            form=form,
            meeting_to_update=meeting_to_update)

@app.route('/delete_meeting/<int:id>', methods=['GET', 'POST'])
def delete_meeting(id):
    meeting_to_delete = Meetings.query.get_or_404(id)
    date = None
    form = MeetingForm()
    try:
        db.session.delete(meeting_to_delete)
        db.session.commit()
        flash("Meeting deleted successfully!")

        date=meeting_to_delete.date
        form.date.data = ''
        form.minute.data = ''
        form.attendees.data = ''

        return render_template('executive_members/update_meeting.html',
            form = form,
            date=date,
            meeting_to_update=meeting_to_delete)
    except:
        flash("Error")
        return render_template('executive_members/update_meeting.html',
            form = form,
            date=date,
            meeting_to_update=meeting_to_delete)

# GENERAL ----------------------------------------------------
@app.route('/')
def index():
    return render_template('/general/index.html')

@app.route('/about')
def about():
    return render_template('/general/about.html')

@app.route('/activity_calendar')
def activity_calendar():
    return render_template('general/activity_calendar.html')

@app.route('/annual_reports')
def annual_reports():
    return render_template('/general/annual_reports.html')

@app.route('/contact_us')
def contact_us():
    return render_template('general/contact_us.html')

@app.route('/login')
def login():
    return render_template('general/login.html')

@app.route('/member_directory')
def member_directory():
    return render_template('/general/member_directory.html')

@app.route('/mission')
def mission():
    return render_template('general/mission.html')

@app.route('/news')
def news():
    return render_template('general/news.html')

@app.route('/resources')
def resources():
    return render_template('general/resources.html')

## API------------------------------------------------------
@app.route('/get_user/<email>')
def get_user(email):
    user = Members.query.filter_by(email=email).first()
    userDict = {}
    userDict['id'] = user.id
    userDict['name'] = user.name
    userDict['email'] = user.email
    userDict['role'] = user.role
    userDict['telephone'] = user.telephone
    userDict['english'] = user.english
    userDict['french'] = user.french
    userDict['preferable'] = user.preferable
    userDict['organization'] = user.organization
    userDict['volunteers'] = user.volunteers
    return userDict, 200

@app.route('/get_executive_user/<email>')
def get_executive_user(email):
    user = ExecutiveMembers.query.filter_by(email=email).first()
    userDict = {}
    userDict['id'] = user.id
    userDict['name'] = user.name
    userDict['email'] = user.email
    userDict['role'] = user.role
    userDict['telephone'] = user.telephone
    userDict['english'] = user.english
    userDict['french'] = user.french
    userDict['preferable'] = user.preferable
    userDict['organization'] = user.organization
    return userDict, 200

@app.route('/get_users')
def get_users():
    app.config['USER'] = user
    return jsonify(user_data), 200

## ERROR -----------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html"), 500

@app.template_filter('removeHour')
def removeHour_filter(s):
    return s.split(' ')[0]

# with app.app_context():
#     db.create_all()

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
