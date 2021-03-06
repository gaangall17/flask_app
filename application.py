from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from app.sql_service import db, get_my_requests, get_my_jobs, get_profile, put_request, delete_job, update_job
from app.sql_service import get_profile, get_status_list, update_profile
from app.sql_service import db_am, get_components

import graph
import csv

import unittest
import time

from app import create_app
from app.forms import LoginForm, RequestForm, AssetForm, UserProfileForm
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
        'asset_form': new_asset_form,
    }
    return render_template('assets.html', **context)

@app.route('/assets_positions', methods=['GET','POST'])
@login_required
def assets_positions():
    username = current_user.id
    components = get_components()
    new_asset_form = AssetForm()
    positions = compute_positions(components)
    context = {
        'components': components,
        'username': username,
        'asset_form': new_asset_form,
        'positions': positions
    }
    return render_template('assets_positions.html', **context)

@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    
    username = current_user.id
    profile = get_profile(username)

    profile_form = UserProfileForm()
    profile_form.username.data = profile.username
    profile_form.name.data = profile.name
    profile_form.last_name.data = profile.last_name
    profile_form.email.data = profile.email
    profile_form.phone.data = profile.phone_work
    profile_form.role.data = profile.roles.name
    profile_form.status.data = str(profile.status.id)

    profile_form.status.choices = [(str(i.id), str(i.name)) for i in get_status_list()]
    
    context = {
        'profile_form': profile_form,
        'username': username,
        'profile': profile
    }

    return render_template('profile.html', **context)

@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    profile_form = UserProfileForm(request.form)
    profile_form.status.choices = [(str(i.id), str(i.name)) for i in get_status_list()]
    if profile_form.validate_on_submit():
        update_profile(profile_form)
    else:
        print(profile_form.errors)
    return redirect(url_for('profile'))


def compute_positions(components):
    positions_name = []
    positions_level = []
    position_desc = []
    positions_parent = []
    
    result = []
    for component in components:
        print("-----")
        print(component.vfp_id)
        vfp_wo_loc = component.vfp_id[9:]
        position_list = vfp_wo_loc.rsplit("-",3)
        position_list_length = len(position_list)
        n = 0
        for i in range(position_list_length):
            code = ""
            for j in range(i+1):
                if j != 0:
                    code += "-"
                code += position_list[j]
            position_code = str(i+4) + "-" + code
            print(position_code)
            if position_code not in positions_name:
                positions_name.append(position_code)
                if i == 0:
                    position_desc.append(component.station)
                elif i == 1:
                    position_desc.append(component.p1)
                elif i == 2:
                    position_desc.append(component.p2)
                elif i == 3:
                    if str(component.name) == str(component.p3):
                        position_desc.append(str(component.name))
                    else:
                        position_desc.append(str(component.name) + " " + str(component.p3))
                else:
                    position_desc.append("-")
                if i == 3:
                    positions_level.append("VFP")
                else:
                    positions_level.append("P")
                if i == 0:
                    parent_code = "-"
                else:
                    parent_code = str(i+3) + "-" + vfp_wo_loc.rsplit("-",4-i)[0]
                positions_parent.append(parent_code)
                print(parent_code)
            print("-----")
    for i in range(len(positions_name)):
        result.append([positions_name[i],position_desc[i],positions_level[i],positions_parent[i]])
    writecsv('outputs/positions.csv',result)
    return result

def writecsv(name, values):
    with open(name, 'w', newline='') as csvfile:
        csvdata = csv.writer(csvfile, delimiter=',', quotechar='|')
        csvdata.writerows(values)