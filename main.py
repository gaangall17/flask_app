from flask import Flask, request, make_response, redirect, render_template, session
import graph
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app) #Init bootstrap

app.config['SECRET_KEY'] = 'SUPER SECRETO' #To create session and encrypt cookies

options = ['Element 1','Element 2','Element 3']

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


@app.route('/hello')
def hello():
    #user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    context = {
        'user_ip': user_ip,
        'options': options
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