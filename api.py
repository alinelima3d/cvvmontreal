
from app import app, Members, Meetings, Memberships, ExecutiveMembers


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
    userDict['member_pic'] = user.member_pic
    return userDict, 200

@app.route('/get_user_id/<id>')
def get_user_id(id):
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
