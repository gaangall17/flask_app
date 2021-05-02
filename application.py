from flask import request, make_response, redirect, render_template, session, url_for, flash
import graph
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import unittest
import time

from app import create_app
from app.forms import LoginForm

from credentials.credentials import get_credentials

from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = get_credentials('postgreAWS')
metadata = MetaData(schema="control_scada")
db = SQLAlchemy(app, metadata=metadata)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    role_id = db.Column(db.Integer())
    phone_work = db.Column(db.String())
    phone_personal = db.Column(db.String())

    def __repr__(self):
        return '<User %r>' % self.username

print(User.query.all())


options = ['Element 1','Element 2','Element 3']

def timed():
    print(f'Time is {time}')

sched = BackgroundScheduler(daemon=True)
sched.add_job(timed,'interval',seconds=180)
sched.start()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

# url root where app starts
@app.route('/')     
def index():
    user_ip = request.remote_addr
    
    response = make_response(redirect('/hello'))
    #response.set_cookie('user_ip', user_ip)       #save IP in cookie for its use in other url
    session['user_ip'] = user_ip

    return response     


@app.route('/hello', methods=['GET'])
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')
    
    context = {
        'user_ip': user_ip,
        'options': options,
        'username': username
    }

    return render_template('hello.html', **context)  #expand dictionary as a context


@app.route('/comm_map')
def comm_map():
    script, div = graph.render_map()
    context = {
        'map_script': script,
        'map_div': div
    }
    return render_template('comm_map.html', **context)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
