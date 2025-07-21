from flask import Flask, render_template, jsonify, flash, request
from app import app, ExecutiveMembers, Members, Quotes, AnnualReports, Banners, Activities, News

from datetime import date, timedelta
from datetime import datetime

about_buttons = [
    {"name": "Our Mission", "link": "/mission"},
    {"name": "Executive Members", "link": "/executive_members"},
    {"name": "Member Directory", "link": "/member_directory"},
    {"name": "Annual Reports", "link": "/annual_reports"},
]
news_buttons = [
    {"name": "News from the vol. ecosystem", "link": "/news"},
    {"name": "Activity Calendar", "link": "/activity_calendar"},
]

def calculate_days_from_today(target_date, date_format="%Y-%m-%d"):
    today = date.today()
    # target_date = datetime.strptime(target_date_str, date_format).date()

    delta = target_date - today

    if delta.days > 0:
        return f"{delta.days} days left!"
    elif delta.days < 0:
        return "passed"
    else:
        return "That's today!"

@app.route('/')
def index():
    clean = request.args.get('clean')
    quotes = Quotes.query.filter_by(visible=True).all()
    banner = Banners.query.filter_by(visible=True).first()
    return render_template('/general/index.html',
        clean=clean,
        quotes=quotes,
        banner=banner)

@app.route('/about')
def about():
    clean = request.args.get('clean')
    return render_template('/general/about.html',
        clean=clean)

@app.route('/activity_calendar')
def activity_calendar():
    clean = request.args.get('clean')
    activities = Activities.query.order_by(Activities.date.desc())
    activity_list = []
    for activity in activities:
        activityDict = {}
        activityDict["title"] = activity.title
        activityDict["text"] = activity.text
        activityDict["date"] = activity.date
        activityDict["hour"] = activity.hour
        activityDict["when"] = "%s at %s" % (activity.date, activity.hour)
        activityDict["address"] = activity.address
        activityDict["file"] = activity.file


        time_difference =calculate_days_from_today(activity.date)
        activityDict["gray_text"] = ""
        activityDict["time_difference"] = time_difference
        if time_difference == "passed":
            activityDict["gray_text"] = "gray_text"
            activityDict["time_difference"] = ""

        party = False
        if time_difference == "That's today!":
            party = True
        activityDict["party"] = party
        activity_list.append(activityDict)

    return render_template('general/activity_calendar.html',
        clean=clean,
        activities=activity_list,
        buttons=news_buttons
    )

@app.route('/annual_reports')
def annual_reports():
    annualReports = AnnualReports.query.order_by(AnnualReports.filename)
    clean = request.args.get('clean')
    return render_template('/general/annual_reports.html',
        buttons=about_buttons,
        clean=clean,
        annualReports=annualReports
    )

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
    news = News.query.order_by(News.date)
    clean = request.args.get('clean')
    return render_template('general/news.html',
        clean=clean,
        news=news,
        buttons=news_buttons,
    )

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
