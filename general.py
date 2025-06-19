from flask import Flask, render_template, jsonify, flash, request
from app import app, ExecutiveMembers


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

@app.route('/executive_members')
def executive_members():
    our_executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.order)
    return render_template('executive_members/executive_members.html',
        our_executive_members=our_executive_members)

@app.route('/become_member')
def become_member():
    return render_template('members/become_member.html')
