from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from app.sql_service import db, get_my_requests, get_my_jobs
import graph

import unittest
import time

from app import create_app
from app.forms import LoginForm
from credentials.credentials import get_credentials

from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = get_credentials('postgreAWS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#from app.sql_service import get_users

#print(get_users())
#new_user = User(username='guest',password='password',name='guest')
#db.session.add(new_user)
#db.session.commit()

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
@login_required
def hello():
    user_ip = session.get('user_ip')
    #username = session.get('username')
    username = current_user.id

    jobs = get_my_jobs(username)
    requests = get_my_requests(username)

    context = {
        'user_ip': user_ip,
        'options': options,
        'username': username,
        'jobs': jobs,
        'requests': requests
    }

    return render_template('hello.html', **context)  #expand dictionary as a context


@app.route('/comm_map')
@login_required
def comm_map():
    script, div = graph.render_map()
    username = current_user.id
    context = {
        'map_script': script,
        'map_div': div,
        'username': username
    }
    return render_template('comm_map.html', **context)


@app.route('/dashboard')
@login_required
def dashboard():
    username = current_user.id
    context = {
        'username': username
    }
    return render_template('dashboard.html', **context)
