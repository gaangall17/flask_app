from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from app.sql_service import db, get_my_requests, get_my_jobs, put_request, delete_job, update_job
from app.sql_service import db_am, get_components

import graph

import unittest
import time

from app import create_app
from app.forms import LoginForm, RequestForm, AssetForm
from credentials.credentials import get_credentials

from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = get_credentials('postgreAWS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db_am.init_app(app)
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


@app.route('/hello', methods=['GET','POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    #username = session.get('username')
    username = current_user.id

    jobs = get_my_jobs(username)
    requests = get_my_requests(username)
    new_request_form = RequestForm()

    context = {
        'user_ip': user_ip,
        'options': options,
        'username': username,
        'jobs': jobs,
        'requests': requests,
        'new_request_form': new_request_form
    }

    if new_request_form.validate_on_submit():   #Como un Post
        title = new_request_form.title.data
        description = new_request_form.description.data
        requester = username
        put_request(title,description,requester)
        return redirect(url_for('hello'))

    return render_template('hello.html', **context)  #expand dictionary as a context

@app.route('/jobs/delete/<job_id>', methods=['POST'])
def delete(job_id):
    username = current_user.id
    for job in get_my_requests(username):
        if job.id == job_id:
            delete_job(job_id)
    
    return redirect(url_for('hello'))

@app.route('/jobs/update/<job_id>/<int:status>', methods=['POST'])
def update(job_id, status):
    username = current_user.id
    for job in get_my_requests(username):
        if job.id == job_id:
            update_job(username, job_id, status)
    
    return redirect(url_for('hello'))

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

@app.route('/assets', methods=['GET','POST'])
@login_required
def assets():
    username = current_user.id
    components = get_components()
    new_asset_form = AssetForm()
    context = {
        'components': components,
        'username': username,
        'asset_form': new_asset_form
    }
    return render_template('assets.html', **context)