__author__ = "Daksh Patel"

from flask import jsonify


def create_response(status_value, code, message, result=None):
    """
    :param status_value: The status for the request (True/False)
    :type status_value: bool
    :param code: The status code for the request
    :type code: int
    :param message: The message for the request
    :type message: str
    :param result: The dictionary containing result for the request (if any)
    :type result: dict
    :return: A response to send
    :rtype: dict
    """
    if result is None:
        result = {}
    resp = {
        'status': status_value,
        'code': code,
        'message': message,
        'result': result,
        'version': 'v1'
        }
    resp = jsonify(resp)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


def unauthorized_access():
    code = 401
    status = False
    msg = f'Unauthorized access the private resources. Please login'
    result = {}
    resp = create_response(
        status_value=status,
        code=code,
        message=msg,
        result=result
        )
    return resp
