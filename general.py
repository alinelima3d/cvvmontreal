from flask import Flask, render_template, jsonify, flash, request
from app import app, ExecutiveMembers, Members

about_buttons = [
    {"name": "Our Mission", "link": "/mission"},
    {"name": "Executive Members", "link": "/executive_members"},
    {"name": "Member Directory", "link": "/member_directory"},
    {"name": "Annual Reports", "link": "/annual_reports"},
]


@app.route('/')
def index():
    clean = request.args.get('clean')
    return render_template('/general/index.html',
        clean=clean)

@app.route('/about')
def about():
    clean = request.args.get('clean')
    return render_template('/general/about.html',
        clean=clean)

@app.route('/activity_calendar')
def activity_calendar():
    clean = request.args.get('clean')
    return render_template('general/activity_calendar.html',
        clean=clean)

@app.route('/annual_reports')
def annual_reports():
    clean = request.args.get('clean')
    return render_template('/general/annual_reports.html', buttons=about_buttons)

@app.route('/contact_us')
def contact_us():
    clean = request.args.get('clean')
    return render_template('general/contact_us.html',
        clean=clean)

@app.route('/login')
def login():
    clean = request.args.get('clean')
    return render_template('general/login.html',
        clean=clean)

@app.route('/member_directory')
def member_directory():
    members = Members.query.order_by(Members.name)
    executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.name)
    organizations = []
    for member in members:
        if member.organization:
            organizations.append(member.organization)
    for executive_member in executive_members:
        if executive_member.organization:
            organizations.append(executive_member.organization)
    organizations = list(set(organizations))
    return render_template('/general/member_directory.html',
        buttons=about_buttons,
        organizations=sorted(organizations))

@app.route('/mission')
def mission():
    clean = request.args.get('clean')
    return render_template('general/mission.html',
        buttons=about_buttons,
        clean=clean)

@app.route('/news')
def news():
    clean = request.args.get('clean')
    return render_template('general/news.html',
        clean=clean)

@app.route('/resources')
def resources():
    clean = request.args.get('clean')
    return render_template('general/resources.html',
        clean=clean)

@app.route('/executive_members')
def executive_members():
    clean = request.args.get('clean')
    our_executive_members = ExecutiveMembers.query.order_by(ExecutiveMembers.order)
    return render_template('executive_members/executive_members.html',
        our_executive_members=our_executive_members,
        buttons=about_buttons,
        clean=clean)

@app.route('/become_member')
def become_member():
    clean = request.args.get('clean')
    return render_template('members/become_member.html',
        clean=clean)
