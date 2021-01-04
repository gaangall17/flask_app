from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

list_1 = ['Element 1','Element 2','Element 3']

# url root where app starts
@app.route('/')     
def index():
    user_ip = request.remote_addr
    
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)       #save IP in cookie for its use in other url

    return response     


@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'list_1': list_1
    }
    return render_template('hello.html', **context)  #expand dictionary as a context