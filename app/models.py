import json

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
import uuid


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    uuid = db.Column(db.String(64), index=True, unique=True, default=str(uuid.uuid4()))
    info = db.Column(db.String(256), default="")
    username = db.Column(db.String(64))
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_projects = db.Column(db.JSON, default=json.dumps([]))
    other_projects = db.Column(db.JSON, default=json.dumps([]))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=mp&s={}'.format(digest, size)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(64))
    address = db.Column(db.String(64))
    creator = db.Column(db.Integer, index=True)
    editors = db.Column(db.JSON, default=json.dumps([]))
    viewers = db.Column(db.JSON, default=json.dumps([]))
    works = db.Column(db.JSON, default=json.dumps([]))
    resources = db.Column(db.JSON, default=json.dumps([]))
    payments = db.Column(db.JSON, default=json.dumps([]))
    dependences = db.Column(db.JSON, default=json.dumps({}))

    def __repr__(self):
        return '<Project {}>'.format(self.name)
