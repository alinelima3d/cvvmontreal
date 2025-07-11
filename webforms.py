from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField, FileField, PasswordField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length


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
    member_pic = FileField("Member Pic:")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


class ExecutiveMemberForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    role = StringField("Role:", validators=[DataRequired()])
    bio = StringField("Bio:")
    telephone = StringField("Telephone:")
    english = BooleanField("English:")
    french = BooleanField("French:")
    preferable = IntegerField("Preferable:")
    organization = StringField("Organization:")
    order = IntegerField("Order:")
    executive_member_pic = FileField("Executive Member Pic:")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Update")


class SurveyForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    start = DateField("Start")
    end = DateField("End")
    responders = IntegerField("Responders")
    file = FileField("File")
    submit = SubmitField("Submit")

class MeetingForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    minute = StringField("Minute")
    attendees = IntegerField("Attendees")
    file = FileField("File")
    submit = SubmitField("Submit")

class MembershipForm(FlaskForm):
    start = DateField("Start")
    end = DateField("End")
    remembered = DateField("Remembered")
    file = FileField("File")
    submit = SubmitField("Submit")
