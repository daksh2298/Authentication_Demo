__author__ = 'Daksh Patel'

from flask import request, g
from project import auth, app
from project.user.models import User
from utils import create_response


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.objects(username=username_or_token).first()
        if not user or not user.verify_password(password):
            g.msg = 'Incorrect username of password!'
            return False
        else:
            g.msg = 'Verification successful.'
    g.user = user
    return True


@app.route('/login', methods=['POST'])
def login():
    """
    This function is called when a request is received at /login endpoint
    :return: JSON object containing the name and authentication token in response
    """
    username = request.form.get('username')
    password = request.form.get('password')
    # verifies the password
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
            message=g.msg,
            result=result
            )
    else:
        code = 400
        status = False
        result = {}
        resp = create_response(
            status_value=status,
            code=code,
            message=g.msg,
            result=result
            )

    return resp


@app.route('/signup', methods=['POST'])
def add_user():
    """
    This function is called when a request is received at /signup endpoint
    :return: JSON object containing the response
    """
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
# "@auth.login_required" decorator authorizes the user by verifying the token received in the request
def private_resource():
    """
    This function is called when a request is received at /api/private endpoint
    :return: JSON object containing the response
    """
    return create_response(
        status_value=True,
        code=200,
        message="You have accessed the private resource."
        )


@app.route("/api/public")
# As we have not added "@auth.login_required" decorator, no authorization will be performed and
# user will be able to access this endpoint even without login
def public_resource():
    """
    This function is called when a request is received at /api/private endpoint
    :return: JSON object containing the response
    """
    return create_response(
        status_value=True,
        code=200,
        message="You have access the public resource"
        )


@app.route('/logout', methods=['GET', 'POST'])
@auth.login_required  # User can only logout if and only if the have logged in, so authorization is required
def logout():
    user = g.user
    user.set_new_auth_token()
    print('logged out')
    return create_response(
        status_value=True,
        code=200,
        message="User Logged out and authentication token changed"
        )
