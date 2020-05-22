__author__ = 'Daksh Patel'

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import os
from dotenv import load_dotenv
from utils import unauthorized_access

app = Flask(__name__)
app.secret_key = 'secret-key'
CORS(app)
auth = HTTPBasicAuth()



@auth.error_handler
def custom_401():
    """
    This function is used to return the custom response for unauthorized access to the api.
    :return:
    JSON response with message, status, and code
    """
    return unauthorized_access()


# Loading environment variable from .env file
load_dotenv()
# Getting the environment variables
database = os.getenv("dbname")
username = os.getenv("username")
password = os.getenv("password")

# Setting database configuration in flask app object
app.config['MONGODB_SETTINGS'] = {
    'host': f'mongodb+srv://{username}:{password}@authenticationdemo-c1kk7.mongodb.net/{database}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE'
}

# creating database object
db = MongoEngine(app)

# import the modules after creating the app and auth objects
import project.user
