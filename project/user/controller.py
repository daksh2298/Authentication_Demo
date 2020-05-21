__author__ = 'Daksh Patel'

from flask import request, g
from project import auth
from project.user.models import *
from utils import *

msg = 'Something went wrong'


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    global msg
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.objects(username=username_or_token).first()
        if not user or not user.verify_password(password):
            msg = 'Incorrect username of password!'
            return False
        else:
            msg = 'Verification successful.'
    g.user = user
    return True


@app.route('/login', methods=['POST'])
def login():
    global msg
    username = request.form.get('username')
    password = request.form.get('password')
    flag = verify_password(
        username_or_token=username,
        password=password
    )
    resp = None
    if flag:
        user = g.user
        auth_token = user.auth_token
        name = user.name
        code = 200
        status = True
        result = {
            'name': name,
            'auth_token': auth_token
        }
        resp = create_response(
            status_value=status,
            code=code,
            message=msg,
            result=result
        )
    else:
        code = 400
        status = False
        result = {}
        resp = create_response(
            status_value=status,
            code=code,
            message=msg,
            result=result
        )

    return resp


@app.route('/signup', methods=['POST'])
def add_user():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    query_set = User.objects(username=username)
    resp = None
    if query_set.count() != 0:
        status = False
        code = 400
        msg = 'Username already exists!'
        result = {}
        resp = create_response(
            status_value=status,
            code=code,
            message=msg,
            result=result
        )
    else:
        user = User()
        status = user.create_user(
            name=name,
            username=username,
            password=password
        )
        if status:
            code = 200
            result = {}
            msg = 'User added successfully!'
            resp = create_response(
                status_value=status,
                code=code,
                message=msg,
                result=result
            )
        else:
            code = 400
            result = {}
            msg = 'Something went wrong'
            resp = create_response(
                status_value=status,
                code=code,
                message=msg,
                result=result
            )
    return resp


@app.route("/api/private")
@auth.login_required
def private_resource():
    return create_response(
        status_value=True,
        code=200,
        message="You have accessed the private resource."
    )
