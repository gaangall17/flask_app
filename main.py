from flask import request, make_response, redirect, render_template, session, url_for, flash
import graph

import unittest
import time

from app import create_app
from app.forms import LoginForm

from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

options = ['Element 1','Element 2','Element 3']

def timed():
    print(f'Time is {time}')

sched = BackgroundScheduler(daemon=True)
sched.add_job(timed,'interval',seconds=5)
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
