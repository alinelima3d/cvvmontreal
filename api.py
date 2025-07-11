from flask import request

from app import app, Members, Meetings, Memberships, ExecutiveMembers
from flask import jsonify

## API------------------------------------------------------
@app.route('/get_member/', methods = ['GET','POST'])
def get_member():
    result = jsonify(request.data)
    print('result', result)
    member = Members.query.filter_by(email=request.data["email"]).first()
    if member:
        memberDict = {}
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
    userDict['executive_member_pic'] = user.executive_member_pic
    return userDict, 200

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
