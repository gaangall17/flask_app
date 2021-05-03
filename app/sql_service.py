from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
#from application import app

metadata = MetaData(schema="control_scada")
db = SQLAlchemy(metadata=metadata)

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    users = db.relationship('Users', backref='roles', lazy=True)

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    phone_work = db.Column(db.String())
    phone_personal = db.Column(db.String())

    def __repr__(self):
        return '<User %r>' % self.username

def get_users():
    return Users.query.all()

def get_user(username):
    return Users.query.filter_by(username=username).first()

