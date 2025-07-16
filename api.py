from flask import request

from app import app, db, Members, Meetings, Memberships, ExecutiveMembers, News
from flask import jsonify
import json

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
