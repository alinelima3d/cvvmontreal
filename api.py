from flask import request

from app import app, db, Members, Meetings, Memberships, ExecutiveMembers, News, attendance, TaskRepartitionTexts
from flask import jsonify
import json

from werkzeug.security import generate_password_hash, check_password_hash


## API------------------------------------------------------

@app.route('/check_login/', methods = ['GET','POST'])
def check_login():
    result = json.loads(request.data)
    user = Members.query.filter_by(email=result["email"]).first()
    is_executive_member = False
    if not user:
        user = ExecutiveMembers.query.filter_by(email=result["email"]).first()
        is_executive_member = True

    userDict = {}
    if user:
        if user.verify_password(result["pass"]):
            userDict['id'] = user.id
            userDict['name'] = user.name
            userDict['email'] = user.email
            userDict['is_executive_member'] = is_executive_member
            if is_executive_member:
                userDict['member_pic'] = user.executive_member_pic
            else:
                userDict['member_pic'] = user.member_pic
            app.config['CURRENT_USER_ID'] = user.id
            app.config['IS_EXECUTIVE_MEMBER'] = is_executive_member
        else:
            userDict['error'] = "Invalid password"
    else:
        userDict['error'] = "Email not found"
    return userDict, 200



@app.route('/get_member/', methods = ['GET','POST'])
def get_member():
    result = json.loads(request.data)
    member = Members.query.filter_by(email=result["email"]).first()
    memberDict = {}
    if member:
        if member.verify_password(result["pass"]):
            memberDict['id'] = member.id
            memberDict['name'] = member.name
            memberDict['email'] = member.email
            memberDict['role'] = member.role
            memberDict['telephone'] = member.telephone
            memberDict['english'] = member.english
            memberDict['french'] = member.french
            memberDict['preferable'] = member.preferable
            memberDict['organization'] = member.organization
            memberDict['volunteers'] = member.volunteers
            memberDict['member_pic'] = member.member_pic
        else:
            memberDict['error'] = "Invalid password"
    else:
        memberDict['error'] = "Email not found"
    return memberDict, 200

@app.route('/get_member_id/<id>')
def get_member_id(id):
    user = Members.query.filter_by(id=id).first()
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
    userDict['member_pic'] = user.member_pic
    return userDict, 200

@app.route('/get_executive_member/', methods = ['GET','POST'])
def get_executive_member():
    result = json.loads(request.data)
    print('result', result)
    executiveMember = ExecutiveMembers.query.filter_by(email=result["email"]).first()
    executiveMemberDict = {}
    if executiveMember:
        if executiveMember.verify_password(result["pass"]):
            executiveMemberDict['id'] = executiveMember.id
            executiveMemberDict['name'] = executiveMember.name
            executiveMemberDict['email'] = executiveMember.email
            executiveMemberDict['role'] = executiveMember.role
            executiveMemberDict['telephone'] = executiveMember.telephone
            executiveMemberDict['english'] = executiveMember.english
            executiveMemberDict['french'] = executiveMember.french
            executiveMemberDict['preferable'] = executiveMember.preferable
            executiveMemberDict['organization'] = executiveMember.organization
            executiveMemberDict['executive_member_pic'] = executiveMember.executive_member_pic
        else:
            executiveMemberDict['error'] = "Invalid password"
    else:
        executiveMemberDict['error'] = "Email not found"
    print('executiveMemberDict', executiveMemberDict)
    return executiveMemberDict, 200

@app.route('/get_executive_member_id/<id>')
def get_executive_user_id(id):
    user = ExecutiveMembers.query.filter_by(id=id).first()
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
    userDict['executive_member_pic'] = user.executive_member_pic
    return userDict, 200

@app.route('/get_users')
def get_users():
    app.config['USER'] = user
    return jsonify(user_data), 200

@app.route('/add_likes_news/', methods = ['GET','POST'])
def add_likes_news():
    result = json.loads(request.data)
    news = News.query.filter_by(id=result["id"]).first()
    news.add_like()
    db.session.commit()
    returnVar = {'likes': news.likes}
    return returnVar, 200

@app.route('/change_attendance/', methods = ['GET','POST'])
def change_attendance():
    result = json.loads(request.data)
    print('result', result)
    meeting = Meetings.query.filter_by(id=result["meeting"]).first()
    member = Members.query.filter_by(id=result["member"]).first()
    returnVar = {}
    if result["checked"]:
        if not member in meeting.member_attendance:
            member.meetings_attendance.append(meeting)
            try:
                db.session.commit()
            except:
                returnVar["error"] = "Not possible to save Meeting Attendance"
    else:
        if member in meeting.member_attendance:
            member.meetings_attendance.remove(meeting)
            try:
                db.session.commit()
            except:
                returnVar["error"] = "Not possible to save Meeting Attendance"
    if not "error" in returnVar:
        returnVar["result"] = "Attendance saved successfully."
    return returnVar, 200

@app.route('/clear_attendance/', methods = ['GET','POST'])
def clear_attendance():
    meetings = Meetings.query.order_by(Meetings.id)
    member = Members.query.filter_by(id=Members.id).first()
    for meeting in meetings:
    #     for member in members:
        if member in meeting.member_attendance:
            member.meetings_attendance = []
            db.session.commit()
    returnVar = {}
    return returnVar, 200

@app.route('/create_initial_user/')
def create_initial_user():
    hashed_pw = generate_password_hash("123", method='pbkdf2:sha256')
    result = []
    print(1)
    executive_member = ExecutiveMembers.query.filter_by(name="Initial Executive Member").first()
    print(2)
    if not executive_member:
        print('2a')
        executiveMember = ExecutiveMembers(
            id=1,
            name="Initial Executive Member",
            email="exec@mail.com",
            role="Initial Executive Member",
            order=1,
            organization="System",
            password_hash=hashed_pw,
            )
        print('2b')
        db.session.add(executiveMember)
        print('2c')
        db.session.commit()
        print('2c')
        result.append("Initial Executive Member added successfully.")
    print('3')
    member = Members.query.filter_by(name="Initial Member").first()
    print('4')
    hashed_pw = generate_password_hash("123", method='pbkdf2:sha256')
    print('5')
    if not member:
        print('5a')
        member = Members(
            id=1,
            name="Initial Member",
            email="member@mail.com",
            role="Initial Member",
            organization="System",
            password_hash=hashed_pw,
            )
        print('5b')
        db.session.add(member)
        print('5c')
        db.session.commit()
        print('5d')
        result.append("Initial Member added successfully.")
        print('5e')
    print('6')
    task_repartitionText = TaskRepartitionTexts.query.filter_by(id=1).first()
    print('7')
    if not task_repartitionText:
        print('7a')
        task_repartitionText = TaskRepartitionTexts(
            id=1,
            title="Initial Title",
            text="Initial Text",
            )
        print('7b')
        db.session.add(task_repartitionText)
        print('7c')
        db.session.commit()
        print('7d')
        result.append("Initial Task Repartition added successfully.")
        print('7e')
    print('8')
    return result, 200
