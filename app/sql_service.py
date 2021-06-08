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

class Jobs(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    requester_user = db.Column(db.String())
    description = db.Column(db.String())
    datetime_created = db.Column(db.DateTime())
    datetime_closed = db.Column(db.DateTime())
    datetime_asigned = db.Column(db.DateTime())
    status = db.Column(db.String())
    responsable_user = db.Column(db.String())
    estimated_hours = db.Column(db.Float())
    real_hours = db.Column(db.Float())
    tags = db.Column(db.ARRAY(db.String()))
    title = db.Column(db.String())


def get_users():
    return Users.query.all()

def get_user(username):
    return Users.query.filter_by(username=username).first()

def put_user(userdata):
    user = Users(
        username=userdata.username,
        password=userdata.password,
        email=userdata.email
    )
    print(user)
    db.session.add(user)
    db.session.commit()

def get_my_requests(username):
    return Jobs.query.filter_by(requester_user=username).all()

def get_my_jobs(username):
    return Jobs.query.filter_by(responsable_user=username).all()

def put_request(title, description, requester):
    job = Jobs(
        title = title,
        description = description,
        requester_user = requester
    )
    print(job.id)
    db.session.add(job)
    db.session.commit()
    print(job.id)

def delete_job(job_id):
    pass

def update_job(username, job_id, status):
    pass