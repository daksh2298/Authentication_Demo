__author__ = 'Daksh Patel'

from flask_security import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.hash import sha256_crypt
from project import app, db


class User(db.Document, UserMixin):
    name = db.StringField(max_length=50)
    username = db.StringField(max_length=50)
    password = db.StringField(max_length=255)
    auth_token = db.StringField()

    def __str__(self):
        op = '{{' \
             'name: {}, ' \
             'email: {}, ' \
             'username: {}, ' \
             '}}'.format(self.name,
                         self.email,
                         self.username
                         )

        return op

    def hash_password(self, password):
        self.password = sha256_crypt.hash(password)

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password)

    def set_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in=10000000)
        self.auth_token = s.dumps({'username': self.username}).decode('utf-8')

    def set_new_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in=10000000)
        self.auth_token = s.dumps({'username': self.username}).decode('utf-8')
        self.save()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired as e:
            return None  # valid token, but expired
        except BadSignature as e:
            return None  # invalid token
        user = User.objects.get(username=data['username'])
        if user and token == user.auth_token:
            return user
        else:
            return None

    def create_user(self, name, username, password):
        try:
            self.name = name
            self.username = username
            self.set_auth_token()
            self.hash_password(password)

            self.save()
            return True
        except Exception as e:
            msg = e.message
            return msg
